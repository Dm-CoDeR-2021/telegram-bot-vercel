from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    if not TOKEN:
        # Avoid failing silently on missing token in local runs
        print("BOT_TOKEN is not set.")
        return
    try:
        requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except Exception as e:
        print("Error sending message:", e)

@app.get("/")
def index():
    # Simple health check
    return "ok"

@app.post("/")
def webhook():
    update = request.get_json(silent=True) or {}
    message = update.get("message") or update.get("edited_message")
    if not message:
        return jsonify(ok=True)

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(chat_id, "سلام! ربات فعاله ✅")
    elif text:
        send_message(chat_id, f"شما گفتید: {text}")

    return jsonify(ok=True)
