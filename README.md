# Feijoa — An AI-Native Application Built from Scratch

Feijoa is a ground-up implementation of an AI-native application,
featuring a deterministic Kernel, an Orchestrator layer, and multiple Agents.

The goal is to explore how to build controllable, extensible agent systems
with first-class software architecture.

## Plan Finite State Machine (FSM)

Every Plan in Feijoa follows a strict finite state machine (FSM) enforced at the Kernel level.

The FSM is not a convention agreed upon by agents — it is a runtime contract. Any illegal state transition fails fast at execution time. This design guarantees that plan execution is:

- Deterministic
- Auditable
- Replayable
- Safe against agent misbehavior

### Plan States

| State       | Description                                 | Terminal |
| ----------- | ------------------------------------------- | -------- |
| `PENDING`   | Submitted by a Planner, awaiting a decision | No       |
| `SELECTED`  | Chosen by the Judge agent                   | No       |
| `SIMULATED` | Successfully dry-run                        | No       |
| `EXECUTED`  | Fully executed                              | ✅        |
| `REJECTED`  | Explicitly rejected by the Judge            | ✅        |
| `FAILED`    | Failed during simulation or execution       | ✅        |

### Allowed State Transitions

Only the following state transitions are permitted. Any transition not listed here is illegal.

| From \ To     | PENDING | SELECTED | SIMULATED | EXECUTED | REJECTED | FAILED |
| ------------- | ------- | -------- | --------- | -------- | -------- | ------ |
| `PENDING`     | ➖       | ✅        | ❌         | ❌        | ✅        | ✅      |
| `SELECTED`    | ❌       | ➖        | ✅         | ❌        | ❌        | ✅      |
| `SIMULATED`   | ❌       | ❌        | ➖         | ✅        | ❌        | ✅      |
| `EXECUTED`    | ❌       | ❌        | ❌         | ➖        | ❌        | ❌      |
| `REJECTED`    | ❌       | ❌        | ❌         | ❌        | ➖        | ❌      |
| `FAILED`      | ❌       | ❌        | ❌         | ❌        | ❌        | ➖      |

State transitions are **monotonic** and **irreversible**.

### Kernel Phases

| Phase        | Description                                          | Terminal |
| ------------ | ---------------------------------------------------- | -------- |
| `PLANNING`   | Planner agents generate candidate plans              | No       |
| `DECISION`   | The Judge agent selects or rejects plans             | No       |
| `SIMULATION` | Selected plans undergo a dry run                     | No       |
| `EXECUTION`  | Simulated plans are executed for real                | No       |
| `FINISHED`   | All plans have reached a terminal state              | ✅        |

### Phase × Plan State Validity

Beyond the FSM itself, plan states must also be compatible with the current Kernel phase.

| Kernel Phase | Allowed Plan States               |
| ------------ | --------------------------------- |
| `PLANNING`   | `PENDING`                         |
| `DECISION`   | `PENDING`, `SELECTED`, `REJECTED` |
| `SIMULATION` | `SELECTED`, `SIMULATED`, `FAILED` |
| `EXECUTION`  | `SIMULATED`, `EXECUTED`, `FAILED` |
| `FINISHED`   | `EXECUTED`, `REJECTED`, `FAILED`  |

A plan state that is valid on its own may still be rejected if it is incompatible with the current phase.

### Responsibility Model

Plan state transitions are owned by agents, not by the Orchestrator.

| Transition             | Responsible Agent    |
| ---------------------- | -------------------- |
| `PENDING → SELECTED`   | JudgeAgent           |
| `PENDING → REJECTED`   | JudgeAgent           |
| `SELECTED → SIMULATED` | SimulatorAgent       |
| `SIMULATED → EXECUTED` | ExecutorAgent        |
| `ANY → FAILED`         | Any agent (on error) |

- The Orchestrator controls only phase progression.
- The Kernel enforces legality but never makes decisions.
- Agents must use the controlled transition API.

### Invariants

The following invariants are enforced at all times:

1. Plan states progress in one direction only.
2. Terminal states cannot transition further.
3. Phase transitions do not roll back due to plan failure.
4. All state transitions must pass through the FSM guard.

Violations are treated as programmer errors and raise runtime assertions.
