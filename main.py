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
        "text": text
    }
    requests.post(url, data=data)

def get_gold_price():
    url = "https://api.metals.live/v1/spot/gold"
    response = requests.get(url).json()
    return float(response[0]["price"])

def bot_loop():
    last_price = None
    while True:
        try:
            price = get_gold_price()

            if last_price:
                if price > last_price + 3:
                    send_message(f"📈 BUY XAU/USD\nPrice: {price}")
                elif price < last_price - 3:
                    send_message(f"📉 SELL XAU/USD\nPrice: {price}")

            last_price = price
            time.sleep(300)
        except:
            time.sleep(60)

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot_loop()
