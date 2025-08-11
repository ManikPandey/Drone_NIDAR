import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
from payload.servo_controller import PayloadSystem
from payload.audio_alert import AlertSystem
from core.px4_connector import PX4Interface
from mavsdk import mission

payload_system = PayloadSystem()
alert_system = AlertSystem()

# PX4 SITL Zurich default home position and dropoff 50m NE (approx)
HOME = {"lat": 47.3977419, "lon": 8.5455938}
DROP_OFF = {"lat": 47.3981919, "lon": 8.5460438}  # ~50 meters NE

async def wait_for_global_position(drone):
    print("[MISSION] Waiting for GPS/global position health...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("[MISSION] Global position estimate OK.")
            break
        await asyncio.sleep(1)

async def execute_mission():
    async with PX4Interface() as drone:
        await wait_for_global_position(drone)

        # --------- Phase 1: Mission to DROP-OFF, at 5m hover ---------
        print("[MISSION] Uploading and flying to drop-off (zero touch-down)...")
        mission_items = [
            mission.MissionItem(
                latitude_deg=DROP_OFF['lat'],
                longitude_deg=DROP_OFF['lon'],
                relative_altitude_m=5,   # Hover at 5 meters for drop
                speed_m_s=4,
                is_fly_through=False,
                gimbal_pitch_deg=0,
                gimbal_yaw_deg=0,
                camera_action=mission.MissionItem.CameraAction.NONE,
                loiter_time_s=5,            
                camera_photo_interval_s=0,
                acceptance_radius_m=1,
                yaw_deg=0,
                camera_photo_distance_m=0
            )
        ]
        plan = mission.MissionPlan(mission_items)
        await drone.mission.upload_mission(plan)
        print("[MISSION] Arming and starting mission...")
        await drone.action.arm()
        await drone.mission.start_mission()

        # Monitor progress
        last_progress = -1
        async for mission_progress in drone.mission.mission_progress():
            if mission_progress.current != last_progress:
                print(f"[MISSION] Progress: {mission_progress.current}/{mission_progress.total}")
                last_progress = mission_progress.current
            if mission_progress.current == mission_progress.total:
                break
            await asyncio.sleep(1)

        # At drop-off, in the air, 5 meters high
        print("[MISSION] At drop-off hover. Simulating payload drop and alert (drone stays armed and in air).")
        payload_system.release_package()
        alert_system.play_alert()
        await asyncio.sleep(3)  # wait a little for effect

        # --------- Phase 2: Return to launch (RTL) ---------
        print("[MISSION] Preparing for Return-to-Launch with smooth landing...")

        # Reduce max speed for approach and landing (e.g., 1 m/s)
        await drone.action.set_maximum_speed(1.0)

        # Optional: Hover for 2 seconds before RTL to stabilize
        await drone.action.hold()
        await asyncio.sleep(2)

        # Now send RTL command
        await drone.action.return_to_launch()

        # Wait for drone to land at home
        async for in_air in drone.telemetry.in_air():
            if not in_air:
                print("[MISSION] Drone has landed at home.")
                break
            await asyncio.sleep(1)
        await drone.action.set_maximum_speed(6.0)  # back to normal cruise speed
        print("[MISSION] Reset max speed after landing.")

        print("[MISSION] Mission complete: drone returned to launch and landed.")

if __name__ == "__main__":
    asyncio.run(execute_mission())
