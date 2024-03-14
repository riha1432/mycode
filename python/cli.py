import socket
import cv2
import pickle
import struct
SERVER_IP = '0.0.0.0'
SERVER_PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
cap = cv2.VideoCapture(0)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    # 프레임 인코딩 및 전송
    data = pickle.dumps(frame)
    client_socket.sendall(struct.pack(">L", len(data)) + data)
    # ESC 키를 누르면 종료
    if cv2.waitKey(1) == 27:
        break


client_socket.close()