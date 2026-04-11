# ⚡ Reelioo — Agentic Crypto Intelligence

> A crypto analysis agent powered by LangChain and GPT-4o-mini. Ask about any coin in plain English — Reelioo pulls live Binance data, calculates Mass and Velocity scores, and returns a clear BUY / WAIT / AVOID signal.

---

## What It Does

```
You:     Analyse BTC right now
Reelioo: ● BUY
         Confidence  78%
         Mass        62/100 — MODERATE — OK volume
         Velocity    81/100 — HIGH — Strong momentum
         Reasoning   BTC is showing strong upward velocity with
                     moderate volume support. No Vacuum Trap detected.
                     Momentum favours buyers at this level.
```

The agent remembers your conversation — ask follow-up questions and it keeps context.

---

## How It Works

Reelioo runs a LangChain agent loop with 3 tools:

```
User asks about BTC
        ↓
Agent calls get_crypto_price("BTC")     → live price, 24h change, volume
        ↓
Agent calls get_market_momentum("BTC")  → Velocity score 0-100
        ↓
Agent calls get_volume_analysis("BTC")  → Mass score 0-100, Vacuum Trap check
        ↓
GPT-4o-mini reasons over all 3 results
        ↓
Returns: SIGNAL · CONFIDENCE · MASS · VELOCITY · REASONING
```

**Thread ID + Flask session** keeps conversation context — the agent remembers what it said so you can ask follow-up questions like *"why did you say WAIT?"* or *"compare that to ETH"*.

---

## The Physics Logic

Reelioo interprets market data through three forces:

| Force | What it measures |
|---|---|
| **Mass** | Volume behind a price move. High = real buyers. Low = Vacuum Trap (likely reversal) |
| **Velocity** | Speed of orders hitting the market. High = strong momentum. Low = passive, weak market |
| **Friction** | Where price gets stuck — resistance zones the agent flags in reasoning |

---

## Stack

```
AI        LangChain · GPT-4o-mini · Tool calling
Data      Binance public API (no key needed)
Backend   Flask · Python
Frontend  Tailwind CSS · Jinja2
```

---

## Run Locally

This project uses **uv** for dependency management.

**1. Clone the repo**
```bash
git clone https://github.com/agenticmohit/reelioo.git
cd reelioo
```

**2. Install dependencies with uv**
```bash
uv sync
```

**3. Add your OpenAI key**
```bash
cp .env.example .env
```
Open `.env` and add:
```
OPENAI_API_KEY=your_key_here
```

**4. Run the app**

In PyCharm — click the **Run** button on `app.py`

Or in terminal with uv:
```bash
uv run python app.py
```

**5. Open in browser**
```
http://localhost:5000
```

---

## Project Structure

```
reelioo/
├── agent.py          # LangChain agent — tools wired to GPT-4o-mini
├── tools.py          # 3 tools: price, momentum, volume analysis
├── app.py            # Flask app — routes and session memory
├── templates/
│   └── index.html    # Terminal-style chat UI
├── .env.example      # API key template
└── requirements.txt  # Dependencies
```

---

*Built with LangChain · OpenAI · Binance API · No financial advice*