import pyautogui, os, cv2, time, psutil, socket, numpy as np
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)
cam = None
pyautogui.PAUSE = 0 

@app.route('/health')
def health():
    return jsonify({"cpu": psutil.cpu_percent(), "ram": psutil.virtual_memory().percent})

@app.route('/screen')
def screen():
    # צילום מסך באיכות Quantum
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # הגדלת הרזולוציה לניצול מסך הסמסונג אולטרה
    width = 1280
    height = 720
    resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
    
    _, buf = cv2.imencode('.jpg', resized, [cv2.IMWRITE_JPEG_QUALITY, 55])
    return send_file(BytesIO(buf), mimetype='image/jpeg')

@app.route('/webcam')
def webcam():
    global cam
    if cam is None: cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret: return "Error", 500
    # שיפור איכות מצלמה
    _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
    return send_file(BytesIO(buf), mimetype='image/jpeg')

@app.route('/action', methods=['POST'])
def action():
    data = request.json
    cmd = data.get('cmd')
    if cmd == 'click': pyautogui.click(data['x']*pyautogui.size().width, data['y']*pyautogui.size().height)
    elif cmd == 'right_click': pyautogui.rightClick(data['x']*pyautogui.size().width, data['y']*pyautogui.size().height)
    elif cmd == 'type': pyautogui.write(data['text'], interval=0.01)
    elif cmd == 'desktop': pyautogui.hotkey('win', 'd')
    elif cmd == 'vol_up': pyautogui.press('volumeup')
    elif cmd == 'vol_down': pyautogui.press('volumedown')
    elif cmd == 'copy': pyautogui.hotkey('ctrl', 'c')
    elif cmd == 'paste': pyautogui.hotkey('ctrl', 'v')
    elif cmd == 'task_manager': pyautogui.hotkey('ctrl', 'shift', 'esc')
    elif cmd == 'enter': pyautogui.press('enter')
    elif cmd == 'lock': os.system('rundll32.exe user32.dll,LockWorkStation')
    elif cmd == 'shutdown': os.system('shutdown /s /t 10')
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

