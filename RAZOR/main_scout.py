import sys
import os
import asyncio
import random
from mavsdk import mission

# This ensures that we can import modules from the parent 'DRONE' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import our custom modules
from RAZOR.core.px4_connector import PX4Interface
from RAZOR.vision.survivor_detector import SurvivorDetector
from RAZOR.comms.inter_drone_api import ScoutComms

# --- Mission Parameters ---
# These can be tuned for the mission requirements
SEARCH_ALTITUDE_M = 25
SEARCH_SPEED_MS = 7

# --- Search Area Definition ---
# This uses the original, more complex lawnmower search area as requested.
SEARCH_AREA_CORNERS = [
    {"lat": 47.3980, "lon": 8.5450},  # North-West Corner
    {"lat": 47.3980, "lon": 8.5465},  # North-East Corner
    {"lat": 47.3972, "lon": 8.5465},  # South-East Corner
    {"lat": 47.3972, "lon": 8.5450}   # South-West Corner
]

def generate_lawnmower_pattern(corners, altitude, spacing_m=20):
    """
    Generates the robust lawnmower search pattern mission.
    """
    print(f"[MISSION] Generating lawnmower pattern with {spacing_m}m spacing...")
    mission_items = []
    lat_north, lat_south = corners[0]['lat'], corners[2]['lat']
    lon_west, lon_east = corners[0]['lon'], corners[1]['lon']
    lat_spacing_deg = spacing_m / 111111.0
    current_lat = lat_north
    is_flying_eastward = True

    def create_mission_item(lat, lon):
        return mission.MissionItem(
            lat, lon, altitude, SEARCH_SPEED_MS, is_fly_through=True,
            gimbal_pitch_deg=-60, gimbal_yaw_deg=float('nan'),
            camera_action=mission.MissionItem.CameraAction.NONE,
            loiter_time_s=float('nan'), acceptance_radius_m=5.0,
            yaw_deg=float('nan'), camera_photo_interval_s=0,
            camera_photo_distance_m=0
        )

    while current_lat >= lat_south:
        if is_flying_eastward:
            mission_items.append(create_mission_item(current_lat, lon_west))
            mission_items.append(create_mission_item(current_lat, lon_east))
        else:
            mission_items.append(create_mission_item(current_lat, lon_east))
            mission_items.append(create_mission_item(current_lat, lon_west))
        current_lat -= lat_spacing_deg
        is_flying_eastward = not is_flying_eastward

    print(f"[MISSION] Generated {len(mission_items)} waypoints.")
    return mission.MissionPlan(mission_items)

async def wait_for_health(drone):
    """Waits for the drone to be healthy and have a GPS lock."""
    print("[PRE-FLIGHT] Waiting for drone to be healthy and have GPS lock...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("[PRE-FLIGHT] Drone is healthy and ready.")
            return True
    return False

async def run_scout_mission(connection_string: str):
    """
    Executes the complete scout mission with all fixes and safety checks applied.
    """
    comms_sender = ScoutComms()
    
    async with PX4Interface(connection_string) as drone:
        # --- STEP 1: PRE-FLIGHT ---
        await wait_for_health(drone)
        
        # FIX for "stale mission" concerns: Always start with a clean slate.
        print("[MISSION] Clearing any existing mission from the drone...")
        await drone.mission.clear_mission()
        
        # --- STEP 2: MISSION PLANNING & UPLOAD ---
        mission_plan = generate_lawnmower_pattern(SEARCH_AREA_CORNERS, SEARCH_ALTITUDE_M)
        print("[MISSION] Uploading new search pattern...")
        await drone.mission.upload_mission(mission_plan)
        
        # --- STEP 3: ARM AND VERIFY ---
        print("[MISSION] Arming drone...")
        await drone.action.arm()
        
        # FIX for arming race condition: We must wait for confirmation that the
        # drone is armed before starting the mission.
        print("[MISSION] Waiting for arm confirmation...")
        async for is_armed in drone.telemetry.armed():
            if is_armed:
                print("[MISSION] Drone is confirmed armed.")
                break
            await asyncio.sleep(0.5)

        # --- STEP 4: EXECUTE MISSION ---
        print("[MISSION] Starting scout mission...")
        await drone.mission.start_mission()

        # FIX for loitering: This robust 'while' loop ensures the entire pattern is
        # flown before continuing. It actively checks the drone's status.
        last_item_processed = -1
        while not await drone.mission.is_mission_finished():
            try:
                mission_progress = await drone.mission.mission_progress().__anext__()
                if mission_progress.current > last_item_processed:
                    print(f"[MISSION] Progress: Reached Waypoint {mission_progress.current + 1}/{mission_progress.total}")
                    
                    # Simulate a random detection event
                    if random.random() < 0.3:
                        position = await drone.telemetry.position().__anext__()
                        geotag_lat = position.latitude_deg
                        geotag_lon = position.longitude_deg
                        print(f"[DETECTION] Survivor detected at lat={geotag_lat:.6f}, lon={geotag_lon:.6f}")
                        comms_sender.send_survivor_location(geotag_lat, geotag_lon)
                    
                    last_item_processed = mission_progress.current
            except StopAsyncIteration:
                # This can happen if the progress stream ends; the main 'while' condition will handle it.
                pass
            await asyncio.sleep(1)
        
        # --- STEP 5: RETURN AND LAND ---
        print("[MISSION] Search pattern confirmed complete. Commanding Return to Launch...")
        await drone.action.return_to_launch()

        print("[MISSION] Waiting for drone to land at home...")
        async for in_air in drone.telemetry.in_air():
            if not in_air:
                print("[MISSION] Scout has landed.")
                break
            await asyncio.sleep(1)
        
        # --- STEP 6: FINAL SIGNAL ---
        # NEW LOGIC: Signal that the entire survey is done.
        await asyncio.sleep(2) # Brief pause for safety
        comms_sender.send_mission_complete_signal()
        
        print("[MISSION] Scout mission fully complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the Scout drone mission.")
    parser.add_argument('--port', type=int, default=14541, help='MAVLink UDP port for the Scout drone.')
    args = parser.parse_args()
    connection_str = f"udp://:{args.port}"
    
    try:
        asyncio.run(run_scout_mission(connection_str))
    except Exception as e:
        print(f"[FATAL ERROR] The script encountered an unexpected error: {e}")