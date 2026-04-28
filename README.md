# ⚡ Reelioo — Agentic Crypto Intelligence

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.2-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/GPT--4o--mini-OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![Binance](https://img.shields.io/badge/Binance-Live%20Data-F0B90B?style=flat-square&logo=binance&logoColor=black)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)

> A crypto analysis agent powered by LangChain and GPT-4o-mini. Ask about any coin in plain English — Reelioo pulls live Binance data, calculates Mass and Velocity scores, and returns a clear **BUY / WAIT / AVOID** signal.

---

![Reelioo Hero](screenshots/hero.png)

---

## What It Does

```
You:     Analyse BTC right now

Reelioo: SIGNAL      ▲ BUY
         CONFIDENCE  78%
         MASS        62/100 — MODERATE — OK volume
         VELOCITY    81/100 — HIGH — Strong momentum

         REASONING
         BTC is showing strong upward velocity with moderate volume support.
         No Vacuum Trap detected. Price action above key resistance confirms
         momentum. Momentum favours buyers at this level.
```

The agent **remembers your conversation** — ask follow-up questions and it keeps full context across the session.

---

## Mobile

<img src="screenshots/mobile.png" width="390" alt="Reelioo on mobile" />

---

## How It Works

Reelioo runs a LangChain agent loop with 3 live Binance tools:

```
User asks about BTC
        │
        ▼
Agent calls get_crypto_price("BTC")      → live price, 24h change, high/low, volume
        │
        ▼
Agent calls get_market_momentum("BTC")   → Velocity score 0–100, direction
        │
        ▼
Agent calls get_volume_analysis("BTC")   → Mass score 0–100, Vacuum Trap check
        │
        ▼
GPT-4o-mini reasons over all 3 results
        │
        ▼
Returns: SIGNAL · CONFIDENCE · MASS · VELOCITY · REASONING
```

**Thread ID + Flask session** keeps conversation context alive — the agent remembers what it said so you can ask follow-ups like *"why did you say WAIT?"* or *"compare that to ETH"*.

---

## The Physics Logic

Reelioo interprets raw market data through three forces:

| Force | What it measures |
|---|---|
| **Mass** | Volume behind a price move. High = real buyers present. Low = **Vacuum Trap** — price moved without conviction, likely to reverse |
| **Velocity** | Speed of orders hitting the market. High = strong momentum. Low = passive, weak market |
| **Friction** | Where price gets stuck — resistance zones the agent flags in reasoning |

### Vacuum Trap
When price moves more than 2% but volume is below 70% of average — Reelioo flags this as a **Vacuum Trap**. The move has no mass behind it and is historically likely to reverse.

### Loading Signal
When volume is building above 180% of average but price is flat — Reelioo flags **Loading**. Energy is accumulating for a breakout.

---

## Stack

| Layer | Technology |
|---|---|
| **AI Agent** | LangChain · GPT-4o-mini · Tool calling |
| **Market Data** | Binance public API (no key needed) |
| **Backend** | Flask · Python 3.12 · Gunicorn |
| **Frontend** | HTMX · Tailwind CSS · Jinja2 |
| **Deployment** | Railway |

---

## Run Locally

This project uses **uv** for dependency management.

**1. Clone the repo**
```bash
git clone https://github.com/agenticmohit/reelioo.git
cd reelioo
```

**2. Install dependencies**
```bash
uv sync
```

**3. Add your keys**
```bash
cp .env.example .env
```
Open `.env` and set:
```
OPENAI_API_KEY=your_key_here
FLASK_SECRET_KEY=any-long-random-string
```

**4. Run**

In PyCharm — click **Run** on `app.py`

Or in terminal:
```bash
uv run python app.py
```

**5. Open**
```
http://localhost:5000
```

---

## Deploy to Railway

1. Push the repo to GitHub
2. Create a new Railway project → **Deploy from GitHub repo**
3. Set environment variables in the Railway dashboard:

| Variable | Value |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI key |
| `FLASK_SECRET_KEY` | Any 32+ character random string |

Railway auto-detects Python and serves with Gunicorn.

---

## Project Structure

```
reelioo/
├── app.py                  # Flask app — routes, HTMX endpoints, session
├── agent.py                # LangChain agent — tools wired to GPT-4o-mini
├── tools.py                # 3 Binance tools: price, momentum, volume
├── templates/
│   ├── index.html          # Terminal-style chat UI (HTMX + Tailwind)
│   ├── _thinking.html      # User bubble + animated thinking indicator
│   ├── _ai_message.html    # AI response bubble with signal formatting
│   └── _messages.html      # Session history partial
├── screenshots/
│   ├── hero.png
│   └── mobile.png
├── pyproject.toml
└── .env.example
```

---

## Security

- OpenAI key stored as Railway environment variable — never in code
- Flask secret key from environment variable — signs all session cookies
- Rate limiting: 10 AI requests / minute per IP (Flask-Limiter)
- Input validation: messages capped at 500 characters
- Security headers on every response: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`

---

*Built with LangChain · OpenAI · Binance API · No financial advice*
