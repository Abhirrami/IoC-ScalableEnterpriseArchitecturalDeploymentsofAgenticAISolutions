# Build Prompt: ResolveAI

Build a polished, runnable **Multi-Agent Customer Support & Resolution Assistant** named **ResolveAI** for an e-commerce organisation. The application must demonstrate a governed agentic workflow rather than acting as a simple chatbot.

## Product requirements

Create a React frontend and a Python FastAPI backend. A customer can log in, submit a support message with an order ID, inspect ticket status, and see the workflow outcome. Support staff can inspect tickets. Only an authorised approver can approve or reject proposed refunds or replacements.

Use a central workflow/orchestrator with the following logical agents:

1. **Query Classifier**: detect the issue type, requested action, urgency, and suspicious instructions.
2. **Information Retrieval**: retrieve only the customer’s order record and matching support policy.
3. **Investigation**: verify delivery age, order ownership, evidence requirements, policy eligibility, and missing data.
4. **Resolution**: generate a safe proposed outcome; it may never finalise a refund or replacement.
5. **Escalation**: route ambiguous, unsafe, ineligible, or incomplete cases to a human.
6. **Response Generator**: return a concise, friendly, status-aware response.

Model each run as a bounded state machine. Include a max-step guard, per-tool timeouts/failure handling, step traces, and clear terminal states: `RESOLVED`, `PENDING_APPROVAL`, `NEEDS_INFORMATION`, `ESCALATED`, and `REJECTED`. Keep the LLM optional: deterministic rules and mock tool adapters must make the demo work with no API key. Add an adapter boundary for Gemini through environment configuration, but do not send untrusted text directly to a model or grant model output authority over tools.

## Security and governance requirements

- Implement JWT authentication and roles: `customer`, `support_agent`, `approver`, and `admin`.
- Enforce ownership filtering for customers and role checks on staff routes.
- Validate input length and order ID format.
- Detect prompt-injection signals such as “ignore previous instructions” and escalate rather than carrying out instructions.
- Never let an agent approve its own proposed sensitive action.
- Record structured audit events for ticket creation, tool calls, resolution proposals, and human approvals.
- Store secrets in environment variables; provide `.env.example` only.

## Interface requirements

The React UI should include a welcoming customer support form, a live workflow trace, a ticket list, a dashboard with total tickets, workflow-resolution rate, response time, escalation rate, ticket status distribution, tool success rate, approval wait time, and estimated token/cost fields. Include a staff approval panel that is only rendered for an approver account. Show demo credentials and a ready-to-use damaged-laptop example.

## Delivery requirements

Provide Docker Compose for frontend, backend, and PostgreSQL; health checks; clear README instructions; backend tests for a happy-path replacement request, customer isolation, and approval authorization. Document architecture, agent workflow, deployment/scaling, security controls, and monitoring. Use Mermaid diagrams in the Markdown deliverables.
