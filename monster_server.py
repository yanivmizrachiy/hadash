import pyautogui, os, cv2, time, psutil, ctypes, socket
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
# הגדרה מחמירה לביטול חסימות דפדפן (CORS)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

pyautogui.FAILSAFE = False

def keep_pc_awake():
    # מניעת שינה גם כשהמסך כבוי
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000001 | 0x00000040)

@app.route('/health')
def health():
    return jsonify({"status": "alive", "cpu": psutil.cpu_percent(), "ram": psutil.virtual_memory().percent})

@app.route('/screen')
def screen():
    keep_pc_awake()
    img = pyautogui.screenshot().resize((1024, 576))
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=30)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/action', methods=['POST', 'OPTIONS'])
def action():
    if request.method == 'OPTIONS':
        return jsonify({"ok": True}), 200
    
    data = request.json
    cmd = data.get('cmd')
    
    # ביצוע פיזי - אמת בלבד
    if cmd == 'click': pyautogui.click(data['x']*pyautogui.size().width, data['y']*pyautogui.size().height)
    elif cmd == 'right_click': pyautogui.rightClick(data['x']*pyautogui.size().width, data['y']*pyautogui.size().height)
    elif cmd == 'type': pyautogui.write(data['text'], interval=0.01)
    elif cmd == 'desktop': pyautogui.hotkey('win', 'd')
    elif cmd == 'vol_up': pyautogui.press('volumeup')
    elif cmd == 'vol_down': pyautogui.press('volumedown')
    elif cmd == 'lock': os.system('rundll32.exe user32.dll,LockWorkStation')
    elif cmd == 'shutdown': os.system('shutdown /s /t 10')
    
    return jsonify({"status": "executed", "pc": "SALON"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
