# Agent Workflow

## State and handoffs

```mermaid
sequenceDiagram
  participant U as Customer
  participant O as Orchestrator
  participant C as Classifier
  participant R as Retrieval tool
  participant I as Investigation
  participant A as Approver
  U->>O: message + order ID
  O->>C: classify and safety-screen
  alt suspicious or unclassified
    C-->>O: escalate
  else supported
    O->>R: customer-scoped order + policy lookup
    R-->>O: bounded records
    O->>I: eligibility verification
    alt incomplete/ineligible
      I-->>O: need info or escalate
    else eligible sensitive action
      I-->>O: replacement/refund proposal
      O->>A: pending approval
      A-->>O: accept or reject
    end
  end
  O-->>U: status-aware response + ticket update
```

## Node contract

| Node | Inputs | Output | Permission |
|---|---|---|---|
| Query Classifier | validated customer message | issue type, action, priority, unsafe flag | no tools |
| Information Retrieval | customer ID, validated order ID, issue type | scoped order and policy data | read-only adapters |
| Investigation | retrieved records | eligibility, missing evidence, escalation reason | no tools |
| Resolution | investigation finding | proposed action and next status | cannot execute action |
| Human Approval | ticket, approver identity, note | final approve/reject decision | approver/admin only |
| Response Generator | final ticket state | customer-facing explanation | no tools |

## Failure paths and bounded execution

The state machine has a six-step maximum. Each node records a trace record. An unsupported intent, suspicious instruction, absent policy, or tool failure becomes an `ESCALATED` ticket. A missing order/evidence result becomes `NEEDS_INFORMATION`. No node retries itself indefinitely; production tool adapters should use short timeouts, a limited retry policy for transient failures, circuit breakers, and dead-letter handling for asynchronous jobs.
