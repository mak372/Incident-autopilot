# Incident Autopilot — Agentic Incident Response System

Incident Autopilot is a **multi-agent, human-in-the-loop incident response system** that simulates how modern SRE / platform teams detect, analyze, and mitigate production incidents.

The system orchestrates **specialized agents** (Scout, Triage, Hypothesis, Experiment, Executor, Postcheck) to reason about incidents, propose safe mitigations, enforce guardrails, and optionally wait for **human approval** before taking action.


---

## Key Features

-  **Agentic architecture** — each stage is handled by a specialized agent
-  **Evidence-driven reasoning** using metrics, logs, deploy history, and runbooks
-  **Guardrails** to prevent unsafe mitigations
-  **Human-in-the-loop approval** for risky actions
-  **Asynchronous orchestration** using FastAPI background tasks
-  **Live dashboard** to monitor incidents and timelines
-  **Pluggable AI** (rule-based fallback or LLM-based reasoning)
-  **Deterministic simulator** for reproducible incidents (no real infra required)

---

## System Architecture

```text
Incident Detected
      ↓
┌──────────┐
│  Scout   │  → Collects metrics, logs, deploys, runbooks
└──────────┘
      ↓
┌──────────┐
│  Triage  │  → Classifies incident type (latency, errors, etc.)
└──────────┘
      ↓
┌────────────┐
│ Hypothesis │  → Generates root cause hypotheses
└────────────┘
      ↓
┌────────────┐
│ Experiment │  → Validates hypotheses against evidence
└────────────┘
      ↓
┌───────────┐
│ Executor  │  → Proposes mitigation (guardrails + approval)
└───────────┘
      ↓
┌───────────┐
│ Postcheck │  → Verifies recovery and generates report
└───────────┘
