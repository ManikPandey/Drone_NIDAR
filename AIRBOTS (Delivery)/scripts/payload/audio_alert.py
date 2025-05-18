
import pygame

class AlertSystem:
    def __init__(self):
        pygame.mixer.init()
        self.alert = pygame.mixer.Sound('drop_alert.wav')
    
    def play_alert(self, duration=3):
        channel = self.alert.play()
        pygame.time.wait(int(duration * 1000))
