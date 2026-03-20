<h1>Incident Autopilot - Agentic Incident Response System</h1>

<p>
<strong>Incident Autopilot</strong> is a <strong>multi-agent, human-in-the-loop incident response system</strong>
that simulates how modern SRE and platform teams
<strong>detect, analyze, and mitigate production incidents</strong>.
</p>
<h3>Live Demo</h3>
<p>
<a href="https://incident-autopilot.onrender.com/" target="_blank">
https://incident-autopilot.onrender.com/
</a>
</p>

<p>
Instead of a monolithic workflow, the system orchestrates
<strong>specialized agents</strong>, each responsible for a distinct stage of
incident handling while enforcing <strong>safety guardrails</strong> and enabling
<strong>human approval</strong> for risky actions.
</p>

<hr/>

<h2>Problem Statement</h2>

<p>
Real-world incident response is not a single decision it is a sequence of
reasoning steps involving evidence, safety checks, and human judgment.
Most tooling today focuses on dashboards rather than decision-making systems.
</p>

<p>
<strong>Incident Autopilot</strong> models incident response as an
<strong>agentic workflow</strong>, where agents reason, validate actions,
and coordinate safely with humans.
</p>

<hr/>

<h2>Key Features</h2>

<ul>
  <li><strong>Agentic architecture</strong> each incident stage handled by a dedicated agent</li>
  <li><strong>Evidence-driven reasoning</strong> using metrics, logs, deploy history, and runbooks</li>
  <li><strong>Guardrails engine</strong> to prevent unsafe or irreversible actions</li>
  <li><strong>Human-in-the-loop approval</strong> for high-risk mitigations</li>
  <li><strong>Asynchronous orchestration</strong> with FastAPI background tasks</li>
  <li><strong>Live dashboard</strong> for incident timelines and status</li>
  <li><strong>Pluggable intelligence</strong> (rule-based today, LLM-ready)</li>
  <li><strong>Deterministic incident simulator</strong> — no real infra required</li>
</ul>

<hr/>

<h2>System Architecture</h2>

<pre>
Incident Detected
      ↓
┌──────────┐
│  Scout   │  → Collects metrics, logs, deploys, runbooks
└──────────┘
      ↓
┌──────────┐
│  Triage  │  → Classifies incident type (latency, errors, saturation)
└──────────┘
      ↓
┌────────────┐
│ Hypothesis │  → Generates possible root causes
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
│ Postcheck │  → Verifies recovery & generates report
└───────────┘
</pre>

<hr/>

<h2>Agents Overview</h2>

<table border="1" cellpadding="6" cellspacing="0">
  <tr>
    <th>Agent</th>
    <th>Responsibility</th>
  </tr>
  <tr>
    <td><strong>Scout</strong></td>
    <td>Collects metrics, logs, deploy history, and runbooks</td>
  </tr>
  <tr>
    <td><strong>Triage</strong></td>
    <td>Classifies incident type and severity using evidence and runbooks (LLM-assisted root cause reasoning with deterministic fallback)</td>
  </tr>
  <tr>
    <td><strong>Hypothesis</strong></td>
    <td>Generates and ranks root-cause hypotheses (LLM-assisted root cause reasoning with deterministic fallback)</td>
  </tr>
  <tr>
    <td><strong>Experiment</strong></td>
    <td>Validates hypotheses against collected evidence</td>
  </tr>
  <tr>
    <td><strong>Executor</strong></td>
    <td>Proposes and applies mitigations under strict guardrails</td>
  </tr>
  <tr>
    <td><strong>Postcheck</strong></td>
    <td>Verifies recovery and generates the final incident report</td>
  </tr>
</table>

<hr/>


<hr/>

<h2>Safety & Guardrails</h2>

<p>
The system never blindly executes actions. Guardrails ensure:
</p>

<ul>
  <li>Only <strong>reversible mitigations</strong> are allowed</li>
  <li><strong>Production actions require human approval</strong></li>
  <li>Scaling limits and risk thresholds are enforced</li>
</ul>

<p>
This mirrors real-world SRE safety practices.
</p>

<hr/>

<h2>Human-in-the-Loop Workflow</h2>

<ol>
  <li>System proposes a mitigation</li>
  <li>Guardrails evaluate safety</li>
  <li>Human approves via API or dashboard</li>
  <li>Mitigation is applied</li>
  <li>Postcheck verifies recovery</li>
  <li>Incident marked <strong>COMPLETED</strong> or <strong>FAILED</strong></li>
</ol>

<hr/>

<h2>Running the Project</h2>

<h3>Local</h3>

<pre>
pip install -r requirements.txt
uvicorn api:app --reload
</pre>

<ul>
  <li>Dashboard: <code>http://localhost:8000</code></li>
  <li>API Docs: <code>http://localhost:8000/docs</code></li>
</ul>
<hr/>
