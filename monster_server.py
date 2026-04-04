import pyautogui, os, cv2, time, psutil, ctypes
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # ביטול מוחלט של חסימות דפדפן
pyautogui.FAILSAFE = False

@app.route('/screen')
def screen():
    # צילום מסך מהיר
    img = pyautogui.screenshot().resize((1024, 576))
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=35)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/action', methods=['POST', 'OPTIONS'])
def action():
    if request.method == 'OPTIONS': return jsonify({"ok": True}), 200
    data = request.json
    cmd = data.get('cmd')
    if cmd == 'click': pyautogui.click(data['x']*pyautogui.size().width, data['y']*pyautogui.size().height)
    elif cmd == 'vol_up': pyautogui.press('volumeup')
    elif cmd == 'vol_down': pyautogui.press('volumedown')
    elif cmd == 'lock': os.system('rundll32.exe user32.dll,LockWorkStation')
    elif cmd == 'shutdown': os.system('shutdown /s /t 10')
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
