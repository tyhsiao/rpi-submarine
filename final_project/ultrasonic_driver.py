import RPi.GPIO as GPIO
import time

class Ultrasonic():
    
    def __init__(self, trigger, echo):

        self.v = 340
        self.trigger = trigger
        self.echo = echo

        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def measure(self):
        GPIO.output(self.trigger, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(0.00002)
        GPIO.output(self.trigger, GPIO.LOW)
        pulse_start = time.time()
        first = time.time()
        while GPIO.input(self.echo) == GPIO.LOW:
            cur_time = time.time()
            if cur_time - first >=1 :
               return 0 
            pulse_start = time.time()
       
        first = time.time()
        pulse_end = time.time()
        while GPIO.input(self.echo) == GPIO.HIGH:
            cur_time = time.time()
            if cur_time - first >=1 :
                return 0
            pulse_end = time.time()
        t = pulse_end - pulse_start
        d = t * self.v
        d = d/2
        return d*100



if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    ultrasonic = Ultrasonic(5, 6)

    try:

        while(1):
            print(ultrasonic.measure())

    except KeyboardInterrupt:
        print("ctrl-c stop")
    
    finally:
        GPIO.cleanup()
