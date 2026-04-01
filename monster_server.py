import pyautogui, os, cv2, time, psutil, subprocess, socket
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)
cam = None
pyautogui.FAILSAFE = False

@app.route('/health')
def health():
    return jsonify({"cpu": psutil.cpu_percent(), "ram": psutil.virtual_memory().percent, "pc": socket.gethostname()})

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

@app.route('/action', methods=['POST'])
def action():
    data = request.json
    cmd = data.get('cmd')
    
    # פקודות עכבר
    if cmd == 'click': pyautogui.click(data['x']*pyautogui.size().width, data['y']*pyautogui.size().height)
    elif cmd == 'right_click': pyautogui.rightClick(data['x']*pyautogui.size().width, data['y']*pyautogui.size().height)
    
    # פקודות מקלדת וטקסט
    elif cmd == 'type': pyautogui.write(data['text'], interval=0.01)
    elif cmd == 'enter': pyautogui.press('enter')
    elif cmd == 'backspace': pyautogui.press('backspace')
    
    # ניהול חלונות (ווינדוס)
    elif cmd == 'desktop': pyautogui.hotkey('win', 'd')
    elif cmd == 'taskview': pyautogui.hotkey('win', 'tab')
    elif cmd == 'alt_tab': pyautogui.hotkey('alt', 'tab')
    elif cmd == 'close': pyautogui.hotkey('alt', 'f4')
    
    # שליטה בדפדפן (כרום/אדג')
    elif cmd == 'refresh': pyautogui.press('f5')
    elif cmd == 'new_tab': pyautogui.hotkey('ctrl', 't')
    elif cmd == 'close_tab': pyautogui.hotkey('ctrl', 'w')
    
    # מדיה ומערכת
    elif cmd == 'vol_up': pyautogui.press('volumeup')
    elif cmd == 'vol_down': pyautogui.press('volumedown')
    elif cmd == 'mute': pyautogui.press('volumemute')
    elif cmd == 'play': pyautogui.press('playpause')
    elif cmd == 'lock': os.system('rundll32.exe user32.dll,LockWorkStation')
    elif cmd == 'sleep': os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
    elif cmd == 'shutdown': os.system('shutdown /s /t 10')
    elif cmd == 'restart': os.system('shutdown /r /t 5')
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
