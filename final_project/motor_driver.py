import RPi.GPIO as GPIO
import time

class Motor():
    
    def __init__(self, control_pin_1, control_pin_2, control_pin_3):
        
        self.control_pin_1 = control_pin_1
        self.control_pin_2 = control_pin_2
        self.control_pin_3 = control_pin_3

        GPIO.setup(self.control_pin_1, GPIO.OUT)
        GPIO.setup(self.control_pin_2, GPIO.OUT)
        GPIO.setup(self.control_pin_3, GPIO.OUT)

        self.pwm = GPIO.PWM(self.control_pin_3, 100)
        self.pwm.start(0)

    def forward_rot(self, perc):
        GPIO.output(self.control_pin_1, True)
        GPIO.output(self.control_pin_2, False)
        self.pwm.ChangeDutyCycle(perc)
        GPIO.output(self.control_pin_3, True)

    def stop_rot(self):
        GPIO.output(self.control_pin_1, False)
        GPIO.output(self.control_pin_2, False)
        GPIO.output(self.control_pin_3, False)

    def backward_rot(self, perc):
        GPIO.output(self.control_pin_1, False)
        GPIO.output(self.control_pin_2, True)
        self.pwm.ChangeDutyCycle(perc)
        GPIO.output(self.control_pin_3, True)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    left_motor = Motor(21, 20, 16)
    right_motor = Motor(13, 19, 26)

    try:
        for speed in range(25, 51):
            left_motor.forward_rot(speed)
            time.sleep(0.2)

        #right_motor.stop_rot()

        for speed in range(25, 51):
            left_motor.backward_rot(speed)
            time.sleep(0.2)

        left_motor.stop_rot()

    except KeyboardInterrupt:
        print("ctrl-c stop")
    
    finally:
        GPIO.cleanup()
