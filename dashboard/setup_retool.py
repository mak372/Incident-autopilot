#!/usr/bin/env python3
"""
Setup script for Retool dashboard integration.

This script helps configure and test your Retool dashboard connection.
"""
import os
import json
import requests
from typing import Dict, Any, Optional
from pathlib import Path


class RetoolDashboardSetup:
    """Helper class for setting up Retool dashboard."""
    
    def __init__(self, api_url: str = "http://localhost:8000", retool_api_key: Optional[str] = None):
        self.api_url = api_url
        self.retool_api_key = retool_api_key or os.getenv("RETOOL_API_KEY")
        self.dashboard_dir = Path(__file__).parent
    
    def test_api_connection(self) -> bool:
        """Test connection to Incident Autopilot API."""
        print("🔍 Testing API connection...")
        
        try:
            response = requests.get(f"{self.api_url}/api/statistics", timeout=5)
            if response.status_code == 200:
                print("   ✅ API is accessible")
                data = response.json()
                print(f"   📊 Total incidents: {data.get('total_incidents', 0)}")
                return True
            else:
                print(f"   ❌ API returned status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Cannot connect to {self.api_url}")
            print(f"   💡 Make sure your API server is running:")
            print(f"      python main.py --mode server")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def test_api_endpoints(self):
        """Test all API endpoints used by Retool dashboard."""
        print("\n🔍 Testing API endpoints...")
        
        endpoints = [
            ("/api/statistics", "Statistics"),
            ("/api/incidents", "Incidents List"),
        ]
        
        results = []
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {name}: OK")
                    results.append(True)
                else:
                    print(f"   ❌ {name}: Status {response.status_code}")
                    results.append(False)
            except Exception as e:
                print(f"   ❌ {name}: {e}")
                results.append(False)
        
        return all(results)
    
    def generate_retool_config(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate Retool configuration with current API URL."""
        print("\n📝 Generating Retool configuration...")
        
        config_path = self.dashboard_dir / "retool_dashboard.json"
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Update API URL
        for resource in config.get("resources", []):
            if resource["name"] == "incident_api":
                resource["options"]["baseUrl"] = f"{self.api_url}/api"
                print(f"   ✅ Updated API URL to: {self.api_url}/api")
        
        # Save updated config
        if output_path:
            output_file = Path(output_path)
        else:
            output_file = self.dashboard_dir / "retool_dashboard_configured.json"
        
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"   ✅ Saved configuration to: {output_file}")
        print(f"\n   📋 Next steps:")
        print(f"   1. Go to your Retool workspace")
        print(f"   2. Click 'Create new' → 'From JSON/YAML'")
        print(f"   3. Upload: {output_file}")
        
        return config
    
    def get_dashboard_info(self) -> Dict[str, Any]:
        """Get information about the dashboard setup."""
        return {
            "api_url": self.api_url,
            "api_accessible": self.test_api_connection(),
            "dashboard_json": str(self.dashboard_dir / "retool_dashboard.json"),
            "setup_guide": str(self.dashboard_dir / "RETOOL_SETUP.md"),
            "retool_features": [
                "Real-time incident monitoring",
                "Statistics dashboard",
                "Interactive incident timeline",
                "One-click incident simulation",
                "Approval workflows (with API key)",
                "Auto-refresh every 5 seconds"
            ]
        }
    
    def print_setup_instructions(self):
        """Print setup instructions."""
        print("\n" + "="*70)
        print("🚀 RETOOL DASHBOARD SETUP")
        print("="*70)
        
        print("\n📋 Quick Start:")
        print("   1. Sign up for Retool: https://retool.com")
        print("   2. Create a new app → 'From JSON/YAML'")
        print(f"   3. Upload: {self.dashboard_dir / 'retool_dashboard.json'}")
        print("   4. Update API URL in the resource to your endpoint")
        print("   5. Test queries and publish!")
        
        print("\n📚 Detailed Guide:")
        print(f"   Read: {self.dashboard_dir / 'RETOOL_SETUP.md'}")
        
        print("\n🌐 Current API URL:")
        print(f"   {self.api_url}/api")
        
        if self.api_url.startswith("http://localhost"):
            print("\n⚠️  Using localhost - for Retool access:")
            print("   Option 1: Use ngrok to expose localhost")
            print("      ngrok http 8000")
            print("   Option 2: Deploy API to cloud (Heroku, AWS, etc.)")
            print("   Option 3: Enable Retool's resource proxy")
        
        print("\n✨ Dashboard Features:")
        info = self.get_dashboard_info()
        for feature in info["retool_features"]:
            print(f"   • {feature}")
        
        print("\n" + "="*70)
    
    def create_retool_resource_snippet(self) -> str:
        """Generate code snippet for Retool resource configuration."""
        snippet = f"""
// Retool REST API Resource Configuration
// Copy this into your Retool REST API resource

Resource Name: Incident Autopilot API
Base URL: {self.api_url}/api
Authentication: None

// Endpoints to configure as queries:

1. getStatistics
   Method: GET
   Path: /statistics
   Run when page loads: ✓
   Auto-refresh: 5000ms

2. getIncidents
   Method: GET
   Path: /incidents
   Run when page loads: ✓
   Auto-refresh: 5000ms

3. getIncidentDetail
   Method: GET
   Path: /incidents/{{{{ selectedIncident.value }}}}
   Run when page loads: ✗

4. simulateIncident
   Method: POST
   Path: /incidents/simulate?incident_type={{{{ incidentTypeSelect.value }}}}&auto_approve=true
   Run when page loads: ✗
   Success Event: Trigger getIncidents, getStatistics
"""
        return snippet
    
    def save_resource_snippet(self):
        """Save resource configuration snippet to file."""
        snippet = self.create_retool_resource_snippet()
        snippet_file = self.dashboard_dir / "retool_resource_config.txt"
        
        with open(snippet_file, 'w') as f:
            f.write(snippet)
        
        print(f"\n📄 Saved resource configuration to: {snippet_file}")
        return snippet_file


def main():
    """Main setup function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Setup and test Retool dashboard integration"
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="Incident Autopilot API URL"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test API connection and endpoints"
    )
    parser.add_argument(
        "--generate-config",
        action="store_true",
        help="Generate Retool configuration with current API URL"
    )
    parser.add_argument(
        "--output",
        help="Output path for generated configuration"
    )
    
    args = parser.parse_args()
    
    setup = RetoolDashboardSetup(api_url=args.api_url)
    
    if args.test:
        print("🧪 Testing Incident Autopilot API...\n")
        api_ok = setup.test_api_connection()
        if api_ok:
            setup.test_api_endpoints()
        return
    
    if args.generate_config:
        setup.generate_retool_config(args.output)
        setup.save_resource_snippet()
        return
    
    # Default: show setup instructions
    setup.print_setup_instructions()
    
    # Test connection
    print("\n🧪 Testing connection...")
    api_ok = setup.test_api_connection()
    
    if api_ok:
        print("\n✅ Your API is ready for Retool integration!")
    else:
        print("\n⚠️  Start your API server first:")
        print("   python main.py --mode server")


if __name__ == "__main__":
    main()

