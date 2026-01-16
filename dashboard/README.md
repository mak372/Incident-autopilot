# 📊 Incident Autopilot Dashboards

This directory contains two dashboard options for monitoring your Incident Autopilot system:

## 🎨 Dashboard Options

### 1. HTML Dashboard (Built-in)
**Location:** `index.html`

A beautiful, self-contained dashboard that runs directly in your browser.

**Features:**
- ✨ Real-time statistics (detection latency, mitigation time, success rate)
- 📋 Interactive incident list with filtering
- 📈 Live timeline showing agent actions
- 🚀 One-click incident simulation
- 🔄 Auto-refresh every 5 seconds
- 📱 Responsive design

**Usage:**
```bash
# Start the server
python main.py --mode server

# Open browser to:
http://localhost:8000
```

---

### 2. Retool Dashboard (Enterprise)
**Location:** `retool_dashboard.json`

A professional, low-code dashboard built with Retool - perfect for demonstrating enterprise integration capabilities.

**Features:**
- 🏢 **Enterprise-ready UI** with Retool's platform
- 📊 **Same features** as HTML dashboard
- 🔐 **Built-in authentication** and permissions
- 🔗 **Workflow integration** for approvals
- 📈 **Advanced analytics** capabilities
- 🎨 **Customizable** components
- 📱 **Mobile app support**

**Quick Setup:**
1. Sign up at [retool.com](https://retool.com) (free tier available)
2. Create new app → "From JSON/YAML"
3. Upload `retool_dashboard.json`
4. Update API URL in resources
5. Publish!

**Detailed Guide:** See `RETOOL_SETUP.md`

**Setup Helper:**
```bash
# Test your API connection
python setup_retool.py --test

# Generate configured JSON
python setup_retool.py --generate-config

# View setup instructions
python setup_retool.py
```

---

## 🎯 Which Dashboard to Use?

### Use HTML Dashboard if:
- ✅ You want something working immediately
- ✅ You're doing a quick demo
- ✅ You don't need user authentication
- ✅ You want zero setup

### Use Retool Dashboard if:
- ✅ You want to showcase enterprise integrations
- ✅ You need user permissions and roles
- ✅ You want approval workflows
- ✅ You're building for a team/company
- ✅ You want to say "built with Retool" 😉

---

## 📁 Files in This Directory

| File | Description |
|------|-------------|
| `index.html` | Self-contained HTML dashboard |
| `retool_dashboard.json` | Retool app configuration |
| `RETOOL_SETUP.md` | Comprehensive Retool setup guide |
| `setup_retool.py` | Helper script for Retool setup |
| `README.md` | This file |

---

## 🚀 Quick Start

### Option 1: HTML Dashboard (Instant)
```bash
python main.py --mode server
# Open: http://localhost:8000
```

### Option 2: Retool Dashboard (5 minutes)
```bash
# 1. Test your API
python dashboard/setup_retool.py --test

# 2. Go to retool.com and sign up

# 3. Create new app from JSON
#    Upload: dashboard/retool_dashboard.json

# 4. Done! 🎉
```

---

## 🎥 Demo Tips

### When Demoing HTML Dashboard:
- "We built a real-time control tower for incident response"
- Focus on the multi-agent workflow
- Show live timeline updates

### When Demoing Retool Dashboard:
- "We integrated with Retool for enterprise-grade UI"
- "This connects to our Python API in real-time"
- "Shows how our system can integrate with enterprise tools"
- Highlight the low-code platform benefits

---

## 🔧 Configuration

Both dashboards connect to the same API:

**API Base URL:** `http://localhost:8000/api`

**Endpoints Used:**
- `GET /api/statistics` - Overall metrics
- `GET /api/incidents` - List incidents
- `GET /api/incidents/{id}` - Incident details
- `POST /api/incidents/simulate` - Create test incident

---

## 📚 Additional Resources

- **Main Documentation:** `../README.md`
- **Retool Setup Guide:** `RETOOL_SETUP.md`
- **API Documentation:** http://localhost:8000/docs
- **Retool Docs:** https://docs.retool.com

---

## 💡 Pro Tips

1. **Run both dashboards simultaneously** - they work side by side
2. **Use Retool for stakeholder demos** - looks more polished
3. **Use HTML for development** - faster iteration
4. **Enable CORS** if hosting separately from API
5. **Use ngrok** to share demos publicly

---

## 🆘 Troubleshooting

**Dashboard won't load:**
- Ensure API is running: `python main.py --mode server`
- Check port 8000 is available
- Look at browser console for errors

**Retool can't connect:**
- API must be publicly accessible (use ngrok for localhost)
- Check CORS settings
- Verify API URL in Retool resource config

**No data showing:**
- Simulate an incident first
- Check API endpoints: http://localhost:8000/docs
- Verify queries are running in Retool

---

**Made with ❤️ for the Anthropic Hackathon**

*Built to showcase multi-agent systems with guardrails in incident response automation.*

