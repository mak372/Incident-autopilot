# Reliable buddy

**Agentic Orchestration Hackathon 2026 Submission**

An intelligent multi-agent system that automatically detects, diagnoses, and mitigates incidents in microservices/K8s applications **5x faster than manual response** (45s vs 45min).

---

## ⚡ Quick Setup (3 Steps)

```bash
# 1. Clone the repository
git clone https://github.com/tahsinsoha/Hackathon-Project--Agentic-Orchestration.git
cd Hackathon-Project--Agentic-Orchestration

# 2. Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Run it!
python3 main.py --mode demo --incident-type latency_spike
```

**Or start the web dashboard:**
```bash
python3 main.py --mode server
# Then open: http://localhost:8000
```
.


   
   See [dashboard/README.md](dashboard/README.md) for details on both options!

📖 **Detailed setup guide:** See [INSTALL.md](INSTALL.md)

---

## 🎯 What Makes This Unique

Most incident tools just **detect and page**
**Detect → Diagnose → Mitigate → Verify → Summarize**

## 🤖 Multi-Agent Pipeline

```
📊 Anomaly Detected (metric threshold breach)
    ↓
🔍 Scout Agent (pulls evidence: metrics, logs, traces, deploys)
    ↓
🏥 Triage Agent (classifies: deploy regression vs infra vs dependency)
    ↓
💡 Hypothesis Agent (proposes 2-3 root causes + validation criteria)
    ↓
🧪 Experiment Agent (runs checks: canary comparison, correlation analysis)
    ↓
⚡ Executor Agent (applies guarded mitigation: rollback/scale/feature-flag)
    ↓
✅ Postcheck Agent (verifies recovery + generates incident report)
```

## 📊 What We Monitor

- **Latency spikes** (p95/p99)
- **Error rate increases**
- **CPU/Memory saturation**
- **Queue depth growth**

## 🛡️ Guardrails

- **Human approval** for critical actions
- **Reversible-only** mitigations
- **Impact limits** (max scale, canary %)
- **Circuit breakers** (auto-rollback if metrics worsen)
- **Audit trail** of all actions

## 🎨 Sponsor Tool Integration

| Tool | Purpose | Implementation |
|------|---------|----------------|
| **Retool** | Incident Control Tower UI (alerts, approvals, history) | Full dashboard with real-time data, approval workflows, and timeline visualization. See `dashboard/retool_dashboard.json` |
| **TinyFish**| Scout agent for pulling runbooks/docs from web | Web scraping for incident documentation |
| **Tonic** | Generate realistic incident datasets for reliable demos | Synthetic data generation for testing |
| **Freepik** | Generate incident card visuals & timeline graphics | Visual assets for reports |

## 📈 Metrics We Track

- **Detection Latency** (seconds from anomaly to alert)
- **Triage Accuracy** (% correct incident classification)
- **Time-to-Mitigation** (end-to-end resolution time)
- **Success Rate** (% of successful mitigations)
- **False Positive Rate** (incorrect alerts)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Start backend server
python main.py

# Open dashboard
open http://localhost:8000

# Run simulation
python simulate_incident.py --type latency_spike
```

## 🏗️ Architecture

```
Backend (FastAPI + Multi-Agent System)
    ├── Incident Simulator (Tonic-powered)
    ├── Agent Orchestrator (LLM-based agents)
    ├── Guardrail Engine (safety policies)
    ├── Metrics Store (time-series data)
    └── Audit Log (full history)

Frontend (Retool + Web Dashboard)
    ├── Control Tower (alerts & approvals)
    ├── Evidence Viewer (metrics, logs, traces)
    ├── Timeline Visualizer (incident progression)
    └── Postmortem Generator (Freepik graphics)
```

## 🎮 Demo Scenarios

1. **Latency Spike**: p99 jumps from 200ms → 5s after deploy
2. **Error Rate Surge**: 0.1% → 15% errors from downstream dependency
3. **Memory Leak**: Gradual OOM leading to pod restarts
4. **Queue Backlog**: Message queue depth growing exponentially

## 📁 Project Structure

```
incident-autopilot/
├── agents/               # Individual agent implementations
│   ├── scout.py
│   ├── triage.py
│   ├── hypothesis.py
│   ├── experiment.py
│   ├── executor.py
│   └── postcheck.py
├── core/                 # Core orchestration
│   ├── pipeline.py
│   ├── guardrails.py
│   └── state.py
├── simulator/            # Incident generation
│   ├── metrics_generator.py
│   ├── log_generator.py
│   └── scenarios.py
├── integrations/         # Sponsor tool APIs
│   ├── retool.py
│   ├── tinyfish.py
│   ├── tonic.py
│   └── freepik.py
├── dashboard/            # Frontend
│   ├── index.html
│   ├── static/
│   └── retool_config.json
├── api.py               # FastAPI REST API
├── main.py              # Entry point
└── simulate_incident.py # CLI simulator
```

## 🏆 Hackathon Submission Highlights

- ✅ **3+ Sponsor Tools**: Retool, TinyFish, Tonic, Freepik
- ✅ **Full Autonomy**: End-to-end incident resolution with guardrails
- ✅ **Shippable Product**: Real API, UI, simulation, metrics
- ✅ **Multi-Agent**: Clear orchestration with specialized agents
- ✅ **Safety First**: Guardrails prevent dangerous actions

