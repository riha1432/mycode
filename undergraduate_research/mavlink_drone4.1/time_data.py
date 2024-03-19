import time
import SerialRW


def YearDaysTime():
    T = time.localtime(time.time())
    return str(T.tm_year)+"/"+ str(T.tm_mon)+"/"+ str(T.tm_mday)+"/"+ str(T.tm_hour)+":"+ str(T.tm_min)+":"+ str(T.tm_sec)

def Sleep(serial, t):
    s = time.time()
    while time.time() - s < t:
        if serial.readable():
            serial.read() #데이터를 한 줄 끝까지 읽는다
    
def Second():
    return time.time()

