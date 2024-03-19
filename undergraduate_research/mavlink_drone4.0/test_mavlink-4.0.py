import numpy as np
import pandas as pd
import time
import SerialRW
import MoveCoordinates as MC
import testMavlink as testmv

Mav = testmv.mavlink()
Mav.mavlin.wait_heartbeat()

RW = SerialRW.Serial()
py_serial = RW.SerialPort

Rece = []
Send = []
csv_file = []
Environment_total_Ave = []
Environment_Average = []
 
def setup():
    if py_serial.isOpen() == False: #시리얼 포트가 open인지 확인
        py_serial.open() #시리얼 포트를 연다

    MC.Move_Append(Send)
    RW.Serial_data_reset(py_serial, Rece, True)

    limit = int(input("data check : "))
    if(limit == 0):
        exit()

    Mav.Takeoff()


def Delay():
    print("delay")
    delay = time.time()
    data = 0
    co2_data = 0

    while time.time() - delay < 10:
        data = RW.Serial_read(py_serial, Rece, True)

        if(len(data) != 0):
            csv_file.append(data)
            if(co2_data == 0):
                co2_data = data[7]
            else:
                co2_data = co2_data * 0.5 + data[7] * 0.5

    Environment_Average.append(co2_data)
    print("delay off")

def main():
    while True:
        check = 0
        index = 0
        Mav.mavlin.mav.send(Mav.mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, Mav.mavlin.target_system, Mav.mavlin.target_component,
                                                                             Mav.mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[0].x,Send[0].y,-Send[0].z, 0,0,0, 0,0,0, 0,0))
        while True:
            RW.Serial_read(py_serial, Rece, False)
            Mav.Request()
            if(MC.nextPostionMoveCheck(Send, index, check, Mav.msg)):
                Delay()
                check = 0
                index += 1
                if(index > Send.__len__() -1 ):
                    break
                Mav.mavlin.mav.send(Mav.mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, Mav.mavlin.target_system, Mav.mavlin.target_component,
                                                                                Mav.mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[index].x,Send[index].y,-Send[index].z, 0,0,0, 0,0,0, 0,0))
            else:
                check = 1
        
        Send.clear()
        Environment_total_Ave.append(Environment_Average)
        print(Environment_total_Ave)

        if(MC.nextCenterMove(Environment_Average, Send)):
            break

        Environment_Average.clear()


if(__name__ == "__main__"):
    setup()
    StartTime = time.time()
    print(StartTime)
    main()

    Mav.HomeLand()

    py_serial.close()
    print(time.time()-StartTime)
    print(Environment_total_Ave)

    csv_file = np.array(csv_file)
    df = pd.DataFrame(csv_file)
    df.to_csv('data.csv', index=False, header=["time", "Lat","Lon", "Alt", "LPG", "CH4", "CO", "CO2", "NO2", 'PM1_0', 'PM2_5', "PM10_0"])