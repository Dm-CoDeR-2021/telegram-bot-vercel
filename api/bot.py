from flask import Flask, request, jsonify
import os
import requests
import random
import json
import sys
sys.path.append("api/")
import db as database

db = []
last_random = 0

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

try:
    with open("api/insults.json","r", encoding="utf-8") as f:
        db = json.loads(f.read())
except : {}


def getRandomNumber(start: int, end: int) -> int:
    r = random.randint(start, end)
    r2 = random.randint(start, end)
    r3 = random.randint(start, end)
    global last_random

    _r = (r * r3) / r2

    while(_r > end):
        _r = _r / random.randint(1,3)

    while(_r < start):
        _r = _r * -random.randint(1,3)

    if int(_r) == last_random:
        return int(_r) + 1 if int(_r)+1 < end else int(_r) - 1

        
    last_random = int(_r)
    return int(_r) if _r else 0
    
    # for i in range(1, 100):
    #     if i > r*3 and i % 2 == 0:
    #         _r = random.randint(i, 100) #33
    #         if _r % 2 != 0:
    #             for _i in range(1, 100, 10):
    #                 if _r > end:
    #                     _r = _r - 10
    #                 else:
    #                     return _r

def send_reply(chat_id, message_id, text):
    if not TOKEN:
        # Avoid failing silently on missing token in local runs
        print("BOT_TOKEN is not set.")
        return
    try:
        requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": text, "reply_to_message_id": message_id}, timeout=10)
    except Exception as e:
        print("Error sending message:", e)

def send_message(chat_id, text):
    try:
        requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except Exception as e:
        print("Error sending message:", e)


@app.get("/")
def index():
    # Simple health check
    return "ok new12"

@app.post("/")
def webhook():
    update = request.get_json(silent=True) or {}
    message = update.get("message") or update.get("edited_message")
    if not message:
        return jsonify(ok=True)

    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    text = str(text)
    reply = message.get("reply_to_message")
        
    if "new_chat_members" in message:
        for m in message["new_chat_members"]:
            if m["is_bot"] and m["username"] == "Mobinmubot":
                send_message(chat_id, "کیرم تو این گروه")

    if message["chat"]["type"] == "private" and len(text) > 1:
        for i in db:
            for _i in i["key"]:
                if text.find(_i) != -1:
                    for __i in i["msg"]:
                        if text.find(__i) != -1:
                            send_reply(chat_id, message["message_id"], i[f"answer{getRandomNumber(1,len(i)-1)}"])
                            break
                    break
        
        res = database.Upsert(data={
            "id": int(message["from"]["id"]),
            "first_name": database.decode_unicode(str(message["from"]["first_name"])) if str(message["from"]["first_name"]).find(r"\u1d") else str(message["from"]["first_name"]),
            "last_name": database.decode_unicode(str(message["from"].get("last_name"))) if str(message["from"].get("last_name")).find(r"\u1d") else str(message["from"].get("last_name")),
            "username": str(message["from"]["username"])
        })
        send_message(chat_id, res)
    
    if str(reply) != "null" and message["chat"]["type"] != "private":
        if reply["from"].get("id") == 8202290017:
            for i in db:
                for _i in i["key"]:
                    if text.find(_i) != -1:
                        for __i in i["msg"]:
                            if text.find(__i) != -1:
                                send_reply(chat_id, message["message_id"], i[f"answer{getRandomNumber(1,len(i)-1)}"])
                                break
                        break

    return jsonify(ok=True)
