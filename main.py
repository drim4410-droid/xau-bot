import requests
import time
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def get_gold_price():
    url = "https://api.metals.live/v1/spot/gold"
    response = requests.get(url).json()
    return float(response[0]["price"])

def calculate_signal(price, last_price):
    if price > last_price:
        direction = "BUY 🟢"
        entry = price
        sl = round(price - 8, 2)
        tp = round(price + 16, 2)
    else:
        direction = "SELL 🔴"
        entry = price
        sl = round(price + 8, 2)
        tp = round(price - 16, 2)

    rr = round(abs(tp - entry) / abs(entry - sl), 2)

    return direction, entry, tp, sl, rr

def bot_loop():
    last_price = None
    while True:
        try:
            price = get_gold_price()

            if last_price:
                if abs(price - last_price) >= 3:

                    direction, entry, tp, sl, rr = calculate_signal(price, last_price)

                    message = f"""
📊 *XAU/USD AUTO SIGNAL* (5M)

Direction: *{direction}*
Entry: `{entry}`
Take Profit: `{tp}`
Stop Loss: `{sl}`

Risk/Reward: *1:{rr}*

⚠️ Use proper risk management
"""
                    send_message(message)

            last_price = price
            time.sleep(295)

        except Exception:
            time.sleep(60)

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot_loop()
