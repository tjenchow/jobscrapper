# 🤖 JobAgent — Local AI Job Search Agent

A Python CLI tool that fetches remote job listings via **official public APIs**, scores them using a local AI model (via [Ollama](https://ollama.com)), and sends you a weekly email digest — running **100% offline** on your machine.

Built as a learning project to practice Python while solving a real problem: finding backend & Laravel freelance work faster.

> **Note on data sources:** This project uses only official, publicly documented APIs — not HTML scraping. Job data from [RemoteOK](https://remoteok.com) is fetched via their [official JSON API](https://remoteok.com/api) in compliance with their [Terms of Service](https://remoteok.com/legal).

---

## ✨ Features

- 🔍 **Fetches jobs via official APIs** — uses RemoteOK's public JSON API (no HTML scraping)
- 🧠 **AI-powered scoring** — uses a local LLM (phi3-mini via Ollama) to score each job 1–10 based on your skills
- 🚫 **Deduplication** — remembers seen jobs so you never get the same listing twice
- 📧 **Email digest** — sends a ranked summary of the best matches every Monday morning
- 🔒 **100% local & private** — no cloud API keys needed, everything runs on your machine
- ⚙️ **Fully configurable** — edit `config.json` and `skills.json` to match your profile

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11 |
| Data source | RemoteOK official JSON API |
| HTTP client | `requests` |
| AI model | Ollama (`phi3:mini`) |
| Email | `smtplib` (built-in) |
| Scheduling | `APScheduler` or system `cron` |
| Storage | JSON files |

---

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.11+** — check with `python3 --version`
- **Ollama** installed and running — [ollama.com](https://ollama.com)
- **phi3-mini model** pulled — `ollama pull phi3:mini`
- **Gmail account** with an [App Password](https://myaccount.google.com/apppasswords) set up (for email sending)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tjenchow/jobscrapper.git
cd jobscrapper
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your profile

Copy the example config files and fill in your details:

```bash
cp config.example.json config.json
cp skills.example.json skills.json
```

Edit `config.json`:

```json
{
  "email_to": "you@gmail.com",
  "email_from": "yourbot@gmail.com",
  "email_pass": "your-gmail-app-password",
  "keywords": ["laravel", "python", "backend", "api", "php"],
  "min_score": 6,
  "max_jobs": 10
}
```

Edit `skills.json` to match your actual skills:

```json
{
  "languages": ["PHP", "Python", "SQL", "JavaScript"],
  "frameworks": ["Laravel", "FastAPI", "Django"],
  "tools": ["MySQL", "PostgreSQL", "Redis", "Docker", "Git"],
  "years_exp": 3,
  "prefer": "backend",
  "available_hours": "part-time"
}
```

### 5. Run it

```bash
python main.py
```

---

## 📁 Project Structure

```
job_agent/
├── main.py              # Entry point — orchestrates the full pipeline
├── scraper.py           # Fetches job listings from web sources
├── ai_scorer.py         # Sends jobs to Ollama, gets relevance score + reason
├── storage.py           # Loads config, manages seen-jobs deduplication
├── mailer.py            # Formats and sends the email digest
├── config.json          # Your personal settings (gitignored)
├── skills.json          # Your skills for AI matching (gitignored)
├── seen_jobs.json       # Auto-generated dedup store (gitignored)
├── config.example.json  # Safe example config to commit
├── skills.example.json  # Safe example skills to commit
└── requirements.txt     # Python dependencies
```

---

## ⚙️ How It Works

```
1. scraper.py    →  Calls RemoteOK's official public JSON API
2. storage.py    →  Filters out jobs already seen in previous runs
3. ai_scorer.py  →  Asks local Ollama (phi3-mini) to score each job 1–10
4. main.py       →  Sorts by score, filters by min_score threshold
5. mailer.py     →  Sends the top N results as an email digest
6. storage.py    →  Saves newly seen job URLs to avoid future duplicates
```

---

## 🗓️ Scheduling (run every Monday automatically)

**Option A — system cron (simplest):**

```bash
crontab -e
```

Add this line (update the paths to match your machine):

```
0 8 * * 1 /path/to/job_agent/venv/bin/python /path/to/job_agent/main.py
```

**Option B — APScheduler (Python-native):**

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from main import run

scheduler = BlockingScheduler()

@scheduler.scheduled_job("cron", day_of_week="mon", hour=8)
def weekly_run():
    run()

scheduler.start()
```

---

## ⚖️ API Usage & Attribution

This project fetches job data from the **RemoteOK public JSON API** (`https://remoteok.com/api`).

### Why the official API and not scraping?

| | HTML scraping | Official API (this project) |
|---|---|---|
| Allowed by ToS | grey area | yes |
| Breaks on redesign | yes | no |
| Rate limit risk | high | low |
| Salary data included | no | yes |
| Ethical | debatable | yes |

### RemoteOK API terms

Per [RemoteOK's Terms of Service](https://remoteok.com/legal), when using data from their API you agree to:

- **Link back** to [remoteok.com](https://remoteok.com) on any page or screen where the job data is displayed.

This project is a **personal tool** — the email digest is sent only to yourself. If you ever build a public-facing UI on top of this project, add a visible "Jobs from [RemoteOK](https://remoteok.com)" attribution link.

### Responsible API usage

The code follows these practices to be a good API citizen:

- Descriptive `User-Agent` header: `JobAgent/1.0 (personal job search tool)`
- Requests made at most once per scheduled run (weekly by default)
- No credential bypassing, no pagination abuse, no parallel flooding

---

## 🔐 Environment & Security

- **Never commit** `config.json` — it contains your email password
- **Never commit** `seen_jobs.json` — it's auto-generated state
- Both are already listed in `.gitignore`
- Use a [Gmail App Password](https://myaccount.google.com/apppasswords), not your real Gmail password

---

## 🗺️ Roadmap

- [x] Fetch RemoteOK listings via official public API
- [x] AI scoring with local Ollama model
- [x] Email digest with ranked results
- [x] Deduplication across runs
- [ ] Add more job sources (We Work Remotely, Remotive)
- [ ] Add a web UI dashboard to browse results
- [ ] Export results to CSV
- [ ] Slack / Telegram notification option
- [ ] Docker support for easier deployment

---

## 🐍 Learning Notes

This project was built to learn Python coming from a PHP/Laravel background. Key concepts covered:

- Virtual environments (`venv`) — equivalent to Composer's `vendor/`
- Dicts and lists — equivalent to PHP associative and indexed arrays
- `requests` library — equivalent to Guzzle HTTP
- `json` module — equivalent to `json_encode()` / `json_decode()`
- `try/except` — equivalent to `try/catch`
- List comprehensions — equivalent to `array_filter()` + `array_map()`
- f-strings — equivalent to PHP string interpolation `"Hello {$name}"`
- Modules and imports — equivalent to Laravel's service classes
- `if __name__ == "__main__"` — equivalent to Laravel's `artisan` entry point

---

## 👤 Author

**Fyanco**  
Full-stack web developer (Laravel / PHP) learning Python backend development.

- GitHub: [@tjenchow](https://github.com/tjenchow)
- LinkedIn: [your-linkedin](https://linkedin.com/in/fyanco-tjen)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).