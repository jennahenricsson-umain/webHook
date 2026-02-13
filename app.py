from flask import Flask, request, jsonify
import requests

# Dina unika uppgifter
TOKEN = "8512617836:AAGt5v1vsdshl6EJSvhK58WKmZTmmW0lKsg"
CHAT_ID = "8551506578"  # ID för den person/grupp som ska få meddelandet
MESSAGE = "Hej! Detta meddelande skickades från min externa webbsida."

def send_telegram_message(token, chat_id, text):
    # Telegrams API-endpoint för att skicka meddelanden
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown" # Gör att du kan använda **fetstil** etc.
    }

    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Meddelandet skickades framgångsrikt!")
    else:
        print(f"Något gick fel: {response.text}")

# Kör funktionen
send_telegram_message(TOKEN, CHAT_ID, MESSAGE)

app = Flask(__name__)

# Detta är adressen som Telegram kommer att skicka meddelanden till
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    # 1. Ta emot datan från Telegram
    data = request.get_json()
    
    # 2. Extrahera meddelandet och vem som skickade det
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")
        username = data["message"]["from"].get("first_name", "Okänd")

        print(f"Nytt meddelande från {username} (ID: {chat_id}): {user_text}")

        # Här kan du lägga in logik för att spara i en databas 
        # eller uppdatera din externa webbsida i realtid.
        
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # Kör servern på port 5000
    app.run(port=5000)