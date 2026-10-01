import streamlit as st
import pandas as pd
import json
import time
from src.agent_engine import PatchCraftAgentEngine

# Streamlit Page Config
st.set_page_config(
    page_title="PatchCraft AI - Autonomous Vulnerability Remediation Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Glassmorphism & Aesthetics
st.markdown("""
<style>
    .main { background-color: #0a0e1a; }
    .stApp { background-color: #0a0e1a; color: #f8fafc; }
    
    .status-badge-idle { padding: 4px 12px; background-color: rgba(148, 163, 184, 0.2); color: #94a3b8; border-radius: 12px; font-weight: bold; }
    .status-badge-running { padding: 4px 12px; background-color: rgba(6, 182, 212, 0.2); color: #06b6d4; border-radius: 12px; font-weight: bold; }
    .status-badge-awaiting { padding: 4px 12px; background-color: rgba(245, 158, 11, 0.25); color: #f59e0b; border-radius: 12px; font-weight: bold; }
    .status-badge-completed { padding: 4px 12px; background-color: rgba(16, 185, 129, 0.2); color: #10b981; border-radius: 12px; font-weight: bold; }

    .terminal-box {
        background-color: #050811;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 12px;
        font-family: monospace;
        font-size: 0.85rem;
        color: #38bdf8;
        max-height: 280px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'agent' not in st.session_state:
    st.session_state.agent = PatchCraftAgentEngine()

agent = st.session_state.agent
summary = agent.get_summary()

# Header Layout
col_logo, col_title, col_badge = st.columns([1, 6, 3])

with col_logo:
    st.title("🛡️")

with col_title:
    st.markdown("## **PatchCraft AI**")
    st.caption("Autonomous Security Vulnerability Remediation & Patching Streamlit Agent")

with col_badge:
    state = summary['state']
    if state == 'IDLE':
        st.markdown('<span class="status-badge-idle">STATE: IDLE</span>', unsafe_allow_html=True)
    elif state == 'AWAITING_APPROVAL':
        st.markdown('<span class="status-badge-awaiting">⚠️ STATE: AWAITING_APPROVAL</span>', unsafe_allow_html=True)
    elif state == 'COMPLETED':
        st.markdown('<span class="status-badge-completed">✔ STATE: COMPLETED</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="status-badge-running">⚡ STATE: {state}</span>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar Controls
st.sidebar.header("⚡ Agent Controls")
st.sidebar.markdown("Trigger autonomous vulnerability scan loops or simulate critical breaking updates.")

if st.sidebar.button("▶ Run Security Scan (Standard)", type="primary", use_container_width=True):
    with st.spinner("Executing autonomous agent scan loop..."):
        agent.run_patch_workflow(simulate_critical=False)
        st.rerun()

if st.sidebar.button("⚠️ Simulate Critical CVE Patch", use_container_width=True):
    with st.spinner("Simulating high-risk CVE dependency update..."):
        agent.run_patch_workflow(simulate_critical=True)
        st.rerun()

if st.sidebar.button("🔄 Reset Agent State", use_container_width=True):
    st.session_state.agent = PatchCraftAgentEngine()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🏆 Capstone Deliverables")
st.sidebar.markdown("""
- **1. Architecture Diagram**: 3-tier boundary model
- **2. Agent Workflow**: Finite State Machine
- **3. Deployment Strategy**: K8s HPA & Blue-Green
- **4. Security Model**: RBAC & Secret Sanitizer
- **5. Monitoring Dashboard**: Telemetry & SLAs
""")

# Human-in-the-Loop Approval Modal Alert (If Awaiting Approval)
if summary['state'] == 'AWAITING_APPROVAL' and summary['pendingApproval']:
    appr = summary['pendingApproval']
    st.warning(f"⚠️ **HUMAN-IN-THE-LOOP APPROVAL REQUIRED** (Ticket ID: {appr['id']})")
    
    with st.expander("🔍 **Review High-Risk Vulnerability & Breaking Patch Details**", expanded=True):
        st.write(f"**Risk Score:** `{appr['riskScore']}` (Exceeds approval threshold 0.5)")
        st.write("**Affected Package Dependencies:**")
        for dep in appr['deps']:
            st.markdown(f"- 🔴 **{dep['package']}** (`{dep['currentVersion']}` ➡️ `{dep['patchVersion']}`) | **{dep['cve']}** (CVSS `{dep['cvss']}`) - *{dep['severity']}*")
        
        signature = st.text_input("Security Admin Signature / Authorization Note:", "Approved major dependency patch for release v2.0")
        
        col_app, col_rej = st.columns(2)
        with col_app:
            if st.button("✔ Approve & Execute Sandbox", type="primary", use_container_width=True):
                agent.continue_post_approval()
                st.success("Human Approval GRANTED. Resuming agent execution...")
                st.rerun()
        with col_rej:
            if st.button("✖ Reject & Terminate Patch", use_container_width=True):
                agent.state = 'REJECTED'
                agent.log_step('REJECTED', f'Human approval REJECTED by Admin. Reason: {signature}')
                st.error("Patch workflow rejected and terminated.")
                st.rerun()

# Main Interactive Dashboard Tabs
tab_ops, tab_vuln, tab_sandbox, tab_telemetry = st.tabs([
    "⚡ Operations Pipeline",
    "🛡️ Vulnerability Radar",
    "🧪 Patch Sandbox",
    "📊 Telemetry & SLAs"
])

# TAB 1: OPERATIONS PIPELINE
with tab_ops:
    st.subheader("Agent State Machine Execution Pipeline")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    steps = [
        ("1. Scan Manifests", 'SCANNING_CVES'),
        ("2. Check CVE DB", 'ANALYZING_VULNERABILITIES'),
        ("3. Risk & Guardrails", 'EVALUATING_RISK'),
        ("4. Human Gate", 'AWAITING_APPROVAL'),
        ("5. Verify Sandbox", 'VERIFYING_SANDBOX'),
        ("6. Generate PR", 'GENERATING_PR')
    ]
    
    current_state = summary['state']
    
    for i, (label, step_state) in enumerate(steps):
        col = [col1, col2, col3, col4, col5, col6][i]
        with col:
            if current_state == step_state:
                st.info(f"🔵 **{label}**")
            elif current_state == 'COMPLETED':
                st.success(f"✔ **{label}**")
            else:
                st.text(f"⚪ {label}")

    st.markdown("---")
    st.subheader("🖥️ Real-time Execution & Tool Log Stream")
    
    logs_html = "<div class='terminal-box'>"
    for log in summary['executionLogs']:
        logs_html += f"<div>{log}</div>"
    if not summary['executionLogs']:
        logs_html += "<div>[00:00:00] [SYSTEM]: PatchCraft AI ready. Click 'Run Security Scan' to start.</div>"
    logs_html += "</div>"
    
    st.markdown(logs_html, unsafe_allow_html=True)

# TAB 2: VULNERABILITY RADAR
with tab_vuln:
    st.subheader("🛡️ Vulnerability Radar & Risk Assessment")
    
    memory = summary['activeMemory']
    if 'vulnerabilityReport' in memory:
        report = memory['vulnerabilityReport']
        
        st.metric(
            label="Overall Vulnerability Risk Score",
            value=f"{report['riskScore']:.2f}",
            delta="HIGH RISK" if report['isHighRisk'] else "LOW RISK",
            delta_color="inverse" if report['isHighRisk'] else "normal"
        )
        
        st.write("#### Discovered CVE Vulnerabilities:")
        df = pd.DataFrame(report['scannedDeps'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Run security scan to analyze repository manifest dependencies...")

# TAB 3: PATCH SANDBOX
with tab_sandbox:
    st.subheader("🧪 Sandbox Dry-Run & Automated Diff Preview")
    
    memory = summary['activeMemory']
    if 'sandbox' in memory:
        sb = memory['sandbox']
        st.success(f"✔ Sandbox Test Suite Status: **{sb['status']}** ({sb['passedCount']}/{sb['testCount']} unit & integration tests clean)")
        
        st.write("#### Automated Git Diff Preview:")
        st.code(sb['gitDiff'], language="diff")
    else:
        st.info("Run agent patch cycle to generate git diff sandbox verification...")

# TAB 4: TELEMETRY & CAPSTONE METRICS
with tab_telemetry:
    st.subheader("📊 Live Telemetry & Capstone Compliance")
    
    metrics = summary['metrics']
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Patch Runs", metrics['totalRuns'])
    m2.metric("Avg Latency", f"{metrics['lastRunTimeMs']/1000:.2f}s", "Target SLA < 15s")
    m3.metric("Tokens Consumed", f"{metrics['tokensConsumed']:,}", "~$0.02 / run")
    m4.metric("Sanitized Secrets", metrics['sanitizedSecretsCount'], "PII & Keys Scrubbed")

    st.markdown("---")
    st.subheader("🏆 Enterprise Capstone Architecture Compliance")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 1. Architecture Diagram")
        st.caption("3-tier trust boundary model with API Gateway ingress and Redis working memory.")
    with c2:
        st.markdown("#### 2. Agent Workflow Design")
        st.caption("Finite State Machine with Human-in-the-Loop handoff gate for risk score > 0.5.")
    with c3:
        st.markdown("#### 3. Security & Guardrails")
        st.caption("SecretSanitizerGuardrail active regex scanning AWS keys, SSH keys, and PAT tokens.")
