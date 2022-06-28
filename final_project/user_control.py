from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from datetime import datetime

import motor_driver
import pump_driver
import recorder_driver
import ultrasonic_driver

import RPi.GPIO as GPIO
import imutils
import time
import cv2
import os

if __name__ == '__main__':

    NONE = 0
    FORWARD = 1
    BACKWARD = 2
    
    GPIO.setmode(GPIO.BCM)

    left_motor = motor_driver.Motor(20, 21, 16)
    right_motor = motor_driver.Motor(13, 19, 26)
    pvc = pump_driver.Pump_Valve_Combo(24, 23)
    recorder = recorder_driver.Recorder()
    ultrasonic = ultrasonic_driver.Ultrasonic(5,6)
    text = "stop"

    cur_state = NONE
    help_mode = False
    record_mode = False
    inits = False
    start_dist = False
    try:
        res = (640,480)
        vs = PiVideoStream(resolution=res).start()
        time.sleep(2.0)
        

        while True:
            
            frame = vs.read()
            
            if start_dist == True:
                if dist < 30: 
                    cv2.putText(frame, dist_info , (380, 430), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

                else :
                    cv2.putText(frame, dist_info , (380, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            
            if help_mode == True:
                cv2.putText(frame, "w: forward  s: backward", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, "a: left-turn  d: right-turn", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, "power 1: 25%  2: 50% 3: 75%", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, "float: <up arrow>  sink: <down arrow>", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, "halt h: horizontal  v: vertical", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, "z: return", (10, 340), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, "q: shutdown", (10, 380), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, "r: record t: stop record", (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)

            else: 
                cv2.putText(frame, "help: Press i", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, text, (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
            #frame = imutils.resize(frame, width=400)

            if record_mode == True:
                cv2.circle( frame,(50, 50), 10, (0, 0, 255), -1)

            cv2.imshow("Live Feed", frame)
            if recorder.out != None:
                recorder.out.write(frame)
            
            command = cv2.waitKey(1) & 0xFF
            if command == ord('r'):
                recorder.start_recording(res)
                print("recording started")
                record_mode = True

            elif command == ord('t'):
                recorder.end_recording()
                print("recording ended")
                record_mode = False

            elif command == ord('m'):

                dist = ultrasonic.measure()

                start_measure = time.time()
                dist = round(dist, 1)
                start_dist = True 
                dist_info = "dist:  " + str(dist)  + " cm"

            elif command == ord('i'):
                
                left_motor.stop_rot()
                right_motor.stop_rot()
                print("help")
                pvc.hold()
                cur_state = NONE
                help_mode = True

            elif command == ord('z'):
                help_mode = False

            elif command == ord('w'):
                print("forward 50% power")
                text = "forward 50% power"
                left_motor.forward_rot(50)
                right_motor.forward_rot(50)
                cur_state = FORWARD

            elif command == ord('a'):
                text = "left turn"
                print("left-turn")
                left_motor.backward_rot(50)
                right_motor.forward_rot(50)
                cur_state = NONE

            elif command == ord('s'):
                text = "backward 50% power"
                print("backward 50% power")
                left_motor.backward_rot(50)
                right_motor.backward_rot(50)
                cur_state = BACKWARD
            
            elif command == ord('d'):
                text = "right-turn"
                print("right-turn")
                left_motor.forward_rot(50)
                right_motor.backward_rot(50)
                cur_state = NONE
            
            elif command == ord('h'):
                text = "stop"
                left_motor.stop_rot()
                right_motor.stop_rot()
                print("halt lateral movements")
                cur_state = NONE
            
            elif command == ord('1'):
                if cur_state == FORWARD:
                    text = "forward 25% power"
                    left_motor.forward_rot(25)
                    right_motor.forward_rot(25)
                elif cur_state == BACKWARD:
                    text = "backward 25% power"
                    left_motor.backward_rot(25)
                    right_motor.backward_rot(25)

            elif command == ord('2'):
                if cur_state == FORWARD:
                    text = "forward 50% power"
                    left_motor.forward_rot(50)
                    right_motor.forward_rot(50)
                elif cur_state == BACKWARD:
                    text = "backward 50% power"
                    left_motor.backward_rot(50)
                    right_motor.backward_rot(50)

            elif command == ord('3'):
                if cur_state == FORWARD:
                    text = "forward 75% power"
                    left_motor.forward_rot(75)
                    right_motor.forward_rot(75)
                elif cur_state == BACKWARD:
                    text = "backward 75% power"
                    left_motor.backward_rot(75)
                    right_motor.backward_rot(75)


            elif command == 82:
                text = "floating"
                print("float")
                pvc.fill()
                cur_state = NONE 

            elif command == 84:
                text = "sinking"
                print("sink")
                pvc.release()
                cur_state = NONE
            
            elif command == ord('v'):
                text = "halt vertical movements"
                print("halt vertical movements")
                pvc.hold()
                cur_state = NONE
            
            elif command == ord('q'):
                print("quit")
                GPIO.cleanup()
                cv2.destroyAllWindows()
                vs.stop()
                recorder.cleanup()
                cur_state = NONE
                
                break

    except KeyboardInterrupt:
        print("quit")
        GPIO.cleanup()
        cv2.destroyAllWindows()
        vs.stop()
        recorder.cleanup()
        pass

    finally:
        # run pin cleanup
        GPIO.cleanup()
        cv2.destroyAllWindows()
        vs.stop()
        recorder.cleanup()
