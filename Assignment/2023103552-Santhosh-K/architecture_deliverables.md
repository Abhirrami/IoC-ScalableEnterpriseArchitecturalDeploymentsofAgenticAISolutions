# Capstone Deliverables — ResolveAI

**Student:** Santhosh K · **Roll No:** 2023103552

This document presents the five required enterprise-architecture deliverables for the Multi-Agent Customer Support & Resolution Assistant.

## 1. Architecture diagram

```mermaid
flowchart TB
  C[Customer / Staff] --> FE[React Frontend]
  FE -->|JWT + HTTPS| API[FastAPI API]
  API --> AUTH[Authentication & RBAC]
  API --> ORCH[Central Agent Orchestrator]
  ORCH --> QC[Query Classifier]
  QC --> RET[Information Retrieval]
  RET --> INV[Investigation]
  INV --> RES[Resolution]
  RES -->|sensitive proposal| APP[Human Approval]
  APP --> RESP[Response Generator]
  RES -->|non-sensitive / escalation| RESP
  ORCH --> TOOLS[Order & Policy Tool Adapters]
  TOOLS --> DB[(PostgreSQL + pgvector)]
  API --> AUDIT[Structured Audit / Trace Logs]
  AUDIT --> MON[Monitoring Dashboard]
```

**Trust boundaries:** Browser-to-API traffic is authenticated; the API alone accesses the database and tools; the orchestrator uses narrow tool adapters; only the human-approval API can change a pending sensitive decision to resolved. In the demonstration build, mock records replace external commerce systems.

## 2. Agent workflow design

```mermaid
stateDiagram-v2
  [*] --> Classify
  Classify --> Escalated: unsafe / unknown request
  Classify --> Retrieve: supported issue
  Retrieve --> NeedInfo: unknown order / ownership failure
  Retrieve --> Investigate: order and policy found
  Investigate --> NeedInfo: evidence missing
  Investigate --> Escalated: policy conflict / tool failure
  Investigate --> Propose: eligible
  Propose --> PendingApproval: refund or replacement
  Propose --> Resolved: safe non-sensitive outcome
  PendingApproval --> Resolved: approver accepts
  PendingApproval --> Rejected: approver rejects
```

Each transition writes an execution trace. The run has a maximum of six agent stages and a tool-call deadline. A failed or timed-out tool creates an escalation rather than a retry loop. Classification, retrieval, investigation, and proposal are distinct functions/nodes, which makes their permissions and logs independently reviewable.

## 3. Deployment strategy

```mermaid
flowchart LR
  U[Users] --> CDN[CDN / Ingress]
  CDN --> WEB[React container]
  CDN --> API1[FastAPI replicas]
  CDN --> API2[FastAPI replicas]
  API1 --> Q[Work queue for long investigations]
  API2 --> Q
  API1 --> PG[(PostgreSQL + pgvector)]
  API2 --> PG
  Q --> W[Agent worker replicas]
  W --> PG
  API1 --> O[Logs, metrics, traces]
  W --> O
```

For local delivery, Docker Compose runs frontend, backend, and PostgreSQL. In production, the API is stateless and horizontally scalable, while a queue/worker tier processes longer investigations. Use managed PostgreSQL backups, migration jobs, secret manager injection, readiness probes, autoscaling on CPU/queue depth, canary releases, and a separate production environment.

## 4. Security model

| Area | Control | Implementation in this build |
|---|---|---|
| Identity | JWT authentication | Signed bearer token issued after demo login |
| Access | RBAC and ownership isolation | Customers view their own tickets; only approvers act on proposals |
| Input | Validation and injection defense | Pydantic constraints, order-ID regex, suspicious-instruction escalation |
| Agents | Least privilege | Only tool adapter functions receive order/policy access; no approval tool exists for agents |
| Privacy | Data minimisation | Retrieval requires matching customer ID and returns a narrow order record |
| Secrets | External configuration | `.env.example`; no secrets in source |
| Audit | Immutable-style event trail | Events capture ticket, actor, action, metadata and UTC time |
| LLM safety | Output is advisory | Deterministic policy checks enforce actions independently of any model output |

## 5. Monitoring dashboard design

The dashboard exposes business, technical, and governance metrics:

| Panel | Metrics | Alert / use |
|---|---|---|
| Workflow health | ticket count, terminal status distribution, success rate | Detect stalled/excess escalations |
| Performance | average workflow duration, API latency, tool success rate | Detect degraded dependencies |
| Agent quality | classification outcomes, missing-evidence rate, trace failures | Improve prompts/policies safely |
| Safety & governance | approval queue age, rejection rate, injection escalations | Identify risky requests or bottlenecks |
| Cost | estimated tokens and cost per workflow | Set budget thresholds |
| Audit | approval history and sensitive actions | Support investigation and compliance |

The shipped UI computes dashboard values from ticket and audit records rather than displaying only fixed mock values.
