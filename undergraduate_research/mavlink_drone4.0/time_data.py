import time

def YearDaysTime():
    T = time.localtime(time.time())
    return str(T.tm_year)+":"+ str(T.tm_mon)+":"+ str(T.tm_mday)+":"+ str(T.tm_hour)+":"+ str(T.tm_min)+":"+ str(T.tm_sec)

def Sleep(t):
    time.sleep(t)