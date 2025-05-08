import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_CHAT_ID = '-1002517503255'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
ADMIN_IDS = ['8111624197']  # Jouw Telegram ID hier

@app.route('/', methods=['POST'])
def handle_message():
    data = request.get_json()
    if 'message' in data:
        msg = data['message']
        text = msg.get('text', '')
        chat_id = msg['chat']['id']
        sender = msg.get('from', {})
        user_id = str(sender.get('id'))
        name = f"{sender.get('first_name', '')} {sender.get('last_name', '')}".strip()
        username = sender.get('username', '(geen gebruikersnaam)')

        # START - Welkomstbericht
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
            requests.post(API_URL, data={'chat_id': chat_id, 'text': welcome})
            return {'ok': True}

        # REPLY - Alleen admin
        if text.startswith('/reply') and user_id in ADMIN_IDS:
            try:
                parts = text.split(' ', 2)
                target_id = parts[1]
                reply_msg = parts[2]
                requests.post(API_URL, data={'chat_id': target_id, 'text': reply_msg})
            except:
                requests.post(API_URL, data={'chat_id': chat_id, 'text': '⚠️ Ongeldig /reply commando.'})
            return {'ok': True}

        # VRAAG → doorsturen naar groep
        content = (
            f"📩 *Nieuwe vraag ontvangen*\n"
            f"Van: @{username} / {name}\n"
            f"ID: `{chat_id}`\n\n"
            f"{text}"
        )
        requests.post(API_URL, data={
            'chat_id': GROUP_CHAT_ID,
            'text': content,
            'parse_mode': 'Markdown'
        })

        # Automatisch antwoord naar gebruiker
        auto_reply = (
            "📩 Your question has been received. Keep an eye on the channel for the answer, in shā’ Allāh. Jāzakallāhu khayran!\n\n"
            "📩 Je vraag is binnengekomen. Houd het kanaal in de gaten voor het antwoord, in shā’ Allāh. Jāzakallāhu khayran!"
        )
        requests.post(API_URL, data={'chat_id': chat_id, 'text': auto_reply})

    return {'ok': True}

@app.route('/', methods=['GET'])
def home():
    return 'Bot is running.'

app.run(host='0.0.0.0', port=8080)
