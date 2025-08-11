import asyncio
from mavsdk import System

async def run():
    print("Starting connection...")
    drone = System()
    await drone.connect(system_address="udp://:14540")
    print("Connected call done")

    print("Waiting for connection state...")
    async for state in drone.core.connection_state():
        print(f"Connection state: {state.is_connected}")
        if state.is_connected:
            print("✅ Connected!")
            break

    print("Fetching UUID...")
    async for info in drone.info.identification():
        print(f"Drone identification: {info}")
        break

    async for info in drone.info.uuid():
        print(f"Drone UUID: {info}")
        break


    print("Arming drone...")
    await drone.action.arm()
    print("Drone armed")

    print("Taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    print("Landing...")
    await drone.action.land()

    print("Getting position...")
    async for position in drone.telemetry.position():
        print(f"Lat: {position.latitude_deg}, Lon: {position.longitude_deg}")
        break

if __name__ == "__main__":
    asyncio.run(run())
