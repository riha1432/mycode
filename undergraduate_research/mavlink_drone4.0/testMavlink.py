from pymavlink import mavutil
from pymavlink.dialects.v20 import common
import time

class mavlink:
    def __init__(self):
        self.mavlin = mavutil.mavlink_connection('tcp:localhost:5763')
        self.msg = 0
        self.mavutil = mavutil
    
    def Request(self):
        self.mavlin.mav.command_long_send(
            self.mavlin.target_system,
            self.mavlin.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,  # confirmation
            mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED,
            0, 0, 0, 0, 0, 0  # unused parameters
        )

        self.msg = self.mavlin.recv_match(type = 'LOCAL_POSITION_NED',blocking=True)
        self.msg.z = -self.msg.z
    
    def Takeoff(self):
        time.sleep(3)
        self.mavlin.set_mode_apm(4, 1, 1)
        print("gui")
        time.sleep(4)
        self.mavlin.mav.command_long_send(self.mavlin.target_system, self.mavlin.target_component, 
                            common.MAV_CMD_COMPONENT_ARM_DISARM,0, 1,0,0,0,0,0,0)
        print("arm")
        time.sleep(5)
        self.mavlin.mav.command_long_send(self.mavlin.target_system, self.mavlin.target_component,
                                common.MAV_CMD_NAV_TAKEOFF, 0, 0,0,0,0,0,0,10)
        print("take off")
        time.sleep(7)
    
    def HomeLand(self):
        time.sleep(3)
        self.mavlin.set_mode_apm(6, 1, 1)
        print("home")

        while True:
            self.Request()
            if abs(0 - self.msg.x) < 1 and abs(0 - self.msg.y) < 1:
                break

        self.mavlin.set_mode_apm(9, 1, 1)
        print("land")
