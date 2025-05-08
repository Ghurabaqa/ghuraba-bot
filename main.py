import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Veilig via Render Environment
GROUP_CHAT_ID = '-1002517503255'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

@app.route('/', methods=['POST'])
def handle_message():
    data = request.get_json()
    if 'message' in data:
        msg = data['message']
        text = msg.get('text', '')
        sender = msg.get('from', {})
        name = f"{sender.get('first_name', '')} {sender.get('last_name', '')}".strip()
        username = sender.get('username', '(geen gebruikersnaam)')

        if text.strip() == '/start':
            welcome = (
                "🟢 Welcome to Ghurabā Q&A Bot\n"
                "As-salāmu ‘alaykum wa rahmatullāhi wa barakātuh,\n\n"
                "Use this bot to ask your Islamic questions privately.\n"
                "📢 The answer will be posted in the channel: Ghurabā Q&A.\n"
                "🤝 Your privacy is respected.\n\n"
                "—\n\n"
                "🟢 Welkom bij Ghurabā Q&A Bot\n"
                "As-salāmu ‘alaykum wa rahmatullāhi wa barakātuh,\n\n"
                "Stel hier je islamitische vraag in alle vertrouwen.\n"
                "📢 Het antwoord wordt gedeeld in het kanaal: Ghurabā Q&A.\n"
                "🤝 Jouw privacy wordt gerespecteerd.\n\n"
                "📌 Typ hieronder je vraag."
            )
            requests.post(API_URL, data={
                'chat_id': msg['chat']['id'],
                'text': welcome
            })
            return {'ok': True}

        # Andere berichten naar groep doorsturen
        content = f"📩 *Nieuwe vraag ontvangen*\nVan: @{username} / {name}\n\n{text}"
        requests.post(API_URL, data={
            'chat_id': GROUP_CHAT_ID,
            'text': content,
            'parse_mode': 'Markdown'
        })

    return {'ok': True}

@app.route('/', methods=['GET'])
def home():
    return 'Bot is running.'

app.run(host='0.0.0.0', port=8080)
