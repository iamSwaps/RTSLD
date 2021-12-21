from flask import Flask, render_template, Response
import cv2
from detector import detection
app = Flask(__name__)

camera = cv2.VideoCapture(0)  


def gen_frames():
    while(True):
        success,frame = camera.read()
        if not success:
            print("Alert ! Camera disconnected")
        else:
            detected = detection(success, frame)
            ret,buffer=cv2.imencode('.jpg',detected)
            detected=buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + detected + b'\r\n')
        
 

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)