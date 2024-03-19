DATARESET = 0
import Postion as postion
import time_data as time
import serial

class Serial:
    def __init__(self):
        self.lpg = self.ch4 = self.co = self.co2 = self.no2 = self.pm1_0 = self.pm2_5 = self.pm10_0 = DATARESET
        self.Now_pos = postion.Postion()
        self.SerialPort = serial.Serial(
                            port='COM8',
                            # port='COM9',
                            baudrate=57600,
                        )
        
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
        self.no2 = (((data[28]<<8) | data[29]) * 0.4) + self.no2 * 0.6
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
        return [time.YearDaysTime(), lat, lon, galt, lpg, ch4, co, co2, no2, pm1_0, pm2_5, pm10_0]
    
    def Serial_read(self, serial, data, dataprint):
        if serial.readable():
            r_msg = serial.read() #데이터를 한 줄 끝까지 읽는다
            data.append(r_msg[0])
            if(data.__len__() >= 2):
                if( chr(data[-2]) == 'S' and chr(data[-1]) == 'T'):
                    data.clear()
                elif( chr(data[-1]) == 'E' and chr(data[-2]) == 'N'):
                    return self.__EnvironmentDataPrint(data, dataprint)
        return []

    def Serial_write(self, index, serial, data):
        commend = 'SG1X' + str(data[index].x) + 'Y' + str(data[index].y) + 'Z' + str(data[index].z) + 'D000E'
        print(commend)
        serial.write(commend.encode('utf-8'))
    
    def Serial_data_reset(self, serial, data, dataprint):
        for i in range(20):
            while True:
                if(self.Serial_read(serial, data, dataprint)!=[]):
                    break

    def droneTakeoff(self,serial):
        time.Sleep(3)
        serial.write(b'SM1000E')
        print("gui")
        time.Sleep(4)
        serial.write(b'SO0000E')
        print("arm")
        time.Sleep(5)
        serial.write(b"ST0000E")
        print("take off")
        time.Sleep(7)
    
    def droneHomeLand(self, serial, data, dataprint):
        time.Sleep(3)
        serial.write(b'SM2000000000E')
        print("home")

        while True:
            self.Serial_read(serial, data, dataprint)
            if abs(0 - self.Now_pos.x) < 1 and abs(0 - self.Now_pos.y) < 1:
                break

        serial.write(b'SM3000000000E')
        print("land")



