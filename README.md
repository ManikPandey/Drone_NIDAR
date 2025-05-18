# Disaster Management Drone System (RAZOR & AIRBOTS)

## Overview
This project implements a dual-drone system for disaster response:
- **RAZOR (Surveillance Drone)**: Autonomous aerial reconnaissance with survivor detection
- **AIRBOTS (Delivery Drone)**: Payload delivery system with AI-assisted verification

Key Features:
- Real-time video streaming with YOLOv8 object detection
- MAVLink-based inter-drone communication
- Autonomous waypoint navigation with failsafes
- ROS-integrated payload delivery system
- Cross-platform compatibility (Jetson Nano/Raspberry Pi)

## System Architecture
airbots/
├── config/
│ ├── px4_params.yaml
│ └── mavlink_channels.conf
├── scripts/
│ ├── core/
│ │ ├── px4_connector.py
│ │ ├── autonomous_nav.py
│ │ └── failsafe_manager.py
│ ├── payload/
│ │ ├── servo_controller.py
│ │ └── audio_alert.py
│ ├── vision/
│ │ ├── yolo_detector.py
│ │ └── video_stream.py
│ └── comms/
│ ├── mavlink_bridge.py
│ └── inter_drone_api.py
└── launch/
└── airbots_core.launch



## Hardware Requirements

### RAZOR (Surveillance)
- Raspberry Pi 4 (4GB+)
- Pi Camera Module v3
- Pixhawk 6X Flight Controller
- 3DR Radio Telemetry (915MHz)
- BONKA 35C 5200mAh LiPo

### AIRBOTS (Delivery)
- Jetson Nano 4GB Developer Kit
- NEO-M8N GPS with Compass
- Pixhawk Power Module 28V
- Long-Range Wireless Speaker
- 10Ah 6S4P LiPo Battery

## Software Requirements
- Python 3.8+
- PX4 v1.14.0
- ROS Noetic
- JetPack 5.1.2 (for Jetson Nano)
- CUDA 11.3

## Installation

### For Jetson Nano (AIRBOTS)
sudo apt-get install python3-pip python3-venv
pip3 install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu113



### For Raspberry Pi (RAZOR)
sudo apt-get install libatlas3-base libjasper-dev
python3 -m pip install -r requirements.txt



### Development Environment (x86)
conda create -n airbots python=3.8
conda activate airbots
pip install -r requirements.txt




## Configuration
1. Place YOLOv8 models:
   - AIRBOTS: `airbots/models/yolov8n_survivor.onnx`
   - RAZOR: `razor/models/yolov5s_survivor.pt`

2. Add audio alerts:
   - AIRBOTS: `airbots/assets/alert.wav`
   - RAZOR: `razor/assets/alert.wav`

3. Configure MAVLink channels in `config/mavlink_channels.conf`

## Usage

### Simulation Testing
Start PX4 SITL
make px4_sitl gazebo_iris

Run AIRBOTS mission simulation
python3 scripts/core/autonomous_nav.py --sim

Test RAZOR detection system
python3 razor/scripts/detection_test.py



### Field Deployment
AIRBOTS (Jetson Nano)
roslaunch airbots airbots_core.launch

RAZOR (Raspberry Pi)
python3 razor/main.py --mode autonomous


## Inter-Drone Communication
sequenceDiagram
RAZOR->>AIRBOTS: MAVLink SURVIVOR_LOCATION (lat, lon)
AIRBOTS->>RAZOR: MAVLink ACK_PAYLOAD_REQUEST
AIRBOTS->>GROUND: RTSP Video Stream
GROUND->>AIRBOTS: MAVLink PAYLOAD_CONFIRM




## Safety Features
- Low-battery RTL (Return-to-Launch)
- GPS-denied landing protocol
- Geofence enforcement
- Emergency manual override
- Hardware watchdog timer

## License
Apache 2.0 License - See [LICENSE](LICENSE)

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature`)
5. Open Pull Request

---

**Note:** Always perform hardware checks before flight operations. Maintain line-of-sight during testing.
