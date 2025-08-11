# Improved mavsdk_connect.py
import asyncio
from mavsdk import System

async def run():
    drone = System()
    print("Connecting to PX4 SITL on udp://:14540 ...")
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect (timeout 30s)...")
    timeout = 30
    start = asyncio.get_event_loop().time()
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Drone connected!")
            return
        if asyncio.get_event_loop().time() - start > timeout:
            print("❌ Connection timed out after 30s.")
            return
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
