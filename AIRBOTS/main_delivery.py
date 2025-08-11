import sys
import os
import asyncio
from mavsdk import mission

# This ensures that we can import modules from the parent 'DRONE' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import our custom modules
from AIRBOTS.core.px4_connector import PX4Interface
from AIRBOTS.payload.servo_controller import PayloadSystem
from AIRBOTS.payload.audio_alert import AlertSystem
from AIRBOTS.comms.inter_drone_api import DeliveryComms

async def wait_for_health(drone):
    """
    Awaits for the drone to report that it has a healthy GPS lock and a
    valid home position before allowing any flight operations.
    """
    print("[PRE-FLIGHT] Waiting for drone to be healthy and have GPS lock...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("[PRE-FLIGHT] Drone is healthy and ready.")
            return True
    return False

async def safe_return_and_land(drone, home_position):
    """
    ##! FIX for landing crash ('goto_location' error):
    # This is the robust, mission-based return and landing procedure.
    # It creates a new, one-waypoint mission to fly home before landing,
    # which is the correct and safe way to perform a controlled return.
    """
    print("[RETURN] Starting safe return and landing procedure...")
    
    return_mission_items = [
        mission.MissionItem(
            home_position.latitude_deg, home_position.longitude_deg, 15, 7,
            is_fly_through=False, gimbal_pitch_deg=0, gimbal_yaw_deg=0,
            camera_action=mission.MissionItem.CameraAction.NONE,
            loiter_time_s=3, acceptance_radius_m=5.0, yaw_deg=float('nan'),
            camera_photo_interval_s=0, camera_photo_distance_m=0
        )
    ]
    
    await drone.mission.clear_mission()
    await drone.mission.upload_mission(mission.MissionPlan(return_mission_items))
    
    print("[RETURN] Flying back to home location...")
    await drone.mission.start_mission()
    
    while not await drone.mission.is_mission_finished():
        await asyncio.sleep(1)

    print("[RETURN] Arrived above home location. Initiating final descent.")
    await asyncio.sleep(1)
    await drone.action.land()
    
    async for in_air in drone.telemetry.in_air():
        if not in_air:
            print("[RETURN] Drone has landed successfully.")
            break
        await asyncio.sleep(1)

async def fly_delivery_route(drone, locations: list, home_position):
    """
    Builds and flies ONE multi-point mission to all locations, and then
    safely returns to land. This is the final, robust version.
    """
    if not locations:
        print("[MISSION] No locations to deliver to. Mission complete.")
        return

    payload_system = PayloadSystem()
    alert_system = AlertSystem()
    
    await wait_for_health(drone)

    # --- Build ONE mission plan with ALL survivor locations ---
    print(f"[MISSION] Creating a {len(locations)}-point delivery mission...")
    mission_items = []
    for loc in locations:
        mission_items.append(
            mission.MissionItem(
                loc['lat'], loc['lon'], 15, 8, is_fly_through=False, gimbal_pitch_deg=-90,
                gimbal_yaw_deg=0, camera_action=mission.MissionItem.CameraAction.NONE,
                loiter_time_s=5, acceptance_radius_m=2.0, yaw_deg=float('nan'),
                camera_photo_interval_s=0, camera_photo_distance_m=0
            )
        )
    
    await drone.mission.clear_mission()
    await drone.mission.upload_mission(mission.MissionPlan(mission_items))
    print("[MISSION] Multi-point mission uploaded.")

    print("[MISSION] Arming drone...")
    await drone.action.arm()
    print("[MISSION] Waiting for arm confirmation...")
    async for is_armed in drone.telemetry.armed():
        if is_armed:
            print("[MISSION] Drone is confirmed armed.")
            break
        await asyncio.sleep(0.5)

    print("[MISSION] Starting multi-point delivery mission...")
    await drone.mission.start_mission()
    await asyncio.sleep(1)

    # --- THIS IS THE CORRECTED, ROBUST MISSION MONITORING LOOP ---
    # It actively checks the drone's status instead of passively waiting for a stream.
    last_serviced_waypoint = -1
    while not await drone.mission.is_mission_finished():
        try:
            mission_progress = await drone.mission.mission_progress().__anext__()
            
            # Note: progress.current is the *next* waypoint. We drop payload when we arrive at the previous one.
            serviced_waypoint = mission_progress.current - 1
            
            if serviced_waypoint > last_serviced_waypoint:
                print(f"\n[PAYLOAD] Arrived at survivor {serviced_waypoint + 1}. Releasing payload.")
                payload_system.release_package()
                alert_system.play_alert()
                last_serviced_waypoint = serviced_waypoint
                await asyncio.sleep(2) # Give time for simulated drop

        except StopAsyncIteration:
            pass # The main while loop will catch the mission end
        
        await asyncio.sleep(1)

    # The loop exits when the drone is at the final waypoint. We need to service the final payload drop.
    if len(locations) > 0 and last_serviced_waypoint < len(locations) - 1:
        print(f"\n[PAYLOAD] Arrived at final survivor location {len(locations)}. Releasing payload.")
        payload_system.release_package()
        alert_system.play_alert()

    print("\n[MISSION] All deliveries complete.")
    await safe_return_and_land(drone, home_position)

async def run_standby_and_collect_mode(connection_string: str):
    """
    ##! NEW LOGIC: Collects all survivor locations and waits for the 'go' signal.
    """
    comms_receiver = DeliveryComms()
    survivor_locations = []
    
    async with PX4Interface(connection_string) as drone:
        home_position = await drone.telemetry.home().__anext__()
        print(f"[STANDBY] Home position locked: lat={home_position.latitude_deg:.6f}, lon={home_position.longitude_deg:.6f}")

        print("[STANDBY] Delivery drone is on standby, collecting coordinates...")
        
        while True:
            message = comms_receiver.check_for_message()
            if message:
                if message.get('type') == 'survivor_location':
                    survivor_locations.append({'lat': message['lat'], 'lon': message['lon']})
                    print(f"[STANDBY] Location {len(survivor_locations)} received and saved.")
                elif message.get('type') == 'scout_mission_complete':
                    print("[STANDBY] 'Scout Mission Complete' signal received. Starting delivery run.")
                    break
            await asyncio.sleep(1)
        
        await fly_delivery_route(drone, survivor_locations, home_position)
        
        print("\n[SYSTEM] Full operation complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the Delivery drone in standby mode.")
    parser.add_argument('--port', type=int, default=14542, help='MAVLink UDP port for the Delivery drone.')
    args = parser.parse_args()
    connection_str = f"udp://:{args.port}"
    try:
        asyncio.run(run_standby_and_collect_mode(connection_str))
    except Exception as e:
        print(f"[FATAL ERROR] The script encountered an unexpected error: {e}")