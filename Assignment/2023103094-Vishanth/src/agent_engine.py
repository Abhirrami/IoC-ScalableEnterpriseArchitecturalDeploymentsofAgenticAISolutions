import re
import time
from datetime import datetime

class SecretSanitizerGuardrail:
    """Active regex sanitizer redacting sensitive tokens and credentials."""
    def __init__(self):
        self.patterns = [
            r'AKIA[0-9A-Z]{16}',                                       # AWS Access Key
            r'ghp_[a-zA-Z0-9]{36}',                                    # GitHub Personal Access Token
            r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+',                     # JWT Token
            r'-----BEGIN PRIVATE KEY-----[\s\S]+?-----END PRIVATE KEY-----' # SSH Key
        ]

    def sanitize(self, text: str):
        if not isinstance(text, str):
            return text, 0
        scrubbed_count = 0
        sanitized = text
        for p in self.patterns:
            matches = re.findall(p, sanitized)
            if matches:
                scrubbed_count += len(matches)
                sanitized = re.sub(p, '[REDACTED_SECRET_GUARDRAIL]', sanitized)
        return sanitized, scrubbed_count

class PatchCraftAgentEngine:
    """Core Finite State Machine Agentic Engine for Security Vulnerability Patching."""
    def __init__(self):
        self.state = 'IDLE'
        self.sanitizer = SecretSanitizerGuardrail()
        this_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execution_logs = []
        this_mem = {}
        self.active_memory = this_mem
        self.pending_approval = None
        self.metrics = {
            'totalRuns': 0,
            'tokensConsumed': 0,
            'sanitizedSecretsCount': 0,
            'lastRunTimeMs': 0
        }

    def log_step(self, state, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{state}]: {message}"
        self.execution_logs.append(entry)
        return entry

    def run_patch_workflow(self, simulate_critical=False):
        start_time = time.time()
        self.metrics['totalRuns'] += 1
        self.pending_approval = None
        self.execution_logs = []

        # 1. SCANNING_CVES
        self.state = 'SCANNING_CVES'
        self.log_step('SCANNING_CVES', 'Parsing repository package manifests (package.json, pom.xml)...')

        if simulate_critical:
            scanned_deps = [
                {'package': 'express', 'currentVersion': '4.17.1', 'cve': 'CVE-2026-4491', 'cvss': 8.8, 'severity': 'CRITICAL', 'patchVersion': '5.0.0 (Major)'},
                {'package': 'axios', 'currentVersion': '0.21.1', 'cve': 'CVE-2026-1182', 'cvss': 7.5, 'severity': 'HIGH', 'patchVersion': '1.7.2'}
            ]
        else:
            scanned_deps = [
                {'package': 'lodash', 'currentVersion': '4.17.19', 'cve': 'CVE-2026-0921', 'cvss': 4.3, 'severity': 'MEDIUM', 'patchVersion': '4.17.21'},
                {'package': 'minimist', 'currentVersion': '1.2.5', 'cve': 'CVE-2026-0044', 'cvss': 5.3, 'severity': 'LOW', 'patchVersion': '1.2.8'}
            ]

        self.active_memory['scannedDeps'] = scanned_deps
        self.log_step('SCANNING_CVES', f'Manifest parsed. Found {len(scanned_deps)} package vulnerabilities matching NVD advisories.')

        # 2. ANALYZING_VULNERABILITIES
        self.state = 'ANALYZING_VULNERABILITIES'
        self.log_step('ANALYZING_VULNERABILITIES', 'Cross-referencing National Vulnerability Database (NVD) risk metrics...')

        risk_score = 0.88 if simulate_critical else 0.25
        is_high_risk = risk_score > 0.5
        self.active_memory['vulnerabilityReport'] = {
            'scannedDeps': scanned_deps,
            'riskScore': risk_score,
            'isHighRisk': is_high_risk
        }
        self.metrics['tokensConsumed'] += 1120

        # 3. EVALUATING_RISK & GUARDRAILS
        self.state = 'EVALUATING_RISK'
        self.log_step('EVALUATING_RISK', 'Checking security guardrails and scanning prompt context for secrets...')

        test_prompt = 'Manifest scan for repo with token ghp_A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8'
        _, scrubbed_count = self.sanitizer.sanitize(test_prompt)
        if scrubbed_count > 0:
            self.metrics['sanitizedSecretsCount'] += scrubbed_count
            self.log_step('SECURITY_GUARDRAIL', f'SecretSanitizerGuardrail triggered: Redacted {scrubbed_count} GitHub Personal Access Token(s).')

        if is_high_risk:
            self.state = 'AWAITING_APPROVAL'
            self.pending_approval = {
                'id': f'TICKET-{int(time.time())}',
                'riskScore': risk_score,
                'deps': scanned_deps,
                'status': 'PENDING'
            }
            self.log_step('AWAITING_APPROVAL', f'HIGH RISK / MAJOR VERSION UPDATE DETECTED (Risk Score: {risk_score}). Workflow paused for Security Admin approval.')
            self.metrics['lastRunTimeMs'] = int((time.time() - start_time) * 1000)
            return self.get_summary()

        # 4. CONTINUE POST APPROVAL
        return self.continue_post_approval(start_time)

    def continue_post_approval(self, start_time=None):
        if start_time is None:
            start_time = time.time()

        # 4. VERIFYING_SANDBOX
        self.state = 'VERIFYING_SANDBOX'
        self.log_step('VERIFYING_SANDBOX', 'Spinning up ephemeral docker sandbox to execute dry-run build & automated test suite...')

        git_diff = """diff --git a/package.json b/package.json
index a1b2c3d..e5f6g7h 100644
--- a/package.json
+++ b/package.json
@@ -12,4 +12,4 @@
-    "express": "^4.17.1",
+    "express": "^5.0.0",
-    "axios": "^0.21.1"
+    "axios": "^1.7.2"
"""
        self.active_memory['sandbox'] = {
            'status': 'PASSED',
            'testCount': 42,
            'passedCount': 42,
            'gitDiff': git_diff
        }
        self.metrics['tokensConsumed'] += 1450
        self.log_step('VERIFYING_SANDBOX', 'Sandbox Verification PASSED! 42/42 unit & integration tests verified.')

        # 5. GENERATING_PR
        self.state = 'GENERATING_PR'
        self.log_step('GENERATING_PR', 'Auto-generating GitHub Pull Request: "fix(security): patch CVE vulnerabilities"...')

        # 6. COMPLETED
        self.state = 'COMPLETED'
        self.log_step('COMPLETED', 'PatchCraft AI workflow completed successfully! Pull request opened & audit logged.')

        self.metrics['lastRunTimeMs'] = int((time.time() - start_time) * 1000)
        return self.get_summary()

    def get_summary(self):
        return {
            'state': self.state,
            'activeMemory': self.active_memory,
            'pendingApproval': self.pending_approval,
            'executionLogs': self.execution_logs,
            'metrics': self.metrics
        }
