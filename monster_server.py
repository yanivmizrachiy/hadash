import pyautogui
import os
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)

AUTHORIZED_PHONE_IP = "10.14.20.125"

def is_authorized():
    return request.remote_addr == AUTHORIZED_PHONE_IP or request.remote_addr == "127.0.0.1"

@app.route('/screen')
def screen():
    if not is_authorized(): return "Forbidden", 403
    screenshot = pyautogui.screenshot()
    img_io = BytesIO()
    screenshot.save(img_io, 'JPEG', quality=35)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/action', methods=['POST'])
def action():
    if not is_authorized(): return "Forbidden", 403
    data = request.json
    cmd = data.get('cmd')
    
    if cmd == 'click':
        sw, sh = pyautogui.size()
        pyautogui.click(data['x'] * sw, data['y'] * sh)
    elif cmd == 'type':
        pyautogui.write(data['text'], interval=0.05)
    elif cmd == 'vol_up': pyautogui.press('volumeup')
    elif cmd == 'vol_down': pyautogui.press('volumedown')
    elif cmd == 'shutdown': os.system('shutdown /s /t 5')
    
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("🚀 TITAN PRO מופעל בתיקייה הנכונה!")
    app.run(host='0.0.0.0', port=5000, threaded=True)
