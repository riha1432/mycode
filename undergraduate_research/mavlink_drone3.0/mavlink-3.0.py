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
ragneMax = 50
centerPostion = [0,0]
centerMove = [[10,10], [10,-10], [-10,-10], [-10,10]]
Move = [[5,5], [5,-5], [-5,-5], [-5,5]]

def Move_Append():
    Send.append(Ed.Postion(Move[0][0] + centerPostion[0], Move[0][1] + + centerPostion[1], 15))
    Send.append(Ed.Postion(Move[1][0] + centerPostion[0], Move[1][1] + + centerPostion[1], 15))
    Send.append(Ed.Postion(Move[2][0] + centerPostion[0], Move[2][1] + + centerPostion[1], 15))
    Send.append(Ed.Postion(Move[3][0] + centerPostion[0], Move[3][1] + + centerPostion[1], 15))

def setup():
    if py_serial.isOpen() == False: #시리얼 포트가 open인지 확인
        py_serial.open() #시리얼 포트를 연다

    Move_Append()
    for i in range(20):
        while True:
            if(Ed.Serial_read(py_serial, Rece)!=0):
                break
    
    if(int(input("data in"))):
        exit()

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
total_Ave = []
ave = []

def Delay():
    delay = time.time()
    data = 0
    co2_data = 0

    while time.time() - delay < 10:
        data = Ed.Serial_read(py_serial, Rece)
        if(len(data) != 0):
            csv_file.append(data)
            if(co2_data == 0):
                co2_data = data[7]
            else:
                co2_data = co2_data * 0.5 + data[7] * 0.5

def dataMax():
    index = 0
    max = ave[0]
    for i in range(1,len(ave)):
        if(max < ave[i]):
            max = ave[i]
            index = i
    return index

def main():
    while True:
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
                
        Send.clear()
        total_Ave.append(ave)
        print(total_Ave)
        if((centerPostion[0] + 10 < ragneMax) and (centerPostion[0] - 10 > -ragneMax)) and ((centerPostion[1] + 10 < ragneMax) and (centerPostion[1] - 10 > -ragneMax)):
            key = dataMax()
            centerPostion[0] += centerMove[key][0]
            centerPostion[1] += centerMove[key][1]
            Move_Append()
        else:
            break
        ave.clear()

if(__name__ == "__main__"):
    setup()
    time_last = time.time()
    print(time_last)
    main()

    time.sleep(3)
    py_serial.write(b'SM2000000000E')
    print("home")

    while True:
        Ed.Serial_read(py_serial, Rece)
        if abs(0 - Ed.Now_pos.x) < 1 and abs(0 - Ed.Now_pos.y) < 1:
            break
    
    py_serial.write(b'SM3000000000E')
    print("land")
    
    py_serial.close()
    print(time.time()-time_last)

    csv_file = np.array(csv_file)
    df = pd.DataFrame(csv_file)
    df.to_csv('data.csv', index=False, header=["time", "Lat","Lon", "Alt", "LPG", "CH4", "CO", "CO2", "NO2", 'PM1_0', 'PM2_5', "PM10_0"])