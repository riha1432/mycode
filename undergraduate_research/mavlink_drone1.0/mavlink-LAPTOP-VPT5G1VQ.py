import serial
import numpy as nu
import time

class Postion:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

def int16(x):
    if(x > 0x7fff):
        x = (x - 0x1)^0xffff
        return -x
    else:
        return x
    
def int32(x):
    if(x > 0x7fffffff):
        x = (x - 0x1)^0xffffffff
        return -x
    else:
        return x

def dr_print():
    global Now_pos
    Now_pos.x = int16((Rece[0]<<8) | Rece[1])/10.0
    Now_pos.y = int16((Rece[2]<<8) | Rece[3])/10.0
    Now_pos.z = -(int16((Rece[4]<<8) | Rece[5])/10.0)
    lat = ((Rece[6]<<24) | (Rece[7]<<16) |(Rece[8]<<8) |(Rece[9]))
    lon = ((Rece[10]<<24) | (Rece[11]<<16) |(Rece[12]<<8) |(Rece[13]))
    Alt = ((Rece[14]<<24) | (Rece[15]<<16) |(Rece[16]<<8) |(Rece[17]))
    v = ((Rece[18]<<8) | Rece[19])
    lpg = ((Rece[20]<<8) | Rece[21])
    ch4 = ((Rece[22]<<8) | Rece[23])
    co = ((Rece[24]<<8) | Rece[25])
    co2 = ((Rece[26]<<8) | Rece[27])
    no2 = ((Rece[28]<<8) | Rece[29])
    pm1_0 = Rece[30]
    pm2_5 = Rece[31]
    pm10_0 = Rece[32]
    # mode = Rece[41]
    # ack = Rece[42]
    print("x : ", (Now_pos.x), end=' ')
    print("y : ", (Now_pos.y), end=' ')
    print("z : ", (Now_pos.z), end=' ')
    print("lat : ", int32(lat)/100.0, end=' ')
    print("lon : ", int32(lon)/100.0, end=' ')
    print("galt : ", int32(Alt)/100.0, end=' ')
    print("v : ", int16(v)/1000.0, end=' ')
    print("LPG : ", int16(lpg)/10.0, end=' ')
    print("CH4 : ", int16(ch4)/10.0, end=' ')
    print("CO : ", int16(co)/10.0, end=' ')
    print("Co2 : ", int16(co2), end=' ')
    print("No2 : ", int16(no2)/100.0, end=' ')
    print("pm1.0 : ", int16(pm1_0), end=' ')
    print("pm2.5 : ", int16(pm2_5), end=' ')
    print("pm10.0 : ", int16(pm10_0))
    # print("mode: ", int16(mode), end=' ')
    # print("ack : ", int16(ack))


py_serial = serial.Serial(
    # port='COM3',
    port='COM9',
    baudrate=57600,
)

Rece = []
Send = []
Now_pos = Postion()

def Serial_read():
    if py_serial.readable():
        r_msg = py_serial.read() #데이터를 한 줄 끝까지 읽는다
        Rece.append(r_msg[0])
        # print(Rece)
        if(Rece.__len__() >= 2):
            if( chr(Rece[-2]) == 'S' and chr(Rece[-1]) == 'T'):
                Rece.clear()
            elif( chr(Rece[-1]) == 'E' and chr(Rece[-2]) == 'N'):
                dr_print()
                Rece.clear()

        # if(chr(r_msg[0]) == 'S'):
        #     Rece_index = 0
        # elif(chr(r_msg[0]) == 'E'):
        #     dr_print()
        # Rece[Rece_index] = r_msg[0]
        
        # Rece_index += 1
        # if(Rece_index >= 45):
        #     Rece_index = 45
# 높이 이륙시 주기적으로 초기화
def Serial_write():
    return

def setup():
    if py_serial.isOpen() == False: #시리얼 포트가 open인지 확인
        py_serial.open() #시리얼 포트를 연다

    # Send.append(Postion(0,0,5))
    Send.append(Postion(10,10,10))
    Send.append(Postion(10,-10,10))
    Send.append(Postion(-10,-10,10))
    Send.append(Postion(-10,10,10))

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

    commend = 'SG1X' + str(Send[0].x) + 'Y' + str(Send[0].y) + 'Z' + str(Send[0].z) + 'D000E'
    py_serial.write(commend.encode('utf-8'))

def main():
    Rece_index = 0
    Send_index = 0
    commend_next = 0
    check = 0
    index = 0
    while True:
        Serial_read()
        # if(Now_pos.x > Send[Send_index].x - 1 and Now_pos.x < Send[Send_index].x + 1) and (Now_pos.y > Send[Send_index].y - 1 and Now_pos.y < Send[Send_index].y + 1) and (Now_pos.z > Send[Send_index].z - 1 and Now_pos.z < Send[Send_index].z + 1):
        # print(Send[index].x , Now_pos.x, Send[index].y , Now_pos.y, Send[index].z , Now_pos.z, abs(Send[index].x - Now_pos.x),abs(Send[index].y - Now_pos.y),abs(Send[index].z - Now_pos.z))
        if check == 1 and abs(Send[index].x - Now_pos.x) < 2 and abs(Send[index].y - Now_pos.y) < 2 and abs(Send[index].z - Now_pos.z) < 2 :
            check = 0
            index += 1
            if(index > 3):
                break
            # mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
            #                                                                     mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[index].x,Send[index].y,Send[index].z, 0,0,0, 0,0,0, 0,0))
            commend = 'SG1X' + str(Send[index].x) + 'Y' + str(Send[index].y) + 'Z' + str(Send[index].z) + 'D000000E'
            py_serial.write(commend.encode('utf-8'))
            print(commend)
        else:
            check = 1

if(__name__ == "__main__"):
    time_last = time.time()
    print(time_last)
    setup()
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