
from mavsdk import System
import asyncio

class PX4Interface:
    def __init__(self):
        self.drone = System()
        
    async def connect(self):
        await self.drone.connect(system_address="serial:///dev/ttyACM0:115200")
        print(f"Connected to PX6X FCB: {await self.drone.system_info.version}")

    async def set_flight_mode(self, mode: str):
        await self.drone.action.set_return_to_launch_altitude(15)
        await self.drone.action.hold()
        await self.drone.action.set_takeoff_altitude(15)
