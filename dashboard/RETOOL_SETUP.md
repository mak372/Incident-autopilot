# 🚀 Retool Dashboard Setup Guide

This guide will help you set up the **Incident Autopilot Dashboard** in Retool, a low-code platform for building internal tools.

## 📋 Prerequisites

1. **Retool Account**: Sign up at [retool.com](https://retool.com) (free tier available)
2. **Running API**: Your Incident Autopilot API should be running at `http://localhost:8000`
3. **API Access**: Ensure your Retool instance can access your local API

## 🎯 Quick Setup (2 Methods)

### Method 1: Import JSON Configuration (Recommended)

1. **Log in to Retool**
   - Go to your Retool workspace: `https://[your-company].retool.com`

2. **Create New App**
   - Click **"Create new"** → **"From JSON/YAML"**
   - Upload `retool_dashboard.json` from this directory
   - Name it: **"Incident Autopilot Dashboard"**

3. **Configure API Resource**
   - Go to **Resources** (left sidebar)
   - Edit the "Incident Autopilot API" resource
   - Update Base URL if needed:
     - Local: `http://localhost:8000/api`
     - Production: `https://your-api-domain.com/api`
   - **Important for localhost**: Enable CORS in your API or use Retool's resource proxy

4. **Test Queries**
   - Click each query in the bottom panel
   - Click **"Run"** to test
   - Verify data is loading correctly

5. **Publish**
   - Click **"Release"** in the top right
   - Your dashboard is now live!

### Method 2: Manual Setup

If you prefer to build from scratch or the JSON import doesn't work:

#### Step 1: Create REST API Resource

1. Go to **Resources** → **Create new** → **REST API**
2. Name: `Incident Autopilot API`
3. Base URL: `http://localhost:8000/api`
4. Authentication: None (or configure as needed)
5. Save resource

#### Step 2: Create Queries

Create the following queries using your REST API resource:

**Query 1: getStatistics**
```javascript
Method: GET
Path: /statistics
Run when page loads: ✓
Auto-refresh: Every 5 seconds
```

**Query 2: getIncidents**
```javascript
Method: GET
Path: /incidents
Run when page loads: ✓
Auto-refresh: Every 5 seconds
```

**Query 3: getIncidentDetail**
```javascript
Method: GET
Path: /incidents/{{ selectedIncident.value }}
Run when page loads: ✗
Trigger: On row selection
```

**Query 4: simulateIncident**
```javascript
Method: POST
Path: /incidents/simulate?incident_type={{ incidentTypeSelect.value }}&auto_approve=true
Run when page loads: ✗
Success event: Trigger getIncidents, getStatistics
```

#### Step 3: Build UI Components

##### Header Section
1. **Text Component**: "🚨 Incident Autopilot" (Title)
   - Font size: 32px, Weight: Bold, Color: #667eea

2. **Text Component**: "Multi-Agent Incident Response with Guardrails"
   - Font size: 16px, Color: #666

##### Statistics Cards (4 Statistic Components)
1. **Total Incidents**
   - Value: `{{ getStatistics.data.total_incidents || 0 }}`
   
2. **Detection Latency**
   - Value: `{{ (getStatistics.data.avg_detection_latency || 0).toFixed(1) }}`
   - Suffix: "s"

3. **Time to Mitigation**
   - Value: `{{ (getStatistics.data.avg_time_to_mitigation || 0).toFixed(1) }}`
   - Suffix: "s"

4. **Success Rate**
   - Value: `{{ (getStatistics.data.success_rate || 0).toFixed(0) }}`
   - Suffix: "%"

##### Incidents Table
1. **Table Component**: `incidentsTable`
   - Data source: `{{ getIncidents.data.incidents }}`
   - Columns:
     - `id` - Incident ID (string)
     - `severity` - Severity (tag with conditional colors)
     - `service_name` - Service (string)
     - `incident_type` - Type (string)
     - `stage` - Stage (tag)
     - `start_time` - Started (datetime)
   - Enable: Row selection, Search, Pagination
   - On row click: Set `selectedIncident` state, trigger `getIncidentDetail`

##### Controls
1. **Select Component**: `incidentTypeSelect`
   - Options: Random, Latency Spike, Error Rate, Resource Saturation, Queue Depth
   
2. **Button**: "🚀 Simulate Incident"
   - On click: Trigger `simulateIncident` query

##### Timeline Panel
1. **ListView Component**: `timelineList`
   - Data source: `{{ getIncidentDetail.data.timeline || [] }}`
   - Template: Display stage, message, and timestamp
   - Style: Left border with timeline dots

#### Step 4: Style Your Dashboard

Apply these global styles in **App Settings** → **Theme**:
- Primary color: `#667eea`
- Canvas background: Gradient from `#667eea` to `#764ba2`
- Font: System default

## 🔧 Advanced Configuration

### Enable Localhost Access

If Retool can't reach your localhost API:

**Option 1: Use Retool's Resource Proxy**
- In your REST API resource settings
- Enable "Use Retool's Resource Proxy"

**Option 2: Expose with ngrok**
```bash
# Install ngrok: https://ngrok.com
ngrok http 8000

# Update Retool API base URL with ngrok URL
https://[random-id].ngrok.io/api
```

**Option 3: Deploy API to Cloud**
- Deploy to Heroku, AWS, Vercel, etc.
- Update base URL in Retool

### Add Authentication

If your API requires authentication:

1. **API Key Authentication**
   - Edit REST API resource
   - Authentication → API Key
   - Add header: `X-API-Key: your-api-key`

2. **Bearer Token**
   - Authentication → Bearer Token
   - Token: `your-token-here`

### Set Up Alerts

1. **Create Alert Query**
   - Query: Check for critical incidents
   - Transformer: Filter by severity
   
2. **Add Alert Component**
   - Show when critical incidents detected
   - Auto-trigger mitigation workflows

## 📊 Dashboard Features

Your Retool dashboard includes:

✅ **Real-time Statistics**
- Total incidents processed
- Average detection latency
- Time to mitigation
- Success rate

✅ **Incident List**
- Sortable, searchable table
- Color-coded severity badges
- Real-time status updates
- Auto-refresh every 5 seconds

✅ **Interactive Timeline**
- Click any incident to view details
- Pipeline stage progression
- Timestamps for each action
- Agent outputs and decisions

✅ **Incident Simulation**
- Choose incident type
- One-click simulation
- Watch agents work in real-time

✅ **Approval Workflows**
- Review proposed mitigations
- Approve/reject actions
- Audit trail of decisions

## 🚀 Going to Production

### 1. Update API URLs
Replace localhost URLs with production endpoints

### 2. Enable HTTPS
Ensure all API calls use HTTPS in production

### 3. Add Authentication
Implement proper auth for your API and Retool app

### 4. Set Up Environments
- Create dev/staging/prod Retool apps
- Use environment variables for URLs

### 5. Configure Permissions
- Set user access levels in Retool
- Restrict simulation/approval to authorized users

## 🎥 Demo Script

When showing your Retool dashboard:

1. **Open Dashboard**
   - "This is our Incident Autopilot dashboard built with Retool"
   
2. **Show Statistics**
   - "These metrics update in real-time as incidents are processed"
   
3. **Simulate Incident**
   - Select incident type
   - Click simulate
   - "Watch as our multi-agent system automatically responds"
   
4. **Show Timeline**
   - Click on an incident
   - "Here you can see each agent's decision and action"
   - "The guardrails ensure safe operations"

5. **Highlight Retool Benefits**
   - "We built this dashboard quickly with Retool's low-code platform"
   - "It connects directly to our Python API"
   - "Enterprise-ready with auth, permissions, and audit logs"

## 📚 Resources

- [Retool Documentation](https://docs.retool.com)
- [REST API Resources](https://docs.retool.com/docs/rest-api-resource)
- [Retool University](https://retool.com/university)
- [JSON App Format](https://docs.retool.com/docs/import-export-apps)

## 🆘 Troubleshooting

**Dashboard won't load data:**
- Check API is running: `curl http://localhost:8000/api/statistics`
- Verify CORS is enabled
- Check browser console for errors

**Queries failing:**
- Test REST API resource connection
- Verify endpoint paths are correct
- Check query syntax in Retool

**Can't access localhost:**
- Use ngrok or Retool's proxy
- Or deploy API to accessible URL

## 💡 Tips

- Use Retool's preview mode to test before publishing
- Set up query error handlers for better UX
- Enable query caching to reduce API load
- Use transformers to format data
- Add loading states for better feedback

---

**Questions?** Check the Retool community forums or our project docs!

