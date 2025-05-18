
async def execute_mission(waypoints):
    async with PX4Interface() as drone:
        # Pre-flight checks
        await drone.action.arm()
        await drone.action.set_takeoff_altitude(15)
        
        # Mission execution
        for idx, wp in enumerate(waypoints):
            await drone.action.goto_location(
                latitude_deg=wp['lat'],
                longitude_deg=wp['lon'],
                absolute_altitude_m=15,
                yaw_deg=0
            )
            while await drone.telemetry.ground_speed() > 1.0:
                await asyncio.sleep(0.5)
            
            # Payload drop coordination
            if idx == len(waypoints)-1:
                await trigger_payload_release(drone)
