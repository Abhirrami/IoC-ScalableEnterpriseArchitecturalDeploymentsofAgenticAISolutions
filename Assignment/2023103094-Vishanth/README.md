# PatchCraft AI - Streamlit Agentic Assistant

PatchCraft AI is an enterprise-grade autonomous agentic assistant built in Python and Streamlit. It continuously monitors software repository dependency manifests, scans CVE security databases, evaluates update risk scores, runs dry-run patch validations in isolated sandboxes, auto-generates pull requests, and enforces Human-in-the-Loop approval gates for breaking updates.

---

## 🤖 What Does PatchCraft AI Actually Do?

PatchCraft AI automates end-to-end software dependency security patch governance through a 6-phase autonomous agent loop:

1. **🔍 Continuous CVE Vulnerability Detection**:
   - Parses repository manifest files (`package.json`, `requirements.txt`, `pom.xml`).
   - Scans and correlates dependencies against live National Vulnerability Database (NVD) advisories and CVE security feeds.

2. **📐 CVSS Risk & Breaking Change Assessment**:
   - Calculates a normalized **Breaking Risk Score (0.0 to 1.0)** based on CVSS v3.1 severity metrics and semver upgrade deltas (`patch` vs `minor` vs `major` breaking updates).

3. **🔒 Secret & PII Sanitization Guardrail**:
   - Intercepts all prompt payloads before sending context to LLMs.
   - Automatically redacts AWS Access Keys (`AKIA...`), GitHub Personal Access Tokens (`ghp_...`), JWT tokens, and private SSH keys to `[REDACTED_SECRET_GUARDRAIL]`.

4. **🧪 Dry-Run Sandbox Test Verification**:
   - Spins up an ephemeral, isolated container sandbox.
   - Applies the dependency upgrade, compiles the codebase, and runs full unit/integration test suites to guarantee 100% green builds before opening any PRs.

5. **⚠️ Human-in-the-Loop Approval Governance**:
   - Automatically pauses autonomous execution whenever a major version upgrade or high-risk CVE (Risk Score > 0.5) is detected.
   - Issues a cryptographically signed approval ticket to the Streamlit Operations Dashboard and Slack, requiring explicit Security Admin signature.

6. **📦 Automated Pull Requests & Immutable Audit Logging**:
   - Auto-generates GitHub Pull Requests with syntax-highlighted git diff previews and CVE changelogs.
   - Records every tool invocation, security decision, and admin approval signature in an immutable, append-only SHA-256 ledger.

---

## 📁 Repository & Project Structure

```
Agentic-Assistant-Project/
├── PROMPT.md                  # Master AI Prompt used to generate PatchCraft AI
├── DELIVERABLES.md            # Enterprise Capstone Architectural Documentation (All 5 Deliverables)
├── README.md                  # Overview, architecture guide, & run instructions
├── requirements.txt           # Python dependency file (streamlit, pandas)
├── app.py                     # Main Streamlit Web Application Dashboard
└── src/                       # Source Code Directory
    ├── __init__.py
    ├── agent_engine.py        # Core Agent FSM Engine, Tools, & Secret Guardrails
    └── utils.py               # Telemetry logging & data formatting helpers
```

---

## 🏆 Capstone Deliverables Summary (`DELIVERABLES.md`)

1. **Deliverable 1: Architecture Diagram**: 3-tier enterprise architecture mapping Client Streamlit UI Layer, Ingress Gateway (Trust Boundary 1), Secure Agent Core Layer, Tool Execution Engine, Security Guardrail Layer, and Enterprise Cloud Mesh (Trust Boundary 2).
2. **Deliverable 2: Agent Workflow Design**: Finite State Machine lifecycle, agent roles, tool execution schemas, human-in-the-loop approval handoffs, and error recovery paths.
3. **Deliverable 3: Deployment Strategy**: Docker/Kubernetes pod runtime, Horizontal Pod Autoscaler (HPA), resilience patterns, multi-environment setup, and Blue-Green release strategy.
4. **Deliverable 4: Security Model**: RBAC identity matrix, Vault secret management, `SecretSanitizerGuardrail` PII & token scrubber, and SHA-256 immutable audit ledger.
5. **Deliverable 5: Monitoring Dashboard Design**: Telemetry matrix for system health, execution trace latencies, sandbox build pass rates, guardrail block triggers, LLM token costs, and developer SLA outcomes.

---

## 🚀 How to Run the Streamlit Application

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch the Streamlit web application:
   ```bash
   streamlit run app.py
   ```

3. Open your browser to the local URL (typically `http://localhost:8501`).
