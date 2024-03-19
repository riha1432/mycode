DATARESET = 0
import Postion
import time_data as time
import serial


class Serial:
    def __init__(self,port):
        self.lpg = self.ch4 = self.co = self.co2 = self.no2 = self.pm1_0 = self.pm2_5 = self.pm10_0 = DATARESET
        self.Now_pos = Postion.Postion()
        self.port = serial.Serial(
                            port=port,
                            baudrate=57600,
                        )
        self.Ack = 0
        self.check = False
        
    def __int16(self, x):
        if(x > 0x7fff):
            x = (x - 0x1)^0xffff
            return -x
        else:
            return x
        
    def __int32(self, x):
        if(x > 0x7fffffff):
            x = (x - 0x1)^0xffffffff
            return -x
        else:
            return x
        
    def __EnvironmentDataPrint(self, data, dataprint):
        self.Now_pos.x = self.__int16((data[0]<<8) | data[1])/10.0
        self.Now_pos.y = self.__int16((data[2]<<8) | data[3])/10.0
        self.Now_pos.z = -(self.__int16((data[4]<<8) | data[5])/10.0)
        self.lat = ((data[6]<<24) | (data[7]<<16) |(data[8]<<8) |(data[9]))
        self.lon = ((data[10]<<24) | (data[11]<<16) |(data[12]<<8) |(data[13]))
        self.Alt = ((data[14]<<24) | (data[15]<<16) |(data[16]<<8) |(data[17]))
        self.v = ((data[18]<<8) | data[19])
        self.lpg = (((data[20]<<8) | data[21]) * 0.4) + self.lpg * 0.6
        self.ch4 = (((data[22]<<8) | data[23]) * 0.4) + self.ch4 * 0.6
        self.co = (((data[24]<<8) | data[25]) * 0.4) + self.co * 0.6
        self.co2 = (((data[26]<<8) | data[27]) * 0.4) + self.co2 * 0.6
        self.no2 = (((data[28]<<8) | data[29]))
        self.pm1_0 = (data[30] * 0.4) + self.pm1_0 * 0.6
        self.pm2_5 = (data[31] * 0.4) + self.pm2_5 * 0.6
        self.pm10_0 = (data[32] * 0.4) + self.pm10_0 * 0.6
        
        lat = self.__int32(self.lat)/100.0
        lon = self.__int32(self.lon)/100.0
        galt = self.__int32(self.Alt)/100.0
        v = self.__int16(self.v)/1000.0
        lpg = round(self.__int16(self.lpg)/10.0, 2)
        ch4 = round(self.__int16(self.ch4)/10.0, 2)
        co = round(self.__int16(self.co)/10.0, 2)
        co2 = round(self.__int16(self.co2), 2)
        no2 = round(self.__int16(self.no2)/100.0, 2)
        pm1_0 = round(self.__int16(self.pm1_0), 2)
        pm2_5 = round(self.__int16(self.pm2_5), 2)
        pm10_0 = round(self.__int16(self.pm10_0), 2)
        ack = data[33]

        if(dataprint):
            print("x : ", (self.Now_pos.x), end=' ')
            print("y : ", (self.Now_pos.y), end=' ')
            print("z : ", (self.Now_pos.z), end=' ')
            print("lat : ", lat, end=' ')
            print("lon : ", lon, end=' ')
            print("galt : ", galt, end=' ')
            print("v : ", v, end=' ')
            print("LPG : ", lpg, end=' ')
            print("CH4 : ", ch4, end=' ')
            print("CO : ", co, end=' ')
            print("Co2 : ", co2, end=' ')
            print("No2 : ", no2, end=' ')
            print("pm1.0 : ", pm1_0, end=' ')
            print("pm2.5 : ", pm2_5, 2, end=' ')
            print("pm10.0 : ", pm10_0)

        data.clear()
        return [time.YearDaysTime(), lat, lon, galt, lpg, ch4, co, co2, no2, pm1_0, pm2_5, pm10_0], ack
    
    def Serial_read(self, data, dataprint):
        if self.port.readable():
            r_msg = self.port.read() #데이터를 한 줄 끝까지 읽는다

            data.append(r_msg[0])
            if(data.__len__() >= 2):
                if( chr(data[-2]) == 'S' and chr(data[-1]) == 'T'):
                    data.clear()
                    self.check = True
                elif( chr(data[-1]) == 'E' and chr(data[-2]) == 'N' and self.check == True):
                    self.check = False
                    return self.__EnvironmentDataPrint(data, dataprint)
        return [], -1

    def __Write(self, commend, data = [], resend = 0.5):
        again = 0
        ack = -1
        self.Ack += 1
        if(self.Ack > 50):
            self.Ack = 0
        commend = commend + 'D' + chr(self.Ack) + '000E'
        print("-------------------------------------------")
        print("명령어 : ", commend)
        print("응답 번호 : ",self.Ack)
        print("-------------------------------------------")
        while True:
            while(ack == -1):
                _, ack = self.Serial_read(data, False)

            if(self.Ack == ack):
                print("===========================================")
                print("응답 응답 : ", self.Ack)
                print("수신 응답 : ", ack)
                print("응답 완료 수행")
                print("===========================================")
                break

            else:
                if(time.Second() - again > resend):
                    again = time.Second()
                    print("*******************************************")
                    print("수신 응답 : ",ack)
                    self.port.write(commend.encode('utf-8'))
                    print("전송 : ",commend.encode('utf-8'))
                    print("*******************************************")
                    ack = -1
        return

    def Serial_write(self, index, data):
        commend = 'SG1X' + str(data[index].x) + 'Y' + str(data[index].y) + 'Z' + str(data[index].z)
        self.__Write(commend)
    
    def Serial_data_reset(self, data, dataprint):
        for i in range(20):
            while True:
                if(self.Serial_read(data, dataprint)[0] != []):
                    break

    def SensorReset(self, resend = 2):
        self.__Write('SR', resend = resend)

    def droneTakeoff(self):
        time.Sleep(self.port, 3)

        self.__Write('SM1')
        print("gui")
        time.Sleep(self.port, 4)

        self.__Write('SO')
        print("arm")
        time.Sleep(self.port, 5)

        self.__Write("ST")
        print("take off")
        time.Sleep(self.port, 7)
        self.SensorReset()

    
    def droneHomeLand(self, data, dataprint):
        time.Sleep(self.port, 3)
        self.__Write('SM2')
        print("home")

        while True:
            self.Serial_read(data, dataprint)
            if abs(0 - self.Now_pos.x) < 1 and abs(0 - self.Now_pos.y) < 1:
                break

        self.__Write('SM3')
        print("land")



