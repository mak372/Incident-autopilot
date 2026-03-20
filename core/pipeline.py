"""IncidentPipeline: thin wrapper around the LangGraph-based IncidentGraph.

The public API is unchanged so api.py requires minimal edits.
"""
import time
from typing import Dict, Any, Optional
from datetime import datetime

from .graph import IncidentGraph, _simulate_recovery
from .models import Incident, AgentStage
from .state import incident_store


class IncidentPipeline:

    def __init__(self, guardrail_config: Optional[Dict[str, Any]] = None):
        self._graph = IncidentGraph(guardrail_config)

        # Expose agents directly for backward-compat with api.py
        self.executor = self._graph.executor

    async def run(
        self,
        incident: Incident,
        current_metrics: Dict[str, Any],
        baseline_metrics: Dict[str, Any],
        auto_approve: bool = False,
    ) -> Incident:
        """Run the full LangGraph pipeline."""
        return await self._graph.run(
            incident, current_metrics, baseline_metrics, auto_approve
        )

    async def resume_after_approval(self, incident_id: str) -> Incident:
        """Resume the graph after a human approves the mitigation."""
        return await self._graph.resume_after_approval(incident_id)

    # ------------------------------------------------------------------
    # Kept for backward-compat (api.py approve endpoint calls this)
    # ------------------------------------------------------------------

    async def _run_postcheck(
        self, incident: Incident, context: Dict[str, Any]
    ) -> Incident:
        """Direct postcheck execution (used by the legacy approve flow)."""
        incident.stage = AgentStage.POSTCHECK

        baseline = context.get("baseline_metrics", {}) or {}
        current = context.get("current_metrics", {}) or {}
        recovered_metrics = _simulate_recovery(current, baseline)
        context["current_metrics"] = recovered_metrics

        result = await self._graph.postcheck_agent.execute(context)
        incident.metrics_recovered = result["metrics_recovered"]
        incident.incident_summary = result["incident_summary"]

        incident.add_timeline_event("postcheck", "Recovery verification complete", {
            "recovered": result["metrics_recovered"],
            "checks": result.get("recovery_details", {}).get("checks", {}),
        })

        if result["metrics_recovered"]:
            print("Metrics recovered successfully")
        else:
            print("Metrics not fully recovered")
        print("Generated incident report")

        incident_store.update_incident(incident.id, incident)
        return incident
