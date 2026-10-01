# MASTER PROMPT: Streamlit PatchCraft AI Agentic Assistant Generator

You are an expert Autonomous Systems & Software Security Architect. Generate a complete, modular, Python Streamlit agentic assistant application and capstone architectural documentation for **PatchCraft AI**, an autonomous vulnerability scanning, dependency patching, and remediation agentic assistant.

---

## 🎯 APPLICATION GOAL & CAPABILITIES
PatchCraft AI continuously monitors software repository dependency manifests (e.g. `package.json`, `requirements.txt`, `pom.xml`), scans known CVE security databases, assesses update risk and CVSS severity scores, runs patch validation in an isolated sandbox, auto-generates remediation pull requests, and pauses for Human-in-the-Loop approval whenever a breaking version update or high-risk vulnerability remediation is encountered.

---

## 📁 PROJECT DIRECTORY & FILE STRUCTURE

```
Agentic-Assistant-Project/
├── PROMPT.md                  # Master AI Generation Prompt
├── DELIVERABLES.md            # Enterprise Capstone Architecture Documentation (5 Deliverables)
├── README.md                  # Overview, architecture guide, & run instructions
├── requirements.txt           # Python dependency file (streamlit)
├── app.py                     # Main Streamlit Application UI & Dashboard
└── src/                       # Source Code Folder
    ├── __init__.py
    ├── agent_engine.py        # Core Agent FSM Engine, Tools, & Guardrails
    └── utils.py               # Telemetry logging & formatting utilities
```

---

## 📑 CAPSTONE DELIVERABLES SPECIFICATION (`DELIVERABLES.md`)
Must document all 5 enterprise capstone artifacts matching the capstone framework image:
1. **Architecture Diagram**: 3-tier architecture mapping Client Streamlit UI Layer, Ingress Gateway (Trust Boundary 1), Secure Agent Core Layer, Tool Execution Engine, Security Guardrail Layer, and Enterprise Cloud Mesh (Trust Boundary 2).
2. **Agent Workflow Design**: Multi-agent roles, Finite State Machine (FSM) state transitions (`SCANNING_CVES` -> `ANALYZING_VULNERABILITIES` -> `EVALUATING_RISK` -> `AWAITING_APPROVAL` -> `VERIFYING_SANDBOX` -> `GENERATING_PR` -> `COMPLETED`), tool contracts, human-in-the-loop approval handoffs, and error recovery paths.
3. **Deployment Strategy**: Containerized Kubernetes runtime topology (Docker/K8s), horizontal pod autoscaling (HPA), resilience patterns (Circuit Breaker, Exponential Backoff), multi-environment setup (Dev, Staging, Multi-AZ Prod), and Blue-Green release deployment.
4. **Security Model**: RBAC identity matrix, OAuth2/OIDC, Vault secrets management, `SecretSanitizerGuardrail` PII & SSH key redactor, and SHA-256 immutable audit ledger.
5. **Monitoring Dashboard Design**: Telemetry matrix for system health, execution trace latencies, sandbox build pass rates, guardrail block triggers, LLM token costs, and engineering team SLA outcomes.

---

## ⚙️ PYTHON STREAMLIT APP SPECIFICATION (`app.py` & `src/`)

### 1. Agent Engine (`src/agent_engine.py`)
- **State Machine**: States include `IDLE`, `SCANNING_CVES`, `ANALYZING_VULNERABILITIES`, `EVALUATING_RISK`, `AWAITING_APPROVAL`, `VERIFYING_SANDBOX`, `GENERATING_PR`, `COMPLETED`, `REJECTED`, `FAILED`.
- **Tools**:
  - `CVEScannerTool`: Parses manifest files against live CVE database advisories.
  - `VulnerabilityRiskEvaluator`: Computes CVSS v3.1 risk scores and semver version deltas.
  - `SecretSanitizerGuardrail`: Regex scanner redacting AWS Access Keys, GitHub PATs, JWT tokens, and private SSH keys to `[REDACTED_SECRET_GUARDRAIL]`.
  - `PatchSandboxTool`: Simulates dependency updates and executes virtual test suites.
  - `PRGeneratorTool`: Auto-generates GitHub Pull Request metadata and change logs.

### 2. Streamlit Dashboard UI (`app.py`)
- Sidebar layout with configuration triggers ("▶ Run Security Scan", "⚠️ Simulate Critical CVE Patch").
- Interactive tabs:
  1. ⚡ **Operations & FSM Pipeline**: Animated state progression, live execution logs.
  2. 🛡️ **Vulnerability Radar**: CVE metrics, risk scores, interactive vulnerability table.
  3. 🧪 **Patch Sandbox & Git Diff**: View simulated git diffs and unit test suite results.
  4. 📊 **Telemetry & SLAs**: Live `st.metric` widgets, LLM token cost tracking, PII sanitization counter, and Capstone compliance framework.
- **Human-in-the-Loop Approval Interface**: Interactive Streamlit form/expander triggered on risk score > 0.5 requiring Security Admin signature.

---

## 🎨 EXECUTION STANDARDS
- Built using clean, idiomatic Python 3.9+ and Streamlit.
- Must run cleanly with `streamlit run app.py` with zero runtime errors.
