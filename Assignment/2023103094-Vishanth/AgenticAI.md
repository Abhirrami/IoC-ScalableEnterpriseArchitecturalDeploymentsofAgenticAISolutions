# Agentic AI: Overview

## 1. What is Agentic AI?

Agentic AI refers to AI systems that can **pursue a goal on their own**. They plan steps, use tools, observe results, and adjust until the task is done. A traditional chatbot answers one question at a time. An agent takes a goal such as "resolve this customer's refund request" and works through it end to end.

**Core idea:** LLM (reasoning) + Tools (actions) + Memory (context) + Loop (repeat until done)

---

## 2. Assistant vs Agent vs Multi-Agent

| Type | Can call tools? | Can change systems? | Example |
|---|---|---|---|
| AI assistant | No | No | Summarizes a policy document |
| Single agent | Yes | Yes (within limits) | Looks up an order and creates a ticket |
| Multi-agent system | Yes | Yes | Research, compliance, and cost agents review a design together |

**Guideline:** Start with one tool-enabled agent. Add more agents only when there is a clear reason.

---

## 3. Core Components

1. **Model (LLM):** reasons, plans, and decides the next step.
2. **Tools:** APIs, databases, search, code execution, and other systems the agent can act on.
3. **Memory:**
   - *Short-term:* the current conversation and task context.
   - *Long-term:* persistent knowledge stored across sessions.
4. **Planner / control loop:** decides what to do, does it, checks the result, and repeats.
5. **Guardrails:** policies, permissions, and approvals that limit what the agent may do.

---

## 4. The Agent Loop

```text
Goal → Plan → Act (call tool) → Observe result → Reflect → Done? 
                    ↑                                      |
                    └────────────── No ────────────────────┘
```

Every loop needs an **iteration limit and a stop condition** so the agent cannot run forever.

---

## 5. Common Design Patterns

- **Tool use:** the agent calls functions or APIs to get data or take actions.
- **Reflection:** the agent reviews and improves its own output.
- **Planning:** the agent breaks a large goal into smaller steps.
- **Supervisor / worker:** a manager agent delegates to specialist agents.
- **Sequential pipeline:** steps run in order, each using the previous output.
- **Concurrent fan-out / fan-in:** independent agents work in parallel and the results are merged.
- **Human-in-the-loop:** a person approves risky actions before they happen.

---

## 6. Knowledge and Retrieval

- **RAG:** retrieve relevant documents, then let the model answer using them.
- **Embeddings and vector databases:** enable search by meaning.
- **Knowledge graph / Graph-RAG:** best for questions that follow relationships across several hops, such as supplier → product → regulation.
- **Permission-aware retrieval:** filter out documents the user is not allowed to see *before* they reach the model.

---

## 7. Security and Governance

- **Prompt injection defense:** treat retrieved text as untrusted data, never as instructions.
- **Least privilege:** each agent gets only the permissions it needs.
- **Authorization at the tool boundary:** check every tool call in code, outside the model.
- **Safe data access:** use allowlisted, parameterized services instead of letting the model write raw SQL.
- **Secrets management:** keep keys in a vault, use workload identity, and redact logs.
- **Human approval gates:** required for money movement, production changes, and other irreversible actions.
- **Audit logging:** record who or what did what, and when.

---

## 8. Reliability Patterns

| Problem | Pattern |
|---|---|
| One failing tool blocks other work | Bulkhead isolation |
| Retry could cause a duplicate action | Idempotency key |
| Restart loses workflow state | Durable external state store |
| Process waits days for a human | Durable workflow with interrupt and resume |
| Agent loops or overspends | Iteration and tool-call budgets |
| Workers return inconsistent results | Typed input/output contracts |

---

## 9. Observability and Operations

- **Distributed tracing:** one span per model call, retrieval, and tool call, so you can see where time goes.
- **Quality metrics:** task success rate, human override rate, groundedness.
- **Cost tracking:** spend per task and per agent, with alerts.
- **Evaluation before release:** run regression tests on representative workflows.
- **Controlled rollout:** canary release with a rollback plan.

---

## 10. Integration Options

- **OpenAPI-based business API:** typed, governed, synchronous calls.
- **A2A (Agent-to-Agent):** task exchange between agents.
- **Events and commands:** commands request an action ("Approve invoice 481"), and events record that it happened ("Invoice 481 was approved").

---

## 11. Example Use Cases

- Customer support agent that checks orders and prepares refunds for approval
- IT operations copilot that answers from databases and runs approved runbooks
- Research agent that gathers sources and drafts a summary
- Procurement agent that compares suppliers and flags compliance risks

---

## 12. Reference Architecture

```text
User (natural language)
        ↓
Supervisor agent
        ↓
Retrieval + specialist agents
        ↓
Policy and approval layer
        ↓
Governed response / action
        ↓
Monitored cloud runtime (tracing, metrics, audit logs)
```

---

## 13. Best Practices Checklist

- [ ] Start with the simplest design that works
- [ ] Set iteration limits and budgets
- [ ] Enforce permissions outside the model
- [ ] Add human approval for irreversible actions
- [ ] Store state durably, not in local memory
- [ ] Use idempotency keys for retryable actions
- [ ] Trace every step end to end
- [ ] Evaluate before rollout, and keep a rollback path
- [ ] Deliver architecture, security, and monitoring documentation, not only code

---

## 14. Key Terms

| Term | Meaning |
|---|---|
| Agent | An LLM that can plan and use tools to reach a goal |
| Orchestration | Coordinating multiple agents or steps |
| Guardrail | A control that limits unsafe behavior |
| Idempotency | Repeating a request has the same effect as doing it once |
| Span | One timed step within a distributed trace |
| Graph-RAG | Retrieval that follows relationships in a knowledge graph |