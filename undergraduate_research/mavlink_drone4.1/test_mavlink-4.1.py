import ToCsv
import time
import SerialRW
import MoveCoordinates as MC
import testMavlink as testmv

Mav = testmv.mavlink()
Mav.mavlin.wait_heartbeat()

RW = SerialRW.Serial('COM6')

Rece = []
Send = []
csv_file = []
Environment_total_Ave = []
Environment_Average = []
StartTime = 0
filename = 'pm10_10.csv'

def setup():
    if RW.port.isOpen() == False: #시리얼 포트가 open인지 확인
        RW.port.open() #시리얼 포트를 연다

    MC.Move_Append(Send)
    while True:
        RW.Serial_data_reset(Rece, True)

        limit = int(input("data check : "))
        if(limit == 0):
            exit()
        elif(limit == 1):
            RW.SensorReset()
        else:
            break

    Mav.Takeoff()
    RW.droneTakeoff()

def Delay():
    print("delay")
    delay = time.time()
    data = 0
    co2_data = 0

    while time.time() - delay < 10:
        data = RW.Serial_read(Rece, True)[0]
        
        if(len(data) != 0):
            Mav.Global_Request(data)
            data.append(round(time.time()-StartTime, 1))
            csv_file.append(data)
            if(co2_data == 0):
                co2_data = data[11]
            else:
                co2_data = co2_data * 0.5 + data[11] * 0.5

    Environment_Average.append(co2_data)
    ToCsv.tocsv(csv_file, filename)

    print("delay off")

def main():
    while True:
        check = 0
        index = 0
        Mav.mavlin.mav.send(Mav.mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, Mav.mavlin.target_system, Mav.mavlin.target_component,
                                                                             Mav.mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[0].x,Send[0].y,-Send[0].z, 0,0,0, 0,0,0, 0,0))
        RW.Serial_write(index, Send)

        while True:
            RW.Serial_read(Rece, False)
            Mav.Local_Request()
            if(MC.nextPostionMoveCheck(Send, index, check, Mav.msg)):
                Delay()
                check = 0
                index += 1
                if(index > Send.__len__() -1 ):
                    break
                Mav.mavlin.mav.send(Mav.mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, Mav.mavlin.target_system, Mav.mavlin.target_component,
                                                                                Mav.mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), Send[index].x,Send[index].y,-Send[index].z, 0,0,0, 0,0,0, 0,0))
                RW.Serial_write(index, Send)
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
    # RW.droneHomeLand(Rece, False)

    RW.port.close()
    print(time.time()-StartTime)
    print(Environment_total_Ave)

    ToCsv.tocsv(csv_file, filename)
