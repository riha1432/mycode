from ultralytics import YOLO
import cv2

model = YOLO('./yolov8_pretrained/yolov8n.pt')
result = model.predict("https://ultralytics.com/images/zidane.jpg", save=False,conf=0.5)
plots = result[0].plot()
# cv2_imshow(plots)
cv2.imshow("ad",plots)
cv2.waitKey(0)
cv2.destroyAllWindows()
