import cv2
from datetime import datetime

class Recorder():

    def __init__(self):
        self.out = None

    def start_recording(self, res):
        if self.out != None:
            return
        curr_time = datetime.now()
        dts = curr_time.strftime("%Y%m%d_%H%M%S")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(f'{dts}_output.avi', fourcc, 20.0, res) 

    def end_recording(self):
        if self.out != None:
            self.out.release()
            self.out = None
        return

    def cleanup(self):
        self.end_recording()
