import time

class Postion:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

Now_pos = Postion()

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


lpg = ch4 = co = co2 = no2 = pm1_0 = pm2_5 = pm10_0 = 0
def senser_setup(serial, data):
    global Now_pos, lpg, ch4, co, co2, no2, pm1_0, pm2_5, pm10_0
    while True:
        if(Serial_read(serial, data)!=0):
            break

def dr_print(data):
    global Now_pos, lpg, ch4, co, co2, no2, pm1_0, pm2_5, pm10_0

    Now_pos.x = int16((data[0]<<8) | data[1])/10.0
    Now_pos.y = int16((data[2]<<8) | data[3])/10.0
    Now_pos.z = -(int16((data[4]<<8) | data[5])/10.0)
    lat = ((data[6]<<24) | (data[7]<<16) |(data[8]<<8) |(data[9]))
    lon = ((data[10]<<24) | (data[11]<<16) |(data[12]<<8) |(data[13]))
    Alt = ((data[14]<<24) | (data[15]<<16) |(data[16]<<8) |(data[17]))
    v = ((data[18]<<8) | data[19])
    lpg = (((data[20]<<8) | data[21]) * 0.4) + lpg * 0.6
    ch4 = (((data[22]<<8) | data[23]) * 0.4) + ch4 * 0.6
    co = (((data[24]<<8) | data[25]) * 0.4) + co * 0.6
    co2 = (((data[26]<<8) | data[27]) * 0.4) + co2 * 0.6
    no2 = (((data[28]<<8) | data[29]) * 0.4) + no2 * 0.6
    pm1_0 = (data[30] * 0.4) + pm1_0 * 0.6
    pm2_5 = (data[31] * 0.4) + pm2_5 * 0.6
    pm10_0 = (data[32] * 0.4) + pm10_0 * 0.6
    print("x : ", (Now_pos.x), end=' ')
    print("y : ", (Now_pos.y), end=' ')
    print("z : ", (Now_pos.z), end=' ')
    print("lat : ", int32(lat)/100.0, end=' ')
    print("lon : ", int32(lon)/100.0, end=' ')
    print("galt : ", int32(Alt)/100.0, end=' ')
    print("v : ", int16(v)/1000.0, end=' ')
    print("LPG : ", round(int16(lpg)/10.0, 2), end=' ')
    print("CH4 : ", round(int16(ch4)/10.0, 2), end=' ')
    print("CO : ", round(int16(co)/10.0, 2), end=' ')
    print("Co2 : ", round(int16(co2), 2), end=' ')
    print("No2 : ", round(int16(no2)/100.0, 2), end=' ')
    print("pm1.0 : ", round(int16(pm1_0), 2), end=' ')
    print("pm2.5 : ", round(int16(pm2_5), 2), end=' ')
    print("pm10.0 : ", round(int16(pm10_0), 2))
    data.clear()
    T = time.localtime(time.time())
    Tstring = str(T.tm_year)+":"+ str(T.tm_mon)+":"+ str(T.tm_mday)+":"+ str(T.tm_hour)+":"+ str(T.tm_min)+":"+ str(T.tm_sec)
    return [Tstring, lat/100.0, lon/100.0, Alt/100.0, lpg/10.0, ch4/10.0, co/10.0, co2, no2/100.0, pm1_0, pm2_5, pm10_0]

def Serial_read(serial, data):
    if serial.readable():
        r_msg = serial.read() #데이터를 한 줄 끝까지 읽는다
        data.append(r_msg[0])
        # print(data)
        if(data.__len__() >= 2):
            if( chr(data[-2]) == 'S' and chr(data[-1]) == 'T'):
                data.clear()
            elif( chr(data[-1]) == 'E' and chr(data[-2]) == 'N'):
                return dr_print(data)
    return []

def Serial_write(index, serial, data):
    commend = 'SG1X' + str(data[index].x) + 'Y' + str(data[index].y) + 'Z' + str(data[index].z) + 'D000E'
    serial.write(commend.encode('utf-8'))