# payload/servo_controller.py

import os

# SIMULATION flag: Set AIRBOTS_SIM=1 in your environment for simulation,
# or AIRBOTS_SIM=0 (or leave unset) for Jetson hardware
SIMULATION = os.environ.get("AIRBOTS_SIM", "1") == "1"

if not SIMULATION:
    import Jetson.GPIO as GPIO
    import time

class PayloadSystem:
    def __init__(self):
        if SIMULATION:
            print("[SIM] PayloadSystem: Initialized (simulation mode).")
        else:
            print("[HW] PayloadSystem: Initializing Jetson GPIO.")
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(33, GPIO.OUT)
            self.pwm = GPIO.PWM(33, 50)  # 50Hz for servo

    def release_package(self):
        if SIMULATION:
            print("[SIM] PayloadSystem: Simulating payload release (servo action).")
            print("[TEST] Payload release SIMULATION SUCCESS")
            return True
        else:
            try:
                print("[HW] PayloadSystem: Activating servo for payload release.")
                self.pwm.start(7.5)
                time.sleep(1)
                self.pwm.ChangeDutyCycle(10.5)
                time.sleep(2)
                self.pwm.stop()
                print("[TEST] Payload release HARDWARE SUCCESS")
                return True
            except Exception as e:
                print(f"[ERROR] Payload release FAILED: {e}")
                return False

   