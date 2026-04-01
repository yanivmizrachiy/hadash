import pyautogui, os, cv2, time, psutil, socket
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)
cam = None
pyautogui.FAILSAFE = False

@app.route('/health')
def health():
    return jsonify({
        "status": "online",
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    })

@app.route('/screen')
def screen():
    img = pyautogui.screenshot()
    img = img.resize((1280, 720))
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

@app.route('/repair', methods=['POST'])
def repair():
    # פקודת תיקון מרחוק - ריסטארט לשרת
    os.system("start /b python monster_server.py")
    return jsonify({"action": "restarting_core"})

@app.route('/action', methods=['POST'])
def action():
    data = request.json
    cmd = data.get('cmd')
    if cmd == 'click': pyautogui.click(data['x']*pyautogui.size().width, data['y']*pyautogui.size().height)
    elif cmd == 'right_click': pyautogui.rightClick(data['x']*pyautogui.size().width, data['y']*pyautogui.size().height)
    elif cmd == 'type': pyautogui.write(data['text'], interval=0.01)
    elif cmd == 'vol_up': pyautogui.press('volumeup')
    elif cmd == 'vol_down': pyautogui.press('volumedown')
    elif cmd == 'lock': os.system('rundll32.exe user32.dll,LockWorkStation')
    elif cmd == 'cam_off':
        global cam
        if cam: cam.release(); cam = None
    elif cmd == 'shutdown': os.system('shutdown /s /t 10')
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
