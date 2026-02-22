import requests
import time
import os

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
        time.sleep(300)  # 5 минут

    except:
        time.sleep(60)
