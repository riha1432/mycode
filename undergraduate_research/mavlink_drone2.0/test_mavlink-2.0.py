import serial
import numpy as np
import pandas as pd
import time
import Environmental_drones as Ed
from pymavlink import mavutil
from pymavlink.dialects.v20 import common

mavlin = mavutil.mavlink_connection('tcp:localhost:5763')
mavlin.wait_heartbeat()
msg = 0
def mav():
    global msg
    mavlin.mav.command_long_send(
        mavlin.target_system,
        mavlin.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,  # confirmation
        mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED,
        0, 0, 0, 0, 0, 0  # unused parameters
    )
    msg = mavlin.recv_match(type = 'LOCAL_POSITION_NED',blocking=True)

py_serial = serial.Serial(
    port='COM3',
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
    mavlin.set_mode_apm(4, 1, 1)
    print("gui")
    time.sleep(4)
    mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component, 
                          common.MAV_CMD_COMPONENT_ARM_DISARM,0, 1,0,0,0,0,0,0)
    print("arm")
    time.sleep(5)
    mavlin.mav.command_long_send(mavlin.target_system, mavlin.target_component,
                              common.MAV_CMD_NAV_TAKEOFF, 0, 0,0,0,0,0,0,10)
    print("take off")
    time.sleep(7)


csv_file = []
ave = []

def Delay():
    print("delay")
    delay = time.time()
    data = 0
    while time.time() - delay < 10:
        data = Ed.Serial_read(py_serial, Rece)
        if(data != 0):
            csv_file.append(data)
    print("delay off")

def main():
    # Delay()
    check = 0
    index = 0
    # commend = 'SG1X' + str(Send[0].x) + 'Y' + str(Send[0].y) + 'Z' + str(Send[0].z) + 'D000E'
    # py_serial.write(commend.encode('utf-8'))
    mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
                                                                             mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[0].x,Send[0].y,-Send[0].z, 0,0,0, 0,0,0, 0,0))
    print("1")
    while True:
        Ed.Serial_read(py_serial, Rece)
        mav()
        if check == 1 and abs(Send[index].x - msg.x) < 2 and abs(Send[index].y - msg.y) < 2 and abs(-Send[index].z - msg.z) < 2 :
            Delay()
            check = 0
            index += 1
            if(index > Send.__len__() -1 ):
                break
            mavlin.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mavlin.target_system, mavlin.target_component,
                                                                             mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[index].x,Send[index].y,-Send[index].z, 0,0,0, 0,0,0, 0,0))
        else:
            check = 1

if(__name__ == "__main__"):
    setup()
    time_last = time.time()
    print(time_last)
    main()
    time.sleep(3)
    # py_serial.write(b'SM2000000000E')
    mavlin.set_mode_apm(6, 1, 1)
    print("home")
    while True:
        Ed.Serial_read(py_serial, Rece)
        mav()
        if abs(0 - msg.x) < 1 and abs(0 - msg.y) < 1:
            break

    # py_serial.write(b'SM3000000000E')
    mavlin.set_mode_apm(9, 1, 1)
    print("land")
    py_serial.close()
    print(time.time()-time_last)

    csv_file = np.array(csv_file)
    df = pd.DataFrame(csv_file)
    df.to_csv('data.csv', index=False, header=["time", "Lat","Lon", "Alt", "LPG", "CH4", "CO", "CO2", "NO2", 'PM1_0', 'PM2_5', "PM10_0"])