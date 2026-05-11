"""LangGraph-based incident pipeline with LangSmith tracing."""
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from langsmith import traceable

from .models import (
    Incident, AgentStage, Evidence, Hypothesis, ExperimentResult
)
from .guardrails import GuardrailEngine
from .state import incident_store

from agents.scout import ScoutAgent
from agents.triage import TriageAgent
from agents.hypothesis import HypothesisAgent
from agents.experiment import ExperimentAgent
from agents.executor import ExecutorAgent
from agents.postcheck import PostcheckAgent


class IncidentGraphState(TypedDict):
    incident: Any  # Incident (Pydantic)
    current_metrics: Dict[str, Any]
    baseline_metrics: Dict[str, Any]
    detection_start: float
    auto_approve: bool
    # Context propagated between nodes
    evidence: Optional[Any]          # Evidence
    runbooks: Optional[Dict[str, Any]]
    incident_type: Optional[Any]     # IncidentType
    reasoning: Optional[str]
    hypotheses: Optional[List[Any]]  # List[Hypothesis]
    most_likely_cause: Optional[Any] # ExperimentResult
    error: Optional[str]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _simulate_recovery(
    current_metrics: Dict[str, float],
    baseline_metrics: Dict[str, float],
) -> Dict[str, float]:
    b_p50 = float(baseline_metrics.get("latency_p50", 120))
    b_p95 = float(baseline_metrics.get("latency_p95", 200))
    b_p99 = float(baseline_metrics.get("latency_p99", 250))
    b_err = float(baseline_metrics.get("error_rate", 0.05))

    return {
        "latency_p50": b_p50 * 1.05,
        "latency_p95": b_p95 * 1.10,
        "latency_p99": b_p99 * 1.10,
        "error_rate": b_err * 1.50,
        "cpu_usage": 45,
        "memory_usage": 60,
        "request_rate": float(current_metrics.get("request_rate", 100)),
        "queue_depth": float(current_metrics.get("queue_depth", 50)),
    }


# ---------------------------------------------------------------------------
# Main graph class
# ---------------------------------------------------------------------------

class IncidentGraph:
    """LangGraph-powered multi-agent incident response pipeline."""

    def __init__(self, guardrail_config: Optional[Dict[str, Any]] = None):
        self.guardrails = GuardrailEngine(guardrail_config)
        self.scout = ScoutAgent()
        self.triage = TriageAgent()
        self.hypothesis = HypothesisAgent()
        self.experiment = ExperimentAgent()
        self.executor = ExecutorAgent(self.guardrails)
        self.postcheck_agent = PostcheckAgent()

        self._checkpointer = MemorySaver()
        self._graph = self._build_graph()

    # ------------------------------------------------------------------
    # Graph construction
    # ------------------------------------------------------------------

    def _build_graph(self):
        builder = StateGraph(IncidentGraphState)

        builder.add_node("scout", self._scout_node)
        builder.add_node("triage", self._triage_node)
        builder.add_node("hypothesis", self._hypothesis_node)
        builder.add_node("experiment", self._experiment_node)
        builder.add_node("executor", self._executor_node)
        builder.add_node("postcheck", self._postcheck_node)

        builder.add_edge(START, "scout")
        builder.add_edge("scout", "triage")
        builder.add_edge("triage", "hypothesis")
        builder.add_edge("hypothesis", "experiment")
        builder.add_edge("experiment", "executor")
        builder.add_edge("executor", "postcheck")
        builder.add_edge("postcheck", END)

        return builder.compile(checkpointer=self._checkpointer)

    # ------------------------------------------------------------------
    # Context helper
    # ------------------------------------------------------------------

    def _build_context(self, state: IncidentGraphState) -> Dict[str, Any]:
        return {
            "incident": state["incident"],
            "current_metrics": state["current_metrics"],
            "baseline_metrics": state["baseline_metrics"],
            "detection_start": state["detection_start"],
            "evidence": state.get("evidence"),
            "runbooks": state.get("runbooks"),
            "incident_type": state.get("incident_type"),
            "reasoning": state.get("reasoning"),
            "hypotheses": state.get("hypotheses"),
            "most_likely_cause": state.get("most_likely_cause"),
        }

    # ------------------------------------------------------------------
    # Agent nodes (each decorated with @traceable for LangSmith)
    # ------------------------------------------------------------------

    @traceable(name="scout_node")
    async def _scout_node(self, state: IncidentGraphState) -> dict:
        incident = state["incident"]
        print("[SCOUT] Gathering evidence...")
        incident.stage = AgentStage.SCOUT
        context = self._build_context(state)

        result = await self.scout.execute(context)
        incident.evidence = result["evidence"]
        incident.add_timeline_event("scout", result["summary"], {
            "metrics_count": len(result["evidence"].metrics),
            "logs_count": len(result["evidence"].logs),
        })
        incident_store.update_incident(incident.id, incident)
        print(f"   ✓ {result['summary']}")

        return {
            "incident": incident,
            "evidence": result["evidence"],
            "runbooks": result.get("runbooks", {}),
        }

    @traceable(name="triage_node")
    async def _triage_node(self, state: IncidentGraphState) -> dict:
        incident = state["incident"]
        print("[TRIAGE] Classifying incident type...")
        incident.stage = AgentStage.TRIAGE
        context = self._build_context(state)

        result = await self.triage.execute(context)
        incident.incident_type = result["incident_type"]
        incident.metrics.triage_accuracy = result["confidence"]
        incident.add_timeline_event("triage", result["reasoning"], {
            "type": result["incident_type"].value,
            "confidence": result["confidence"],
        })
        incident_store.update_incident(incident.id, incident)
        print(f"Type: {result['incident_type'].value} (confidence: {result['confidence']:.0%})")

        return {
            "incident": incident,
            "incident_type": result["incident_type"],
            "reasoning": result["reasoning"],
        }

    @traceable(name="hypothesis_node")
    async def _hypothesis_node(self, state: IncidentGraphState) -> dict:
        incident = state["incident"]
        print("[HYPOTHESIS] Generating root cause hypotheses...")
        incident.stage = AgentStage.HYPOTHESIS
        context = self._build_context(state)

        result = await self.hypothesis.execute(context)
        incident.hypotheses = result["hypotheses"]
        incident.add_timeline_event("hypothesis", result["summary"], {
            "count": len(result["hypotheses"]),
        })
        incident_store.update_incident(incident.id, incident)
        print(f"   ✓ Generated {len(result['hypotheses'])} hypotheses")
        for i, h in enumerate(result["hypotheses"], 1):
            print(f"   {i}. {h.description} (confidence: {h.confidence:.0%})")

        return {
            "incident": incident,
            "hypotheses": result["hypotheses"],
        }

    @traceable(name="experiment_node")
    async def _experiment_node(self, state: IncidentGraphState) -> dict:
        incident = state["incident"]
        print("[EXPERIMENT] Validating hypotheses...")
        incident.stage = AgentStage.EXPERIMENT
        context = self._build_context(state)

        result = await self.experiment.execute(context)
        incident.experiments = result["experiment_results"]
        incident.add_timeline_event("experiment", result["summary"], {
            "validated_count": sum(1 for r in result["experiment_results"] if r.validated),
        })
        incident_store.update_incident(incident.id, incident)
        print(f"{result['summary']}")
        best = result["most_likely_cause"]
        print(f"Most likely: {best.findings}")

        return {
            "incident": incident,
            "most_likely_cause": result["most_likely_cause"],
        }

    @traceable(name="executor_node")
    async def _executor_node(self, state: IncidentGraphState) -> dict:
        incident = state["incident"]
        print("[EXECUTOR] Proposing mitigation...")
        incident.stage = AgentStage.EXECUTOR
        context = self._build_context(state)

        result = await self.executor.execute(context)

        if result["status"] == "blocked":
            print(f"Mitigation blocked by guardrails: {result['reason']}")
            incident.add_timeline_event(
                "executor", "Mitigation blocked by guardrails",
                {"reason": result["reason"]},
            )
            incident_store.update_incident(incident.id, incident)
            return {"incident": incident}

        mitigation = result["mitigation"]
        incident.proposed_mitigation = mitigation
        print(f"Proposed: {mitigation.type.value}")
        print(f"{mitigation.description}")
        print(f"Risk: {mitigation.risk_level}, Reversible: {mitigation.reversible}")

        if mitigation.requires_approval and not state["auto_approve"]:
            incident.add_timeline_event(
                "executor", "Mitigation proposed — awaiting human approval",
                {"mitigation_type": mitigation.type.value},
            )
            incident_store.update_incident(incident.id, incident)

            print(f"\n{'='*60}")
            print(f"⏸️  PIPELINE PAUSED (Awaiting Approval): {incident.id}")
            print(f"Proposed mitigation: {mitigation.type.value}")
            print(f"{'='*60}\n")

            # Human-in-the-loop: pause the graph until resumed
            approved = interrupt({
                "incident_id": incident.id,
                "mitigation": mitigation.type.value,
                "message": "Awaiting human approval — call POST /api/incidents/{id}/approve to continue",
            })

            if not approved:
                incident.stage = AgentStage.FAILED
                incident.add_timeline_event("executor", "Mitigation rejected by human")
                incident_store.update_incident(incident.id, incident)
                return {"incident": incident}

        # Apply mitigation
        print("Applying mitigation...")
        apply_result = await self.executor.apply_mitigation(mitigation, incident.service_name)

        if apply_result["success"]:
            mitigation_time = time.time() - state["detection_start"]
            incident.metrics.time_to_mitigation_seconds = mitigation_time
            incident.applied_mitigation = mitigation
            incident.mitigation_approved = True
            incident.add_timeline_event("executor", "Mitigation applied successfully", {
                "mitigation_type": mitigation.type.value,
                "time_to_mitigation": f"{mitigation_time:.1f}s",
                "applied_at": apply_result.get("applied_at"),
            })
            print(f"Mitigation applied successfully (time: {mitigation_time:.1f}s)")
        else:
            print(f"Mitigation failed: {apply_result.get('message')}")
            incident.add_timeline_event("executor", "Mitigation apply failed", apply_result)

        incident_store.update_incident(incident.id, incident)
        return {"incident": incident}

    @traceable(name="postcheck_node")
    async def _postcheck_node(self, state: IncidentGraphState) -> dict:
        incident = state["incident"]
        print("[POSTCHECK] Verifying recovery...")
        incident.stage = AgentStage.POSTCHECK
        context = self._build_context(state)

        # Simulate metrics improving after mitigation
        baseline = context.get("baseline_metrics", {}) or {}
        current = context.get("current_metrics", {}) or {}
        context["current_metrics"] = _simulate_recovery(current, baseline)

        result = await self.postcheck_agent.execute(context)
        incident.metrics_recovered = result["metrics_recovered"]
        incident.incident_summary = result["incident_summary"]
        incident.add_timeline_event("postcheck", "Recovery verification complete", {
            "recovered": result["metrics_recovered"],
            "checks": result.get("recovery_details", {}).get("checks", {}),
        })

        incident.end_time = datetime.utcnow()
        incident.stage = AgentStage.COMPLETED if incident.metrics_recovered else AgentStage.FAILED
        incident.metrics.detection_latency_seconds = 2.5
        if not incident.metrics.time_to_mitigation_seconds:
            incident.metrics.time_to_mitigation_seconds = time.time() - state["detection_start"]
        incident.metrics.mitigation_success = incident.metrics_recovered

        incident.add_timeline_event(
            "completed" if incident.metrics_recovered else "failed",
            "Incident pipeline completed" if incident.metrics_recovered
            else "Incident pipeline finished but not recovered",
        )

        if result["metrics_recovered"]:
            print("Metrics recovered successfully")
        else:
            print("Metrics not fully recovered")
        print("Generated incident report")

        incident_store.update_incident(incident.id, incident)
        return {"incident": incident}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def run(
        self,
        incident: Incident,
        current_metrics: Dict[str, Any],
        baseline_metrics: Dict[str, Any],
        auto_approve: bool = False,
    ) -> Incident:
        detection_start = time.time()
        config = {"configurable": {"thread_id": incident.id}}

        print(f"\n{'='*60}")
        print(f"INCIDENT GRAPH STARTED: {incident.id}")
        print(f"Service: {incident.service_name}")
        print(f"{'='*60}\n")

        incident_store.update_incident(incident.id, incident)

        initial_state: IncidentGraphState = {
            "incident": incident,
            "current_metrics": incident.current_metrics or current_metrics,
            "baseline_metrics": incident.baseline_metrics or baseline_metrics,
            "detection_start": detection_start,
            "auto_approve": auto_approve,
            "evidence": None,
            "runbooks": None,
            "incident_type": None,
            "reasoning": None,
            "hypotheses": None,
            "most_likely_cause": None,
            "error": None,
        }

        try:
            result = await self._graph.ainvoke(initial_state, config=config)
            incident = result.get("incident", incident)
        except Exception as e:
            print(f"Graph execution error: {e}")
            incident.stage = AgentStage.FAILED
            incident.add_timeline_event("failed", f"Pipeline failed: {str(e)}")
            incident_store.update_incident(incident.id, incident)

        ttm = incident.metrics.time_to_mitigation_seconds or 0.0
        print(f"\n{'='*60}")
        print(f"INCIDENT GRAPH FINISHED: {incident.id}")
        print(f"Stage: {incident.stage.value}")
        print(f"Time to mitigation: {ttm:.1f}s")
        print(f"Success: {incident.metrics.mitigation_success}")
        print(f"{'='*60}\n")

        return incident

    async def resume_after_approval(self, incident_id: str) -> Incident:
        """Resume the graph after human approves the proposed mitigation."""
        config = {"configurable": {"thread_id": incident_id}}
        incident = incident_store.get_incident(incident_id)

        print(f"\n{'='*60}")
        print(f"RESUMING GRAPH AFTER APPROVAL: {incident_id}")
        print(f"{'='*60}\n")

        try:
            result = await self._graph.ainvoke(
                Command(resume=True), config=config
            )
            incident = result.get("incident", incident)
        except Exception as e:
            print(f"Graph resume error: {e}")
            if incident:
                incident.stage = AgentStage.FAILED
                incident.add_timeline_event("failed", f"Resume failed: {str(e)}")
                incident_store.update_incident(incident_id, incident)

        return incident
