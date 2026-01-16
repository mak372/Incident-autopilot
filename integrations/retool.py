"""Retool integration for Incident Control Tower UI.

Retool provides the enterprise UI layer for:
- Incident alerts and real-time monitoring
- Approval workflows for mitigations
- Run history and audit logs
- Evidence visualization
"""
import os
import requests
from typing import Dict, Any, List
from datetime import datetime


class RetoolClient:
    """Client for Retool API integration."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("RETOOL_API_KEY", "")
        self.base_url = "https://api.retool.com/v1"
    
    def create_incident_dashboard(self, incident_data: Dict[str, Any]) -> str:
        """Create a Retool dashboard for an incident.
        
        Args:
            incident_data: Incident details to display
            
        Returns:
            URL to the Retool dashboard
        """
        # In production, use Retool API to create/update dashboards
        # For demo, return mock URL
        return f"https://mycompany.retool.com/apps/incident-{incident_data['id']}"
    
    def send_approval_request(self, incident_id: str, mitigation: Dict[str, Any]) -> bool:
        """Send approval request to Retool Workflow.
        
        Args:
            incident_id: ID of the incident
            mitigation: Mitigation details requiring approval
            
        Returns:
            True if approval request was sent successfully
        """
        if not self.api_key:
            print(f"   ℹ️ [RETOOL] No API key - simulating approval request for incident {incident_id}")
            print(f"   📋 [RETOOL] Mitigation: {mitigation.get('type', 'unknown')}")
            return True
        
        print(f"   🔑 [RETOOL] API key detected, sending real approval request...")
        
        try:
            # Real Retool Workflows API call
            workflow_url = f"{self.base_url}/workflows/trigger"
            
            response = requests.post(
                workflow_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "workflowId": os.getenv("RETOOL_WORKFLOW_ID", "incident-approval"),
                    "data": {
                        "incident_id": incident_id,
                        "mitigation_type": mitigation.get('type', 'unknown'),
                        "description": mitigation.get('description', ''),
                        "risk_level": mitigation.get('risk_level', 'unknown'),
                        "timestamp": datetime.utcnow().isoformat()
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"   ✅ [RETOOL] Successfully sent approval request via REAL API to workflow!")
                print(f"   🎯 [RETOOL] Incident {incident_id} approval logged in Retool")
                return True
            else:
                print(f"   ⚠️ [RETOOL] API returned status {response.status_code}, using fallback")
                return False
                
        except Exception as e:
            print(f"   ⚠️ [RETOOL] API call failed: {e}")
            return False
    
    def log_incident_event(self, incident_id: str, event: Dict[str, Any]):
        """Log an incident event to Retool for audit trail.
        
        Args:
            incident_id: ID of the incident
            event: Event details to log
        """
        # In production, send to Retool's workflow API
        pass
    
    def get_approval_status(self, incident_id: str) -> str:
        """Check approval status from Retool UI.
        
        Args:
            incident_id: ID of the incident
            
        Returns:
            Approval status: 'pending', 'approved', 'rejected'
        """
        # In production, query Retool API
        return "approved"  # Auto-approve for demo

