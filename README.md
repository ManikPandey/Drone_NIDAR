Autonomous Dual-Drone System for Disaster Management
====================================================

_Last Updated: August 12, 2025_

An advanced, fully autonomous two-drone system designed for search and rescue operations in a disaster scenario. This project was developed for the Disaster Management mission, where a Scout drone surveys a large area to find survivors and a Delivery drone provides aid. The entire system is built on the PX4 autopilot, simulated in Gazebo, and controlled by high-level Python scripts using the MAVSDK.

1\. Mission Objective
---------------------

In response to a simulated coastal flood, this project deploys two autonomous drones to achieve the following:

1.  **Survey & Detect:** A **Scout Drone (RAZOR)** autonomously surveys a 30-hectare area, identifies stranded survivors using simulated computer vision, and geotags their locations.
    
2.  **Collect & Deliver:** A **Delivery Drone (AIRBOTS)** remains on standby, collecting a list of all survivor locations from the Scout.
    
3.  **Coordinated Response:** Once the Scout completes its survey and lands, it signals the Delivery drone, which then autonomously flies a multi-point delivery mission to drop survival kits to every survivor before safely returning to land.
    

2\. System Architecture
-----------------------

The system is composed of two primary agents communicating over a local network.

*   **RAZOR (Scout Drone):**
    
    *   **Companion Computer:** Raspberry Pi 5 (simulated).
        
    *   **Role:** Performs a wide-area lawnmower search pattern, runs a simulated detection pipeline, and acts as the primary data gatherer and mission initiator.
        
*   **AIRBOTS (Delivery Drone):**
    
    *   **Companion Computer:** NVIDIA Jetson Nano (simulated).
        
    *   **Role:** Acts as the logistics and aid delivery agent. It remains on standby until tasked by the Scout drone.
        
*   **Software Stack:**
    
    *   **Autopilot:** PX4 SITL (v1.16.0)
        
    *   **Simulator:** Gazebo Classic (v11.15.1)
        
    *   **Control API:** MAVSDK for Python
        
    *   **Language:** Python 3.8
        

3\. Core Features
-----------------

*   **Dual-Drone Cooperative System:** Two drones working together to accomplish a complex mission.
    
*   **Fully Autonomous Operation:** From takeoff to landing, all mission phases are handled by the Python scripts without manual intervention.
    
*   **Complex Autonomous Search Pattern:** The Scout drone flies a robust lawnmower pattern to ensure full coverage of the designated area.
    
*   **Real-time Inter-Drone Communication:** A lightweight UDP broadcast system allows the Scout to send survivor coordinates and a final "mission complete" signal in real-time.
    
*   **Advanced "Collect-then-Deliver" Logic:** The Delivery drone intelligently waits for the full survey to be complete before launching its optimized multi-point delivery run.
    
*   **Robust State Management & Error Handling:** The scripts include numerous safety checks, pre-flight health validation, and robust control loops to handle potential race conditions and ensure reliable mission execution.
    
*   **Stable Multi-Vehicle Simulation:** A definitive launch script provides a stable and correctly configured two-drone environment in Gazebo for consistent testing.
    

4\. Project Structure
---------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML
```
   DRONE/  
├── launch_dual_sim.sh           # The definitive script to launch the simulation  
├── requirements.txt             # All Python dependencies  
├── README.md                    # This file  
│  ├── RAZOR (Scout)/  
│   ├── main_scout.py              # Main mission script for the Scout drone  
│   ├── core/
|   │   └── px4_connector.py       # MAVSDK connection manager  
│   ├── vision/
│   │   └── survivor_detector.py   # Simulated survivor detection module  
│   └── comms/  
│       └── inter_drone_api.py     # Shared communication module  
│  └── AIRBOTS (Delivery)/      
|   ├── main_delivery.py           # Main mission script for the Delivery drone      
|   ├── core/      
|   │   └── px4_connector.py       # MAVSDK connection manager      
|   ├── payload/      
|   ├   ├── servo_controller.py    # Logic for payload drop mechanism      
|   │   └── audio_alert.py         # Logic for audio alerts      
|   └── comms/          
      └── inter_drone_api.py     # Shared communication module 
```      

5\. Setup and Installation
--------------------------

### Prerequisites

*   A working PX4 development environment for SITL simulation (Ubuntu 20.04 recommended). Follow the official [PX4 Developer Guide](https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu.html).
    
*   Gazebo Classic (v11).
    
*   Python 3.8 or newer.
    

### Installation Steps

1.  git clone cd DRONE
    
2.  python3 -m venv airbots-envsource airbots-env/bin/activate
    
3.  **requirements.txt:**mavsdkultralyticstorchopencv-pythonnumpy**Install Command:**pip install -r requirements.txt
    

6\. How to Run the Full Simulation
----------------------------------

The entire end-to-end mission can be run using three terminals. All commands should be run from the root DRONE/ directory.

### Step 1: Launch the Simulation Environment

In your **first terminal**, run the definitive launch script. This will start Gazebo and spawn both drones in their correct, separate starting positions.

`   # Make sure the script is executable first: chmod +x launch_dual_sim.sh  ./launch_dual_sim.sh   `

Wait for the script to finish and for the Gazebo window to appear with two drones.

### Step 2: Run the Scout Drone (RAZOR)

In your **second terminal** (with the airbots-env activated), run the Scout's main script. It will connect to the first drone on port 14541.

`   source airbots-env/bin/activate  python3 ./RAZOR/main_scout.py --port 14541   `

The Scout drone will take off and begin its lawnmower search pattern, printing detection coordinates as it finds them.

### Step 3: Run the Delivery Drone (AIRBOTS)

In your **third terminal** (with the airbots-env activated), run the Delivery drone's main script. It will connect to the second drone on port 14542.

`   source airbots-env/bin/activate  python3 ./AIRBOTS/main_delivery.py --port 14542   `

The Delivery drone will start in standby mode, printing each survivor coordinate it receives. After the Scout lands and sends the "mission complete" signal, the Delivery drone will automatically begin its multi-point delivery mission.

7\. Next Steps
--------------

With the full mission logic validated in the simulator, the project is now ready for **Phase 4: Hardware Integration**. This involves:

*   Deploying the code to the physical Raspberry Pi and Jetson Nano companion computers.

*   Connecting to the physical PX4 flight controller.
    
*   Performing bench tests (props-off) to validate sensor data, payload mechanisms, and motor outputs.
    
*   Conducting controlled field trials.

## Copyright

© 2025 Manik Pandey. All rights reserved.

This drone project and its related materials are the intellectual property of Manik Pandey.  
Unauthorized reproduction, distribution, or use of any content is strictly prohibited.

