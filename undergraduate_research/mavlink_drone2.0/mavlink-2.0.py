import serial
import numpy as np
import pandas as pd
import time
import Environmental_drones as Ed

py_serial = serial.Serial(
    port='COM6',
    # port='COM9',
    baudrate=57600,
)

Rece = []
Send = []

def Move_Append():
    Send.append(Ed.Postion(10,10,10))
    Send.append(Ed.Postion(10,-10,10))
    Send.append(Ed.Postion(-10,-10,10))
    Send.append(Ed.Postion(-10,10,10))

def setup():
    if py_serial.isOpen() == False: #시리얼 포트가 open인지 확인
        py_serial.open() #시리얼 포트를 연다

    Move_Append()
    for i in range(20):
        while True:
            if(Ed.Serial_read(py_serial, Rece)!=0):
                break

    time.sleep(3)
    py_serial.write(b'SM1000E')
    print("gui")
    time.sleep(4)
    py_serial.write(b'SO0000E')
    print("arm")
    time.sleep(5)
    py_serial.write(b"ST0000E")
    print("take off")
    time.sleep(7)


csv_file = []
def Delay():
    delay = time.time()
    data = 0
    while time.time() - delay < 10:
        data = Ed.Serial_read(py_serial, Rece)
        if(data != 0):
            csv_file.append(data)

def main():
    # Delay()
    check = 0
    index = 0
    Ed.Serial_write(index, py_serial, Send)
    while True:
        Ed.Serial_read(py_serial, Rece)
        if check == 1 and abs(Send[index].x - Ed.Now_pos.x) < 2 and abs(Send[index].y - Ed.Now_pos.y) < 2 and abs(Send[index].z - Ed.Now_pos.z) < 2 :
            Delay()
            check = 0
            index += 1
            if(index > Send.__len__ -1 ):
                break
            Ed.Serial_write(index, py_serial, Send)
        else:
            check = 1

if(__name__ == "__main__"):
    setup()
    time_last = time.time()
    print(time_last)
    main()
    time.sleep(3)
    py_serial.write(b'SM2000000000E')
    print("home")
    # while True:
    #     if py_serial.readable():
    #         r_msg = py_serial.read() #데이터를 한 줄 끝까지 읽는다

    #         if(chr(r_msg[0]) == 'S'):
    #             Rece_index = 0
    #         elif(chr(r_msg[0]) == 'E'):
    #             dr_print()
    #         Rece[Rece_index] = r_msg[0]

    #         Rece_index += 1
    #         if(Rece_index >= 45):
    #             Rece_index = 45
    #     if abs(0 - Now_pos.x) < 1 and abs(0 - Now_pos.y) < 1:
    #         break
    time.sleep(10)
    py_serial.write(b'SM3000000000E')
    print("land")
    py_serial.close()
    print(time.time()-time_last)

    csv_file = np.array(csv_file)
    df = pd.DataFrame(csv_file)
    df.to_csv('data.csv', index=False, header=["time", "Lat","Lon", "Alt", "LPG", "CH4", "CO", "CO2", "NO2", 'PM1_0', 'PM2_5', "PM10_0"])