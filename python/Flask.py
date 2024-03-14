from flask import Flask, render_template, Response
import cv2
# from ultralytics import YOLO
import time

camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture('')
# model = YOLO('./yolov8_pretrained/yolov8n.pt')
app = Flask(__name__)

def gen_frames():
  ret, frame = 0,0
  camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  camera.set(cv2.CAP_PROP_FPS,30)
  while True:
    ret, frame = camera.read()
    if not ret:
      break
    else:
      # result = model.predict(frame, save=False, conf=0.4)
      # ret, buffer = cv2.imencode('.jpg', result[0].plot())
      ret, buffer = cv2.imencode('.jpg', frame)

      frame = buffer.tobytes()
      yield (b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
  return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
  return render_template('video.html')

if __name__ == "__main__":
  # app.run(host='0.0.0.0',port=8080,debug=False,ssl_context='adhoc')
  app.run(host='0.0.0.0',port=8080,debug=False)

