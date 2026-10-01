# Capstone Enterprise Architecture Deliverables: PatchCraft AI (Streamlit)

**Project Name:** PatchCraft AI - Autonomous Vulnerability Remediation Streamlit Agent  
**Architectural Baseline:** Enterprise Scalable Agentic AI Solution  
**Document Status:** Complete Deliverables Presentation  

---

## Executive Summary
PatchCraft AI is an enterprise-grade autonomous agentic assistant built in Python and Streamlit designed to continuously scan repository dependency manifests, detect CVE security vulnerabilities, evaluate update risk scores, safely execute dry-run patch validations in isolated sandboxes, and enforce Human-in-the-Loop approval gates for high-risk or breaking dependency updates.

---

## Deliverable 1: Architecture Diagram

### 1.1 Enterprise System Topology & Trust Boundaries

```mermaid
graph TB
    subgraph ClientZone ["1. Untrusted Client & Presentation Layer"]
        UI["💻 Streamlit Web Dashboard (app.py)"]
        CLI["💻 Developer CLI / Webhook Triggers"]
    end

    subgraph TrustBoundary1 ["🔐 Trust Boundary 1: API Ingress Gateway"]
        Gateway["🛡️ API Gateway & WAF<br/>(OIDC Auth, Rate Limiter, TLS 1.3)"]
    end

    subgraph SecureAgentCore ["2. Secure Agent Execution Core (Isolated Container Runtime)"]
        Orchestrator["⚙️ Agent FSM Orchestrator<br/>(src/agent_engine.py)"]
        Memory["🧠 Redis Working Memory<br/>(State Machine Context Store)"]
        
        subgraph ToolEngine ["🔧 Autonomous Tool Execution Engine"]
            ScannerTool["🔍 CVE Scanner Tool"]
            RiskTool["📐 Vulnerability Risk Evaluator"]
            SandboxTool["🧪 Patch Sandbox Tester"]
            PRTool["📦 PR Generator Tool"]
            ApprovalTool["⚠️ Approval Handoff Tool"]
        end

        subgraph GuardrailEngine ["🛡️ Security & Privacy Guardrail Layer"]
            Sanitizer["🔒 SecretSanitizerGuardrail<br/>(AWS, PAT, JWT Scrubber)"]
            ComplianceCheck["📋 Enterprise Policy Evaluator"]
        end
    end

    subgraph TrustBoundary2 ["🔐 Trust Boundary 2: External Enterprise Cloud Mesh"]
        LLMGateway["🤖 Enterprise LLM Gateway<br/>(Azure OpenAI / Anthropic)"]
        AuditLedger[("📜 Immutable Audit Ledger<br/>(PostgreSQL Ledger)")]
        NVDDatabase["🌐 National Vulnerability DB<br/>(NVD CVE API)"]
        GitHubAPI["🐙 GitHub Pull Request API"]
        NotificationChannel["💬 Slack / MS Teams Webhook"]
    end

    UI --> Gateway
    CLI --> Gateway
    Gateway --> Orchestrator
    Orchestrator <--> Memory
    Orchestrator --> ToolEngine
    ToolEngine --> GuardrailEngine
    GuardrailEngine --> LLMGateway
    GuardrailEngine --> AuditLedger
    ToolEngine --> NVDDatabase
    ToolEngine --> GitHubAPI
    ApprovalTool --> NotificationChannel
```

### 1.2 System Layer Breakdown & Component Responsibilities

| Layer | Micro-Component | Functional Responsibility | Trust Level |
| :--- | :--- | :--- | :--- |
| **Client Layer** | Streamlit UI (`app.py`) | Renders live state machine pipeline, vulnerability radar, sandbox git diffs, and metrics. | Untrusted |
| **Ingress Gate** | API Gateway | Validates OIDC JWT tokens, enforces IP rate limits, and scrubs invalid incoming payloads. | Boundary 1 |
| **Agent Core** | Orchestrator (`src/agent_engine.py`) | Enforces state transitions, manages working memory, dispatches tools, and logs telemetry. | High Trust |
| **Toolset** | CVE Scanner Tool | Parses dependency manifests (`package.json`, `pom.xml`) against live CVE databases. | High Trust |
| **Toolset** | Risk Evaluator Tool | Computes CVSS v3.1 scores, semver update delta (patch vs minor vs major), and risk weight. | High Trust |
| **Toolset** | Patch Sandbox Tool | Simulates dependency upgrades in ephemeral sandbox; executes unit & smoke test suites. | High Trust |
| **Guardrails** | Secret Sanitizer | Active regex engine scrubbing private keys, AWS tokens, and secrets prior to LLM submission. | High Trust |
| **Integrations** | GitHub / Slack APIs | Auto-generates remediation pull requests; dispatches interactive approval webhooks. | Boundary 2 |

---

## Deliverable 2: Agent Workflow Design

### 2.1 Agent State Machine (FSM) Lifecycle

```mermaid
stateDiagram-v2
    [*] --> IDLE
    IDLE --> SCANNING_CVES: Webhook Triggered / Scheduled Scan
    
    SCANNING_CVES --> ANALYZING_VULNERABILITIES: Manifest Parsed
    SCANNING_CVES --> FAILED: Parser Exception
    
    ANALYZING_VULNERABILITIES --> EVALUATING_RISK: Vulnerabilities Discovered
    ANALYZING_VULNERABILITIES --> COMPLETED: Zero Vulnerabilities Found
    
    EVALUATING_RISK --> VERIFYING_SANDBOX: Low/Med Risk (Score <= 0.5)
    EVALUATING_RISK --> AWAITING_APPROVAL: High/Breaking Risk (Score > 0.5)
    
    AWAITING_APPROVAL --> VERIFYING_SANDBOX: Security Admin Approved
    AWAITING_APPROVAL --> REJECTED: Security Admin Rejected
    
    VERIFYING_SANDBOX --> GENERATING_PR: Tests Passed in Sandbox
    VERIFYING_SANDBOX --> FAILED: Sandbox Test Suite Regression
    
    GENERATING_PR --> COMPLETED: Pull Request Opened & Logged
    
    REJECTED --> COMPLETED: Handoff Closed (No Patch Applied)
    FAILED --> EXCEPTION_RECOVERY: Retry Sandbox Task
    EXCEPTION_RECOVERY --> VERIFYING_SANDBOX: Retry Count < 3
    EXCEPTION_RECOVERY --> FAILED: Max Retries Exceeded
```

### 2.2 Roles, Tools, Handoffs & Failure Paths

- **Agent Roles**:
  - `Scanner Agent`: Parses project manifests and correlates dependencies with CVE identifiers.
  - `Risk Assessment Agent`: Evaluates CVSS v3.1 scores and semver version deltas.
  - `Remediation Agent`: Applies patches in isolated sandboxes and opens GitHub Pull Requests.
- **Human-in-the-Loop Handoff**:
  - Triggered automatically when risk score > 0.5 (e.g. Major version update like `v1.x` -> `v2.x` or CVSS score >= 8.0).
  - Execution is paused, issuing a cryptographically signed approval ticket to the Streamlit Operations Dashboard & Slack.
  - Workflow resumes ONLY upon receiving an authorized `APPROVED` signature from a Security Admin.
- **Failure & Exception Paths**:
  - Ephemeral sandbox test regressions abort PR creation and tag dependency update as `NEEDS_REFACTOR`.
  - Network timeouts trigger jittered exponential backoff ($2^n \times 1000\text{ms} \pm \text{jitter}$).

---

## Deliverable 3: Deployment Strategy

### 3.1 Target Environment Topology

```mermaid
graph LR
    subgraph Dev ["Development Environment"]
        DevPod["Single Pod Container (Streamlit)"]
        DevMock["Mock CVE DB & Mock Git"]
    end

    subgraph Staging ["Staging Environment"]
        StgCluster["Kubernetes Cluster (2 Replicas)"]
        StgDB[("Staging Database & Redis")]
    end

    subgraph Production ["Multi-AZ Production"]
        ALB["AWS ALB / Cloudflare WAF"]
        subgraph EKS ["EKS Kubernetes Cluster (Auto-Scaling)"]
            PodA["PatchCraft Pod - AZ 1"]
            PodB["PatchCraft Pod - AZ 2"]
            PodC["PatchCraft Pod - AZ 3"]
        end
        ProdRedis[("Redis Enterprise Cluster")]
        ProdDB[("PostgreSQL Aurora Multi-AZ")]
    end

    Dev --> Staging
    Staging --> Production
```

### 3.2 Deployment Strategy Key Specifications
- **Runtime Environment**: Containerized Docker image (`python:3.10-slim`) running Streamlit on Kubernetes (EKS/GKE).
- **Horizontal Pod Autoscaling (HPA)**: Target CPU = 70%, Target Memory = 75%; autoscales from 2 to 10 pods during build spikes.
- **Resilience**: Stateless pod architecture; working memory stored in Redis; graceful fallback to cached CVE database snapshots during upstream network outages.
- **Release Strategy**: Blue-Green deployment with automated smoke test verification prior to 100% traffic cutover.

---

## Deliverable 4: Security Model

### 4.1 RBAC Identity & Authorization Matrix

| User / Role | Read Manifests | Trigger Scan | Approve Breaking Patches | Admin Audit Access |
| :--- | :---: | :---: | :---: | :---: |
| **PatchCraft Agent Core** | ✔ | ✔ | x (Requires Human Gate) | x |
| **Security Administrator** | ✔ | ✔ | ✔ | ✔ |
| **Lead Developer** | ✔ | ✔ | ✔ (Low Risk Only) | x |
| **Auditor / Observer** | ✔ | x | x | ✔ |

### 4.2 Security Guardrails & Privacy Controls
1. **Secret & PII Sanitization Guardrail**:
   - Active regex scanner redacting AWS Access Keys (`AKIA...`), GitHub Personal Access Tokens (`ghp_...`), private SSH keys, and passwords to `[REDACTED_SECRET_GUARDRAIL]` before LLM processing.
2. **Key Management**:
   - Zero hardcoded credentials in source code. Secrets fetched at runtime from AWS Secrets Manager / HashiCorp Vault via IAM Workload Identity.
3. **Immutable Audit Ledger**:
   - Cryptographically hashed (SHA-256) append-only database table logging every scan result, vulnerability evaluation, and human approval signature.

---

## Deliverable 5: Monitoring Dashboard Design

### 5.1 Telemetry Metrics & Target SLAs

| Category | Metric Name | Target Baseline SLA | Alert Condition |
| :--- | :--- | :--- | :--- |
| **Health** | System Uptime & Memory Usage | > 99.9% Uptime, < 80% RAM | RAM > 85% for > 5 mins |
| **Trace** | End-to-End Patch Latency | < 15.0 seconds per run | Latency > 35s |
| **Quality** | Sandbox Build Pass Rate | > 98% Green Builds | Regression Rate > 2% |
| **Safety** | PII & Secret Leak Interception | 100% Interception | Any un-sanitized token in prompt |
| **Cost** | LLM Token Cost / Patch Run | < 12,500 tokens / run | Cost > \$0.20 per run |
| **Outcomes** | Vulnerability Mean Time to Remediate (MTTR) | Reduced from 14 days to < 2 hours | MTTR > 24 hours |

### 5.2 Operations Dashboard Interface
The Streamlit Web Application (`app.py`) embeds an interactive telemetry dashboard displaying:
- Live FSM State Machine pipeline status and execution timer.
- Timestamped tool log streaming terminal.
- Vulnerability Radar displaying CVE severity badges (CRITICAL, HIGH, MEDIUM).
- Patch Sandbox view showing git diff previews and test suite results.
- Human-in-the-Loop interactive approval expander/form.
