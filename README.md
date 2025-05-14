# Disaster Management Drone Mission

## Overview
This project enables a drone to autonomously scan disaster-affected areas, detect survivors using YOLOv8, and log their locations.

## Requirements
- Raspberry Pi 4
- Pi Camera Module
- DroneKit-compatible flight controller (e.g., Pixhawk)
- Speaker (3.5mm or USB)
- Python 3.7+

## Setup
1. Install dependencies:  
   `pip install -r requirements.txt`
2. Place your YOLOv8 model as `yolov8n_survivor.onnx`.
3. Add an alert sound as `alert.wav`.
4. Connect hardware and run:  
   `python disaster_mission.py`

## Files
- `disaster_mission.py`: Main mission script
- `requirements.txt`: Python dependencies
- `alert.wav`: Audio alert
- `yolov8n_survivor.onnx`: YOLOv8 model
- `mission_log.csv`: Output log (auto-generated)
