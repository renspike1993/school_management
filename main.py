from flask import Flask, request
import requests

from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "my_verify_token_123"

@app.route("/")
def home():
    return "Messenger webhook is running!"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print("MODE:", mode)
    print("TOKEN RECEIVED:", token)
    print("EXPECTED TOKEN:", VERIFY_TOKEN)
    print("CHALLENGE:", challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification token mismatch", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Incoming webhook:", data)
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)