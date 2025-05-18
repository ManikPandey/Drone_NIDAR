
import Jetson.GPIO as GPIO

class PayloadSystem:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(33, GPIO.OUT)
        self.pwm = GPIO.PWM(33, 50)  # 50Hz servo frequency
    
    def release_package(self):
        self.pwm.start(7.5)  # Neutral position
        time.sleep(1)
        self.pwm.ChangeDutyCycle(10.5)  # Release position
        time.sleep(2)
        self.pwm.stop()
