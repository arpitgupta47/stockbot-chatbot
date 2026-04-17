# StockBot — Stock Market Chatbot
### College Project | Python + Flask + yfinance

---

## Project Architecture

```
User Input
  │
  ▼
Intent Detection (NLP)        ← What does the user want?
  │ price / trend / compare / 52week / info
  ▼
Symbol Detection              ← Which stock(s)?
  │ "Apple" → AAPL, "Reliance" → RELIANCE.NS
  ▼
Stock API (yfinance)          ← Fetch real market data
  │ price, history, metadata
  ▼
Data Processing               ← Calculate trend, change %
  ▼
Response Builder              ← Format human-readable reply
  ▼
Flask REST API → Frontend HTML
```

---

## Features

| Feature              | Description                                        |
|---------------------|----------------------------------------------------|
| Intent Detection     | Detects price / trend / compare / 52-week / info  |
| Company Detection    | Maps names like "Apple" → AAPL, "Reliance" → .NS |
| Live Price Fetch     | Real data via yfinance (Yahoo Finance)            |
| 30-Day Trend         | Historical price analysis with UP/DOWN direction  |
| Stock Comparison     | Compare up to 4 stocks side-by-side               |
| 52-Week Range        | Annual high/low data                              |
| REST API             | Clean `/api/chat` endpoint                        |
| Web UI               | Terminal-style chat interface                     |

---

## Setup & Run

### 1. Install dependencies
```bash
🚀 Stock Market Chatbot (Full Guide + Code)
🧠 Features You Want (We’ll Build All)

✔ Stock intent detection
✔ Company symbol detection
✔ Stock API integration
✔ Live price fetch
✔ Basic trend logic

🏗️ Project Architecture
User Input → NLP (intent + company detection)
           → Symbol mapping
           → Stock API call
           → Data processing
           → Response (price + trend)
```

### 2. Project structure
```
stockbot_project/
├── app.py              ← Flask backend (main file)
├── static/
│   └── index.html      ← Frontend chat UI
└── README.md
```

### 3. Run the server
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

---

## API Endpoints

| Endpoint              | Method | Description              |
|----------------------|--------|--------------------------|
| `/api/chat`          | POST   | Main chatbot endpoint    |
| `/api/price/<sym>`   | GET    | Direct price lookup      |
| `/api/history/<sym>` | GET    | Historical data          |
| `/api/symbols`       | GET    | List supported symbols   |
| `/api/health`        | GET    | Server health check      |

### Example API call
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "price of Apple"}'
```

---

## Supported Stocks

**US Stocks:** AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, NFLX, JPM, INTC, AMD...

**Indian Stocks (NSE):** RELIANCE, TCS, INFY, WIPRO, HDFC Bank, ICICI, SBI, Kotak, Bajaj, Maruti...

---

## Example Queries

- "What is the price of Apple?"
- "Show me Tesla trend"
- "Compare Microsoft vs Google vs NVIDIA"
- "52 week high of NVDA"
- "Tell me about Reliance stock"
- "Is TSLA going up or down?"

---

## Technologies Used

- **Python 3.10+** — Backend language
- **Flask** — Web framework
- **yfinance** — Yahoo Finance API wrapper
- **flask-cors** — Cross-Origin Resource Sharing
- **HTML/CSS/JS** — Frontend (no frameworks needed)

---

## Module Breakdown (for report)

### 1. `IntentDetector` class
Uses keyword matching (NLP) to classify what the user wants:
price | trend | compare | 52week | info | help | greet

### 2. `SymbolDetector` class
Maps company names and direct symbols to ticker strings:
- "Apple" → AAPL
- "Reliance" → RELIANCE.NS

### 3. `StockAPI` class
Three methods:
- `get_price()` → current price + change
- `get_history()` → 30-day OHLCV data
- `get_52week()` → annual range

### 4. `ResponseBuilder` class
Formats raw data into conversational responses

### 5. `StockChatbot` class
Orchestrator — wires all modules together

---

*Built for college project. Data from Yahoo Finance via yfinance.*
