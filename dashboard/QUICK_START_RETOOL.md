# ⚡ Retool Dashboard - Quick Start Card

**5-Minute Setup Guide**

## 🎯 Step 1: Start Your API

```bash
cd incident-autopilot
python main.py --mode server
```

✅ API running at: `http://localhost:8000`

---

## 🎯 Step 2: Get Retool Account

1. Visit: https://retool.com
2. Sign up (free tier is fine)
3. Create workspace

---

## 🎯 Step 3: Import Dashboard

1. In Retool, click **"Create new"**
2. Select **"From JSON/YAML"**
3. Upload: `dashboard/retool_dashboard.json`
4. Name: "Incident Autopilot Dashboard"

---

## 🎯 Step 4: Configure API

1. Go to **Resources** (left sidebar)
2. Edit "Incident Autopilot API"
3. Update Base URL:
   - Local: `http://localhost:8000/api`
   - Remote: Use ngrok (see below)

### Using ngrok for Remote Access
```bash
# Install: https://ngrok.com
ngrok http 8000

# Copy the https URL (e.g., https://abc123.ngrok.io)
# Use in Retool: https://abc123.ngrok.io/api
```

---

## 🎯 Step 5: Test & Publish

1. Click each query in bottom panel
2. Click **"Run"** to test
3. Verify data appears
4. Click **"Release"** (top right)

---

## ✅ Done!

Your dashboard is live at:
`https://[your-workspace].retool.com/apps/incident-autopilot`

---

## 🎬 Demo Script (2 Minutes)

### Opening (15 seconds)
> "This is our Incident Autopilot dashboard built with Retool, showing real-time incident response."

### Statistics (15 seconds)
> "These metrics update every 5 seconds - detection latency, mitigation time, and success rate."

### Simulate (30 seconds)
1. Select "Latency Spike"
2. Click **"🚀 Simulate Incident"**
3. > "Watch our multi-agent system work in real-time"

### Timeline (45 seconds)
1. Click the new incident
2. Scroll through timeline
3. > "Each agent - Scout, Triage, Hypothesis, Experiment, Executor - makes decisions with guardrails"

### Closing (15 seconds)
> "Built with Retool for enterprise features: auth, workflows, mobile support. Production-ready today."

---

## 🆘 Troubleshooting

**Dashboard won't load data?**
- Check API is running: `curl http://localhost:8000/api/statistics`
- Verify resource URL in Retool
- Check browser console for errors

**Can't connect to localhost?**
- Use ngrok: `ngrok http 8000`
- Update Retool resource with ngrok URL
- Or deploy API to cloud

**Queries failing?**
- Test resource connection in Retool
- Check endpoint paths
- Verify API is accessible

---

## 📊 Dashboard Features

✅ Real-time statistics (4 metrics)
✅ Interactive incident table
✅ Timeline with agent actions
✅ One-click simulation
✅ Auto-refresh (5 seconds)
✅ Color-coded severity badges
✅ Mobile responsive
✅ Approval workflow ready

---

## 🔗 Quick Links

- **Full Setup Guide:** [RETOOL_SETUP.md](RETOOL_SETUP.md)
- **Demo Guide:** [RETOOL_DEMO_GUIDE.md](RETOOL_DEMO_GUIDE.md)
- **Integration Summary:** [RETOOL_INTEGRATION_SUMMARY.md](RETOOL_INTEGRATION_SUMMARY.md)
- **API Docs:** http://localhost:8000/docs

---

## 💡 Pro Tips

1. **Practice the demo** - Run through it 2-3 times
2. **Have backup ready** - Keep HTML dashboard available
3. **Use mobile view** - Show Retool's mobile app if possible
4. **Explain the value** - Highlight enterprise features
5. **Show the JSON** - Prove it's a real integration

---

## 🎪 What Makes This Special

✅ **Not a mockup** - Real Retool app
✅ **Importable** - Anyone can use the JSON
✅ **Production-ready** - Enterprise features included
✅ **Well-documented** - Complete guides provided
✅ **Demo-ready** - Works out of the box

---

## 📱 Mobile Demo (Bonus)

If you have Retool mobile app:
1. Download Retool app on phone
2. Log in to your workspace
3. Open Incident Autopilot dashboard
4. Show it works on mobile!

> "Our on-call engineers can approve mitigations from their phone at 2 AM."

---

## 🎯 Key Message

> "We integrated with Retool to provide an enterprise-grade UI for our multi-agent incident response system. It connects to our Python API in real-time, shows agents working with guardrails, and includes approval workflows. This is production-ready today."

---

**Time from zero to working dashboard: 5 minutes** ⚡

**Good luck! 🚀**

---

## 📋 Pre-Demo Checklist

- [ ] API running
- [ ] Retool dashboard imported
- [ ] API URL configured
- [ ] All queries tested
- [ ] Dashboard published
- [ ] Demo script practiced
- [ ] Backup plan ready
- [ ] Laptop charged
- [ ] Internet working

---

**You've got this! Show them what you built! 💪**

