# 🔑 API Keys Setup Guide

## Quick Setup

Create a `.env` file in the project root:

```bash
touch .env
```

Then add your API keys:

```bash
# REQUIRED: At least 3 for hackathon

# Anthropic Claude (AI-powered agents)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Retool (Approval workflows)
RETOOL_API_KEY=your-retool-key-here
RETOOL_WORKFLOW_ID=incident-approval

# Tonic AI (Synthetic data)
TONIC_API_KEY=your-tonic-key-here

# Freepik (AI visuals)
FREEPIK_API_KEY=your-freepik-key-here

# TinyFish (Web scraping)
TINYFISH_API_KEY=your-tinyfish-key-here
```

---

## ✅ Which APIs Are Actually Used?

### **1. Anthropic (ACTIVE)**
- **Used in:** `agents/triage.py`
- **Purpose:** AI-powered incident classification
- **Fallback:** Rule-based classification if no key
- **How to get:** https://console.anthropic.com/

### **2. Retool (ACTIVE)**
- **Used in:** `integrations/retool.py` 
- **Purpose:** Sends approval requests for mitigations
- **Fallback:** Prints to console if no key
- **How to get:** https://retool.com/

### **3. Tonic AI (ACTIVE)**
- **Used in:** `integrations/tonic.py`
- **Purpose:** Generate synthetic test metrics
- **Fallback:** Local random generation if no key
- **How to get:** From hackathon booth or https://tonic.ai/

### **4. Freepik (ACTIVE)**
- **Used in:** `integrations/freepik.py`
- **Purpose:** AI-generated incident card visuals
- **Fallback:** Returns placeholder URLs if no key
- **How to get:** https://www.freepik.com/api

---

## 🎯 Recommended for Hackathon Demo

**Use these 3 (easiest to showcase):**

1. ✅ **Anthropic** - Visible in agent decisions
2. ✅ **Retool** - Visible in approval workflow
3. ✅ **Freepik** - Visible in generated images

---

## 🚀 Testing API Integration

After adding keys, test each one:

```bash
# Test Anthropic
python3 -c "import os; from anthropic import Anthropic; print('✅ Anthropic works!' if os.getenv('ANTHROPIC_API_KEY') else '❌ No key')"

# Run full demo to see APIs in action
python3 main.py --mode demo --incident-type latency_spike
```

**Look for these log messages:**
- `[TRIAGE] ✅ Using Anthropic Claude for classification`
- `[RETOOL] ✅ Approval request sent successfully`
- `[FREEPIK] ✅ Generated incident card`

---

## ⚠️ Important Notes

1. **System works WITHOUT keys** - Uses smart fallbacks
2. **Keys are optional** - But needed for hackathon judging
3. **Never commit .env** - Already in .gitignore
4. **Free tiers available** - Check each service

---

## 🔒 Security

- `.env` is in `.gitignore` - won't be pushed to GitHub
- Keys are loaded via `os.getenv()` - secure
- Fallbacks protect against API failures

---

## 📝 Example .env File

```bash
# Copy and paste this, then fill in your actual keys
ANTHROPIC_API_KEY=sk-ant-api03-xxx
RETOOL_API_KEY=retool_xxx  
RETOOL_WORKFLOW_ID=incident-approval
TONIC_API_KEY=tonic_xxx
FREEPIK_API_KEY=freepik_xxx
```

---

**Done!** Run `python3 main.py --mode demo` and the system will automatically use any available API keys. 🚀

