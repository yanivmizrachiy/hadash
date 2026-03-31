import pyautogui
import os
import cv2
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)

# משתנה גלובלי לבדיקת מצב מצלמה
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
    if cam is None:
        cam = cv2.VideoCapture(0) # פתיחת המצלמה הראשית
    
    success, frame = cam.read()
    if not success:
        return "Camera Error", 500
    
    # המרת הפריים של OpenCV לפורמט JPEG לשידור בטלפון
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])
    return send_file(BytesIO(buffer), mimetype='image/jpeg')

@app.route('/action', methods=['POST', 'OPTIONS'])
def action():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    data = request.json
    cmd = data.get('cmd')
    global cam
    
    if cmd == 'click':
        sw, sh = pyautogui.size()
        pyautogui.click(data['x'] * sw, data['y'] * sh)
    elif cmd == 'type':
        pyautogui.write(data['text'], interval=0.01)
    elif cmd == 'vol_up': pyautogui.press('volumeup')
    elif cmd == 'vol_down': pyautogui.press('volumedown')
    elif cmd == 'lock': os.system('rundll32.exe user32.dll,LockWorkStation')
    elif cmd == 'shutdown': 
        if cam: cam.release() # שחרור מצלמה לפני כיבוי
        os.system('shutdown /s /t 5')
    elif cmd == 'cam_off': # כיבוי המצלמה לחיסכון במשאבים
        if cam:
            cam.release()
            cam = None
    
    return jsonify({"status": "executed", "pc": "TITAN"}), 200

if __name__ == '__main__':
    print("🚀 TITAN SURVEILLANCE v7.0 IS LIVE")
    app.run(host='0.0.0.0', port=5000, threaded=True)
