
from pymavlink import mavutil

class MAVComms:
    def __init__(self):
        self.master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
    
    def send_survivor_coords(self, lat, lon):
        self.master.mav.command_long_send(
            target_system=self.master.target_system,
            target_component=self.master.target_component,
            command=mavutil.mavlink.MAV_CMD_USER_1,
            confirmation=0,
            param1=lat,
            param2=lon,
            param3=0, param4=0, param5=0, param6=0, param7=0
        )
