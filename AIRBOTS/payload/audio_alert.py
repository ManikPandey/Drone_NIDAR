# payload/audio_alert.py

import os

SIMULATION = os.environ.get("AIRBOTS_SIM", "1") == "1"

if not SIMULATION:
    import pygame

class AlertSystem:
    def __init__(self):
        if SIMULATION:
            print("[SIM] AlertSystem: Initialized (simulation mode).")
        else:
            print("[HW] AlertSystem: Initializing pygame mixer.")
            pygame.mixer.init()
            self.alert = pygame.mixer.Sound('drop_alert.wav')

    def play_alert(self, duration=3):
        if SIMULATION:
            print(f"[SIM] AlertSystem: Simulating audio alert playback for {duration} seconds.")
            print("[TEST] Audio alert SIMULATION SUCCESS")
            return True
        else:
            try:
                print("[HW] AlertSystem: Playing hardware audio alert.")
                channel = self.alert.play()
                pygame.time.wait(int(duration * 1000))
                print("[TEST] Audio alert HARDWARE SUCCESS")
                return True
            except Exception as e:
                print(f"[ERROR] Audio alert FAILED: {e}")
                return False


