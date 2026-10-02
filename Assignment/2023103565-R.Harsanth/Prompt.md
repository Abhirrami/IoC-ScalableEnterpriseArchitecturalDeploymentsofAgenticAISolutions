\# AEGISDESK — Agentic IT Support Demonstrator



\## Project Prompt



Design and implement an enterprise-oriented agentic IT support system named \*\*AEGISDESK\*\* that demonstrates how an AI-powered support agent can safely receive IT support requests, understand the request, retrieve relevant internal knowledge, execute permitted diagnostic actions, enforce security and approval policies, and provide a traceable response.



The system should demonstrate an agentic workflow rather than a simple chatbot. It must separate request planning, knowledge retrieval, policy enforcement, tool execution, human approval, response generation, and observability.



\## Core Requirements



The system must:



1\. Accept IT support requests through a web interface.

2\. Classify and route requests to appropriate support workflows.

3\. Retrieve relevant information from an internal support knowledge base.

4\. Execute simulated IT diagnostic tools for safe operations.

5\. Identify protected or sensitive actions.

6\. Require human approval before protected actions are executed.

7\. Never automatically perform sensitive account or device changes.

8\. Provide clear responses explaining the action taken or the reason an action is blocked.

9\. Maintain request identifiers and workflow trace information.

10\. Maintain an approval queue for protected actions.

11\. Maintain audit information for requests, policy decisions, approvals, and outcomes.

12\. Expose health and operational metrics.

13\. Provide an operations dashboard for monitoring the demonstrator.

14\. Run reproducibly using Docker Compose.

15\. Include automated tests covering routing, retrieval, safety gating, and simulated tools.



\## Demonstrated Support Scenarios



The implementation should demonstrate at least the following workflows:



\### Scenario 1 — Wi-Fi Troubleshooting



A user reports that Wi-Fi is disconnecting or internet connectivity is intermittent.



The agent should:



\* classify the request as a network/Wi-Fi issue;

\* retrieve the relevant internal Wi-Fi troubleshooting guidance;

\* execute a simulated connectivity diagnostic;

\* provide safe troubleshooting steps;

\* clearly indicate that no external network configuration was changed.



\### Scenario 2 — Corporate VPN



A user reports that the corporate VPN is not connecting.



The agent should:



\* classify the request as a VPN issue;

\* retrieve the VPN support guidance;

\* execute a simulated VPN diagnostic;

\* provide safe troubleshooting steps;

\* clearly indicate that credentials or configuration were not modified.



\### Scenario 3 — Protected Account Action



A user asks the system to unlock an account or perform another sensitive account/device action.



The agent should:



\* identify the request as a protected action;

\* stop automatic execution;

\* create an approval request;

\* place the request in the approval queue;

\* allow an authorized operator to approve or reject the request;

\* record the approval decision and rationale;

\* never perform the sensitive action automatically.



\### Scenario 4 — Support Ticket



A user explicitly requests that a support ticket be created.



The agent should:



\* identify the ticketing request;

\* create a simulated ticket;

\* return a demonstrator ticket reference;

\* explicitly state that no external ticketing system was contacted.



\## Security and Governance Principles



The design should follow:



\* Human-in-the-loop approval for sensitive operations.

\* Least-privilege tool access.

\* Policy checks before tool execution.

\* Explicit separation between safe diagnostics and protected actions.

\* No automatic execution of sensitive account/device changes.

\* No hard-coded production credentials or secrets.

\* Clear distinction between simulated and real integrations.

\* Request and approval auditability.

\* Fail-closed behavior for protected operations.

\* Safe handling of unknown or unsupported requests.



\## Architecture Requirements



The architecture should document:



\* User interface;

\* API layer;

\* agent orchestrator;

\* planner/router;

\* knowledge retrieval;

\* local knowledge base;

\* policy and guardrail layer;

\* simulated tools;

\* approval queue;

\* human approver;

\* response composer;

\* audit/event storage;

\* metrics and health endpoints;

\* operations dashboard;

\* future enterprise integrations;

\* trust boundaries.



\## Deployment Requirements



The solution should demonstrate:



\* Docker-based deployment;

\* Docker Compose orchestration;

\* FastAPI/Uvicorn runtime;

\* reproducible dependency installation;

\* health checking;

\* restart behavior;

\* automated tests;

\* environment separation;

\* a documented path toward production scaling and resilience.



\## Monitoring Requirements



The monitoring design should cover:



\* service health;

\* request throughput;

\* latency;

\* error rate;

\* workflow traces;

\* retrieval behavior;

\* tool execution;

\* approval activity;

\* policy blocks;

\* safety events;

\* ticket creation;

\* operational workload;

\* resolution-related business metrics;

\* future model/API cost tracking.



\## Design Principles



The project should demonstrate the following enterprise agentic AI principles:



1\. \*\*Human oversight\*\* — sensitive actions require authorized approval.

2\. \*\*Policy-first execution\*\* — authorization is checked before tool execution.

3\. \*\*Least privilege\*\* — agents receive only the capabilities required for their task.

4\. \*\*Local-first operation\*\* — the demonstrator can operate without external AI or enterprise APIs.

5\. \*\*Explicit simulation\*\* — mocked integrations must never be presented as real enterprise actions.

6\. \*\*Traceability\*\* — important workflow stages should be observable.

7\. \*\*Auditability\*\* — requests, approvals, decisions, and outcomes should be recorded.

8\. \*\*Fail-safe behavior\*\* — uncertainty or policy violations should result in safe stopping or escalation.

9\. \*\*Reproducibility\*\* — the project should be runnable using the documented Docker workflow.

10\. \*\*Production extensibility\*\* — simulated integrations should be replaceable by authenticated enterprise adapters without redesigning the overall architecture.



