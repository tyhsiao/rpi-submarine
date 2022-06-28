import RPi.GPIO as GPIO
import time
from time import process_time, sleep

class Pump_Valve_Combo():
    
    def __init__(self, pump_enable, valve_enable):
        
        self.pump_enable = pump_enable
        self.valve_enable = valve_enable

        GPIO.setup(self.pump_enable, GPIO.OUT)
        GPIO.setup(self.valve_enable, GPIO.OUT)

    def start_pump(self):
        GPIO.output(self.pump_enable, True)

    def stop_pump(self):
        GPIO.output(self.pump_enable, False)

    def open_valve(self):
        GPIO.output(self.valve_enable, True)

    def close_valve(self):
        GPIO.output(self.valve_enable, False)
        
    def fill(self):
    
        self.open_valve()
        self.start_pump()
        
        time.sleep(3)
        self.hold()

    
    def hold(self):
        self.open_valve()
        self.stop_pump()
        
    def release(self):
        self.close_valve()
        self.stop_pump()

if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BCM)
    pump = Pump_Valve_Combo(24, 23)

    try:
        pump.fill()
        time.sleep(5)
        pump.hold()
        time.sleep(10)
        pump.release()
    except KeyboardInterrupt:
        print("ctrl-c stop")
    
    finally:
        GPIO.cleanup()
