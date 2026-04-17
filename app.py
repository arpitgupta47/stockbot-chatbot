from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yfinance as yf
import re
import os   # ✅ FIXED

app = Flask(__name__, static_folder='static')
CORS(app)

SYMBOL_MAP = {
    "apple": "AAPL",
    "google": "GOOGL",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "meta": "META",
    "nvidia": "NVDA",

    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "wipro": "WIPRO.NS",
    "hdfc bank": "HDFCBANK.NS",
    "icici bank": "ICICIBANK.NS",
    "sbi": "SBIN.NS",
}

DIRECT_SYMBOL_PATTERN = re.compile(r'\b([A-Z]{2,5}(?:\.NS)?)\b')

def detect_intent(text):
    text = text.lower()

    if "compare" in text or "vs" in text:
        return "compare"
    elif "trend" in text:
        return "trend"
    elif "hello" in text or "hi" in text:
        return "greet"
    elif "help" in text:
        return "help"
    else:
        return "price"

def extract_symbols(text):
    symbols = []
    text_lower = text.lower()
    text_upper = text.upper()

    for name, sym in SYMBOL_MAP.items():
        if name in text_lower:
            symbols.append(sym)

    matches = DIRECT_SYMBOL_PATTERN.findall(text_upper)
    valid_symbols = set(SYMBOL_MAP.values())

    for m in matches:
        if m in valid_symbols and m not in symbols:
            symbols.append(m)

    return symbols

def get_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="5d")

        if hist is None or len(hist) == 0:
            return {"error": True}

        current = float(hist["Close"].iloc[-1])
        prev = float(hist["Close"].iloc[-2]) if len(hist) > 1 else current

        change = current - prev
        pct = (change / prev) * 100 if prev != 0 else 0

        return {
            "symbol": symbol,
            "name": symbol,
            "price": round(current, 2),
            "change": round(change, 2),
            "change_pct": round(pct, 2),
            "prev_close": round(prev, 2),
            "currency": "INR" if ".NS" in symbol else "USD",
            "sector": "Market",
            "exchange": "NSE" if ".NS" in symbol else "NASDAQ",
            "pe_ratio": "—"
        }

    except Exception as e:
        print("PRICE ERROR:", e)
        return {"error": True}

def get_trend(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="30d")

        if hist is None or len(hist) == 0:
            return {"trend": "No Data", "change_pct": 0}

        start = float(hist["Close"].iloc[0])
        end = float(hist["Close"].iloc[-1])  # ✅ FIXED

        trend = "UP 📈" if end > start else "DOWN 📉"

        return {
            "trend": trend,
            "change_pct": round(((end - start) / start) * 100, 2)
        }

    except Exception as e:
        print("TREND ERROR:", e)
        return {"trend": "Unavailable", "change_pct": 0}

def build_response(intent, symbols):

    if intent == "greet":
        return {
            "type": "info",
            "text": "Hello! Ask me about stocks 📊",
            "suggestions": ["Price of Apple", "Tesla trend"]
        }

    if intent == "help":
        return {
            "type": "info",
            "text": "Try: price of apple, tesla trend, compare apple microsoft",
            "suggestions": ["Price of Apple", "Tesla trend", "Compare MSFT NVDA"]
        }

    if not symbols:
        return {
            "type": "error",
            "text": "❌ Company not found."
        }

    if intent == "compare":
        stocks = []
        for s in symbols[:3]:
            data = get_price(s)
            if "error" not in data:
                stocks.append(data)

        return {"type": "compare", "data": stocks}

    symbol = symbols[0]

    if intent == "trend":
        data = get_trend(symbol)
        return {
            "type": "info",
            "text": f"{symbol} Trend: {data['trend']} ({data['change_pct']}%)"
        }

    data = get_price(symbol)

    if "error" in data:
        return {
            "type": "error",
            "text": "Could not fetch stock data"
        }

    return {
        "type": "price",
        "data": data,
        "suggestions": [f"Trend of {symbol}", f"Compare {symbol} MSFT"]
    }

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"type": "error", "text": "No message"}), 400

    user_input = data["message"]

    intent = detect_intent(user_input)
    symbols = extract_symbols(user_input)

    response = build_response(intent, symbols)

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Server running on port {port}")
    app.run(host='0.0.0.0', port=port)
