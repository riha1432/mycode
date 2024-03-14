import cv2
from ultralytics import YOLO
import time
cap = cv2.VideoCapture('')
model = YOLO('./yolov8_pretrained/yolov8n.pt')

while True:
    time.sleep(0.0001)
    #    cap = cv2.VideoCapture('')
    for i in range(3):
        ret, frame = cap.read()
    result = model.predict(frame, save=True, conf=0.4, augment=False, retina_masks = False)
    if not ret:
        break
    cv2.imshow('yolo', result[0].plot())
    #cv2.imshow('yolo',frame)
    if cv2.waitKey(20) == 27:
        break

cap.release()
cv2.destroyAllWindows()
