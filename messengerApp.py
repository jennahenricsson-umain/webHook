from flask import Flask, request, jsonify

app = Flask(__name__)

# En valfri kodsträng du hittar på själv och skriver in i Meta-portalen
VERIFY_TOKEN = "min_hemliga_nyckel_123"
PAGE_ACCESS_TOKEN = "EAAW7cCsOtEIBQgqDZB1UGu5DMYYPgZAvWfjeiR827FGWMrsQGSUPsaQLqhyXMn0BT8hfZCK5ZC2LU46ZCPKAs7r2cBKlSmp0pGZAFYKc3yAQ3BOIPCE4mZB0jhHj5f4mQBAURB7oH6KuLOp5J83u0UjMKGZAqJBduyBcAIZB0pAIZBAZBgPlncXCaFsrNzBqj5TeflSnLbYoQZDZD"

@app.route('/webhook', methods=['GET'])
def verify():
    # Meta skickar en kontrollfråga för att verifiera din server
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verifiering misslyckades", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text")
                    print(f"Meddelande från {sender_id}: {message_text}")
                    
                    # Här kan du anropa en funktion för att skicka svar
    
    return "EVENT_RECEIVED", 200

if __name__ == '__main__':
    app.run(port=5000)