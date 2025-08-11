import asyncio
from mavsdk import System
from mavsdk import mission

async def smooth_landing(drone):
    """Enhanced landing procedure with vertical speed control"""
    print("🛬 Beginning smooth landing...")
    try:
        # Get initial altitude
        async for position in drone.telemetry.position():
            current_alt = position.relative_altitude_m
            break
        
        # Descend at 1 m/s until 0.5m altitude
        await drone.action.set_current_speed(1.0)
        while current_alt > 0.5:
            await drone.action.land()
            async for position in drone.telemetry.position():
                current_alt = position.relative_altitude_m
                print(f"↘️ Descending: {current_alt:.1f}m", end='\r')
                if current_alt <= 0.5: break
            await asyncio.sleep(0.1)
        
        # Final descent
        await drone.action.kill()
        print("\n🛑 Motors stopped. Landing complete!")
        
    except Exception as e:
        print(f"🚨 Landing error: {e}")
        await drone.action.emergency()

async def run():
    print("Starting connection...")
    drone = System()
    await drone.connect(system_address="udp://:14540")
    print("✅ Connection established")

    # Wait for connection and GPS
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Drone connected!")
            break
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("🌍 Global position OK")
            break

    # Define mission waypoints
    mission_items = [
        mission.MissionItem(
            47.3977419, 8.5455938, 10, 10, True,
            float('nan'), float('nan'), mission.MissionItem.CameraAction.NONE,
            float('nan'), float('nan'), float('nan'), float('nan'), float('nan')
        ),
        mission.MissionItem(
            47.3978000, 8.5458000, 12, 10, True,
            float('nan'), float('nan'), mission.MissionItem.CameraAction.NONE,
            float('nan'), float('nan'), float('nan'), float('nan'), float('nan')
        )
    ]
    mission_plan = mission.MissionPlan(mission_items)

    try:
        # Upload and execute mission
        await drone.mission.upload_mission(mission_plan)
        print("🗺️ Mission uploaded")
        await drone.action.arm()
        print("✅ Armed")
        await drone.mission.start_mission()
        print("🚀 Mission started")

        # Monitor progress
        async for progress in drone.mission.mission_progress():
            print(f"📈 Progress: {progress.current}/{progress.total}")
            if progress.current == progress.total:
                print("✅ Mission complete!")
                break

        # Smooth landing sequence
        await smooth_landing(drone)

    except Exception as e:
        print(f"🚨 Critical error: {e}")
        await drone.action.emergency()

    finally:
        # Graceful shutdown
        await asyncio.sleep(1)
        await drone.action.disarm()
        print("🔋 Disarmed")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n🛑 Mission interrupted by user")
    # finally:
    #     # Prevent thread join error
    #     asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.5))
