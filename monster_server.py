import pyautogui, os, cv2, time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)
cam = None

@app.route('/screen')
def screen():
    img = pyautogui.screenshot()
    img = img.resize((1024, 576))
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=30)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/webcam')
def webcam():
    global cam
    if cam is None: cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret: return "Error", 500
    _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 35])
    return send_file(BytesIO(buf), mimetype='image/jpeg')

@app.route('/action', methods=['POST', 'OPTIONS'])
def action():
    if request.method == 'OPTIONS': return jsonify({"ok": True}), 200
    data = request.json
    cmd = data.get('cmd')
    global cam
    if cmd == 'click':
        sw, sh = pyautogui.size()
        pyautogui.click(data['x']*sw, data['y']*sh)
    elif cmd == 'type': pyautogui.write(data['text'], interval=0.01)
    elif cmd == 'vol_up': pyautogui.press('volumeup')
    elif cmd == 'vol_down': pyautogui.press('volumedown')
    elif cmd == 'lock': os.system('rundll32.exe user32.dll,LockWorkStation')
    elif cmd == 'cam_off': 
        if cam: cam.release(); cam = None
    elif cmd == 'shutdown': os.system('shutdown /s /t 5')
    return jsonify({"status": "executed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
