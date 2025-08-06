# Disaster Management Drone Mission

## Overview
This project develops a fully autonomous dual-drone system to support disaster management operations:

- **Scout Drone:** Autonomously surveys disaster-affected areas from high altitude (~30m), uses onboard YOLOv8 machine learning model to detect people in need, geo-tags detections on a map, and communicates detection locations to a base station or directly to the supply drone.
- **Supply Drone:** Receives geotagged survivor locations, autonomously flies to each site, hovers at low altitude (~5m), performs real-time ML verification, drops payloads (e.g., medical supplies), and returns safely to the launch point.

All mission control and drone interaction use PX4 flight stack and MAVSDK with Python for flexible autonomous navigation, mission uploading, and real-time telemetry.

## Features Completed So Far

- Robust **PX4 SITL simulation setup** with Gazebo for initial testing.
- Implementation of asynchronous Python context manager for drone connection and mission handling.
- Autonomous mission scripts allowing:
  - Takeoff,
  - Mission waypoint upload with hover/drop-off commands,
  - Precise simulated payload release and audio alert playback,
  - Safe Return-To-Launch (RTL) with smooth landing.
- Adaptation of MissionItem parameters ensuring waypoint acceptance in simulation (e.g., altitude, acceptance radius, loiter time).
- Handling of MAVSDK-specific connection delays and system info retrieval.
- Thorough mission progress tracking and logging.
- Designed multi-stage mission profiles that support hovering instead of landing at drop points to preserve home location for RTL.
- Detailed troubleshooting and mitigation of PX4/MAVSDK quirks such as mission waypoint spacing, home repositioning after disarming, and RTL command behavior.
- Guidance and best practices for smooth, precise landings including lowered speeds and hover stabilization.
- Roadmap and architectural planning for integration of onboard ML (YOLOv8) for real-time person detection.
- Step-by-step ML integration plan including camera capture, inference, geotagging with telemetry, and communication of detection data.
- Simulation-validated workflow from autonomous scout drone detection to payload drone delivery.

## Hardware Requirements
- PX4-compatible flight controller (e.g., Pixhawk)
- Onboard computer (NVIDIA Jetson TX2/TX2i, Jetson Nano, or Raspberry Pi 4)
- CSI or USB camera module for video capture
- Payload release mechanism (servo or motor-actuated)
- Audio output device for alerts

## Software Stack & Dependencies

- Python 3.7+ with:
  - `mavsdk` for drone control and telemetry
  - `asyncio` for asynchronous mission execution
  - `ultralytics` or ONNX runtime for YOLOv8 inference
  - `opencv-python` for camera frame capture and processing
- PX4 autopilot software and SITL Gazebo simulation environment for initial testing
- Optional ROS2 or custom UDP/MAVLink layers for inter-drone communication and detection data forwarding

## Setup Instructions

1. Install Python dependencies:
```python
pip install -r requirements.txt
```
2. Place your trained YOLOv8 model weights (e.g., `yolov8n_survivor.onnx`) in the project folder.
3. Include an alert sound file `alert.wav` to simulate audio feedback after payload release.
4. Connect your flight controller, onboard computer, and peripherals as per your hardware setup.
5. Run your mission script simulation or hardware mission:

```python
python3 core/autonomous_nav.py
```
6. Monitor mission logs, QGroundControl map, and terminal outputs for mission progress, detections, and payload operations.

## Project Folder Summary

| File/Folder               | Description                                       |
|--------------------------|-------------------------------------------------|
| `core/px4_connector.py`   | PX4 MAVSDK interface with async drone connection|
| `core/autonomous_nav.py`  | Main mission script supporting autonomous missions with payload drop and RTL |
| `payload/servo_controller.py` | Simulated and real payload release control logic |
| `payload/audio_alert.py`        | Audio alert playback for mission notifications |
| `yolov8n_survivor.onnx`   | Trained ML model weights for people detection    |
| `alert.wav`               | Audio file played upon payload delivery          |
| `requirements.txt`        | Python package dependencies                       |
| `mission_log.csv`         | Auto-generated logs of mission progress and detections |
| `README.md`               | Project overview and usage instructions           |

## Next Steps

- Integrate real-time camera frame capture to feed live vision inference onboard the scout drone.
- Complete onboard YOLOv8 model inference pipeline and tie detections to telemetry data for geo-tagging.
- Develop robust communication protocols (ROS2 topics, MAVLink messages, UDP/Socket) for scout → supply drone detection handoff.
- Expand mission management to dynamically handle multiple detected sites.
- Conduct hardware-in-the-loop testing and field trials.
- Refine landing approaches, failsafes, and improve mapping user interface.

**This README reflects the project's current state, combining your autonomous drone simulation progress, ML detection prep, and the disaster relief mission scenario.**  
Please let me know if you would like me to generate a full example mission script, vision inference demo code, or detailed setup instructions for the ML pipeline next!
