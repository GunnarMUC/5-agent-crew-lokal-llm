[![CI](https://github.com/GunnarMUC/5-agent-crew-lokal-llm/actions/workflows/ci.yml/badge.svg)](https://github.com/GunnarMUC/5-agent-crew-lokal-llm/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](LICENSE)n

# Instagram 5-Agenten CrewAI – Lokal & Autonom 🚀


**Autonomes 5-Agenten-Team für 24/7 Instagram-Content** – **100% lokal** mit CrewAI + Ollama (Qwen2.5 14B). Keine Cloud, keine Kosten, datenschutzkonform. Läuft stabil auf Apple Silicon (24GB+ RAM).

Perfekt für **Marketing-Agenturen, Freelancer & Studios**.

## 🎯 Features
- **5 Spezialisierte Agenten**: Supervisor, Trend Scout, Idea Generator, Caption Writer, Hashtag Specialist, Reviewer
- **Infinite Loop Mode**: Stündlich/neuer Post (CLI: `--loop -1`)
- **Auto-Logging**: `instagram_content_log.md` mit Timestamps
- **Configurable**: `.env` für Model/Interval, CLI Args
- **Proven**: 10h+ Endurance (60 Runs @10min)
- **Lightweight**: ~5-10min pro Post

## ⚡ Schnellstart (macOS/Apple Silicon)

```bash
# 1. Ollama Setup
brew install ollama && brew services start ollama
ollama pull qwen2.5:14b-instruct-q4_K_M  # or llama3.2:3b

# 2. Clone & Install
git clone https://github.com/GunnarMUC/5-agent-crew-lokal-llm.git
cd 5-agent-crew-lokal-llm
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit if needed

# 3. Run
python instagram_agent_crew.py --loop 1  # Single run
python instagram_agent_crew.py --loop -1 --interval 60  # Infinite hourly
```

**Test Output**: Check `instagram_content_log.md` – ready-to-post captions! 📱

## 🛠 Tech Stack
- **CrewAI**: Agent Orchestration
- **Ollama + Qwen2.5 14B**: Local LLM (MLX-accelerated)
- **Vanilla Python**: No bloat

## 📁 Example Output
![Screenshot](https://via.placeholder.com/800x400?text=Instagram+Post+Sample)  <!-- Add real GIF -->

```
## 15.10.2024 – 14:30
**Thema:** AI Marketing Trends
**Finaler Post:** 🚀 AI revolutioniert Marketing! Trends: Personalisierte Ads, Voice-Suche. Welchen testest du? #AIMarketing #Trends2024
```

## 🚀 Usage
```bash
python instagram_agent_crew.py --help
# --loop N: Runs (default 1, -1 infinite)
# --interval M: Min between (default 10)
# --topic "Dein Thema"
```

## 💡 Tips
- **RAM**: 24GB+ recommended
- **Models**: qwen2.5:14b > llama3.2:3b (faster)
- **Extend**: Add image gen (DALL-E local?)

## 🤝 Contribute
Issues/PRs welcome! Star if useful. ⭐

**Apache 2.0** – Free to use/extend.
