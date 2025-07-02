# 🔒 Sec-Fix Agents – Automated Java Dependency Vulnerability Fixer

This tool uses [CrewAI](https://github.com/joaomdmoura/crewai) agents to **scan a GitHub repo, detect vulnerable Maven dependencies, auto-fix them by upgrading versions, and open a pull request** – all in one shot.

> 🧠 _Part of my developer automation series at_ [**blog.slayitcoder.in**](https://blog.slayitcoder.in)  
> 📰 _Subscribe to_ [**SlayItCoder Weekly**](https://slayitcoder.substack.com) _for dev productivity insights._

---

## 🧠 Agentic Flow

1. 🔍 **Security Scanner** – Detects vulnerabilities using Snyk  
2. 🛠 **Dependency Fixer** – Selects safe upgrade versions  
3. 📦 **PR Creator** – Patches `pom.xml`, creates a branch, commits, and opens a PR  

---

## ✨ Demo

📺 [Watch the full demo on YouTube](https://youtu.be/8D0iM1ZcmaM)

---

## 🚀 Quick Start

### 1️⃣ Clone & Set Up

```bash
git clone https://github.com/tpushkarsingh/sec-fix-agents.git
cd sec-fix-agents
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Add Your .env
Create a .env file in the root directory with the following:
```bash
OPENAI_API_KEY=your-openai-key
GITHUB_TOKEN=your-github-pat
REPO_TO_SCAN=https://github.com/tpushkarsingh/auth-server
CREWAI_MODEL=gpt-3.5-turbo-0125
CREWAI_TEMPERATURE=0.2
```
🔑 GitHub token must have repo and pull_request scopes
🛡️ Snyk CLI must be installed and authenticated (snyk auth)
### 3️⃣ Run the Bot
python run_bot.py
If successful, you’ll see output like:
```bash
✓ Clone success  
✓ Vulnerabilities found via Snyk  
✓ Suggested upgrades: spring-security-core → 5.8.9, ...  
✓ Branch created: ai/sec-fix-bot-YYYYMMDD-HHMMSS  
✓ Pull request opened: https://github.com/tpushkarsingh/auth-server/pull/123
``` 
---
### 📁 Project Structure

sec-fix-agents/
├── agents/
│   ├── pr_agent.py
│   ├── scan_agent.py
│   └── fix_agent.py
├── helpers/
│   ├── pom_tools.py
│   └── snyk_parser.py
├── run_bot.py
├── .env.example
├── .gitignore
└── requirements.txt

---
### 📚 More from the Author

> 📝 Blog: https://blog.slayitcoder.in
> 📨 Newsletter: https://slayitcoder.substack.com
> 🧑‍💻 Built with ❤️ by Pushkar Singh
