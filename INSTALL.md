# 🚀 Installation Guide

Complete setup instructions for running Incident Autopilot on your machine.

---

## Prerequisites

- **Python 3.10 or higher** (Python 3.13 recommended)
- **pip** (Python package manager)
- **git** (to clone the repository)

### Check Your Python Version

```bash
python3 --version
# Should show: Python 3.10.x or higher
```

If you don't have Python 3.10+, download it from: https://www.python.org/downloads/

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/tahsinsoha/Hackathon-Project--Agentic-Orchestration.git
cd Hackathon-Project--Agentic-Orchestration
```

---

## Step 2: Create a Virtual Environment

**Why?** This keeps the project dependencies isolated from your system Python.

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**You should see `(venv)` at the start of your terminal prompt.**

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages:
- FastAPI & Uvicorn (web server)
- Pydantic (data validation)
- Anthropic & OpenAI (AI integrations - optional)
- NumPy & Pandas (data processing)
- And more...

**Installation time:** 1-2 minutes

---

## Step 4: Run the Application

### Option A: CLI Demo (Quick Test)

Run a single incident simulation in your terminal:

```bash
python3 main.py --mode demo --incident-type latency_spike
```

**What you'll see:**
- Incident details
- 6 agents working in sequence
- Mitigation applied
- Recovery verified
- Complete incident report

**Try other incident types:**
```bash
python3 main.py --mode demo --incident-type error_rate
python3 main.py --mode demo --incident-type resource_saturation
python3 main.py --mode demo --incident-type queue_depth
```

### Option B: Web Dashboard (Recommended)

Start the web server with interactive UI:

```bash
python3 main.py --mode server
```

Then open your browser to:
```
http://localhost:8000
```

**Dashboard features:**
- 📊 Real-time statistics
- 🎮 Interactive incident simulation
- 📋 Incident history
- ⏱️ Live agent timeline

---

## Step 5: Explore the API (Optional)

With the server running, visit:

**Interactive API Documentation:**
```
http://localhost:8000/docs
```

**API Examples:**

```bash
# Simulate an incident via API
curl -X POST "http://localhost:8000/api/incidents/simulate?incident_type=latency_spike"

# List all incidents
curl "http://localhost:8000/api/incidents"

# Get statistics
curl "http://localhost:8000/api/statistics"
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pydantic'"

**Solution:** Make sure you activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "python3: command not found"

**Solution:** Try `python` instead of `python3`:
```bash
python main.py --mode demo
```

### Issue: "Address already in use" (Port 8000 busy)

**Solution:** Use a different port:
```bash
python3 main.py --mode server --port 8080
```
Then visit: http://localhost:8080

### Issue: Build errors with pydantic-core on Python 3.13

**Solution:** This is already fixed in requirements.txt with `pydantic>=2.10.0`

If you still have issues, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: Permission denied when installing packages

**Solution:** Make sure you're in the virtual environment:
```bash
# Should see (venv) in prompt
which python
# Should point to: .../venv/bin/python
```

---

## Configuration (Optional)

The system works out-of-the-box with no API keys needed! 

However, if you want to use real AI models instead of rule-based fallbacks:

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```bash
# AI Providers (optional)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Sponsor Tools (optional - stubs work without keys)
RETOOL_API_KEY=your_key
TINYFISH_API_KEY=your_key
TONIC_API_KEY=your_key
FREEPIK_API_KEY=your_key
```

**Note:** The demo works perfectly without any API keys using simulated responses!

---

## Verifying Installation

Run this quick test:

```bash
python3 main.py --mode demo --incident-type latency_spike
```

**Expected output:**
```
🚨 INCIDENT AUTOPILOT WITH GUARDRAILS - Demo Mode
==================================================================

📋 Incident Details:
   ID: inc-20260116-123456
   Service: api-service
   Severity: high

🔍 [SCOUT] Gathering evidence...
   ✓ Collected 4 log entries, found 1 recent deploys
🏥 [TRIAGE] Classifying incident type...
   ✓ Type: latency_spike (confidence: 90%)
💡 [HYPOTHESIS] Generating root cause hypotheses...
   ✓ Generated 3 hypotheses
🧪 [EXPERIMENT] Validating hypotheses...
   ✓ Validated 3/3 hypotheses
⚡ [EXECUTOR] Proposing mitigation...
   ✅ Mitigation applied successfully
✅ [POSTCHECK] Verifying recovery...
   ✅ Metrics recovered successfully

✅ INCIDENT PIPELINE COMPLETED
Time to mitigation: 45.3s
Success: True
```

If you see this, **installation is successful!** ✅

---

## Quick Command Reference

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run CLI demo
python3 main.py --mode demo --incident-type latency_spike

# Start web server
python3 main.py --mode server

# Run on different port
python3 main.py --mode server --port 8080

# Deactivate virtual environment
deactivate
```

---

## System Requirements

- **OS:** macOS, Linux, or Windows
- **Python:** 3.10+ (tested on 3.10, 3.11, 3.12, 3.13)
- **RAM:** 2GB minimum, 4GB recommended
- **Disk:** 500MB for dependencies
- **Network:** Only needed for installing packages (runtime works offline)

---

## What Gets Installed

Dependencies breakdown:

| Package | Purpose | Size |
|---------|---------|------|
| fastapi, uvicorn | Web server & API | ~20MB |
| pydantic | Data validation | ~5MB |
| anthropic, openai | AI integrations (optional) | ~10MB |
| numpy, pandas | Data processing | ~50MB |
| aiohttp | Async HTTP | ~5MB |
| Others | Various utilities | ~10MB |

**Total:** ~100MB

---

## Next Steps

After installation:

1. ✅ Read `START_HERE.md` for project overview
2. ✅ Read `QUICK_START.md` for 2-minute demo guide
3. ✅ Try different incident scenarios
4. ✅ Explore the web dashboard
5. ✅ Check out the code in `agents/` and `core/`

---

## Need Help?

- 📖 **Documentation:** Check `START_HERE.md` and `README.md`
- 🐛 **Issues:** Open an issue on GitHub
- 💬 **Questions:** See `SETUP_GUIDE.md` for detailed explanations

---

## Success! 🎉

You're ready to run Incident Autopilot. Start with:

```bash
python3 main.py --mode demo --incident-type latency_spike
```

Or for the web dashboard:

```bash
python3 main.py --mode server
```

Then open: http://localhost:8000

Enjoy! 🚀

