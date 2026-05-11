import time
from flask import Flask, render_template, Response, jsonify
from smart_gate import SmartGate

app = Flask(__name__)
sistema = SmartGate()

def generate_frames():
    while True:
        frame_bytes = sistema.get_frame()
        if frame_bytes:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    # Evitar error si estado_actual aún no existe (antes del primer frame)
    if hasattr(sistema, 'estado_actual'):
        return jsonify(sistema.estado_actual)
    return jsonify({"estado": "ESPERANDO", "nombre": ""})

if __name__ == '__main__':
    # run with threaded=True to ensure video stream works alongside status API
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
