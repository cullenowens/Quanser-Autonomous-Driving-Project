import matplotlib.pyplot as plt
import numpy as np
import time

from Libraries.pal.products.qcar import QCar, IS_PHYSICAL_QCAR
from Libraries.pal.utilities.stream import BasicStream , Timeout
from Libraries.pal.utilities.scope import MultiScope, Signal
from threading import Thread

if not IS_PHYSICAL_QCAR:
    import scripts.qlabs_setup as qlabs_setup
    qlabs_setup.setup()

Signal.maxChunks = 1500


class sensorInterfacing():
    def __init__(self, loopTime:int, readRate=120):

        # QCar DAQ configuration
        self.mode     = "read"
        self.readRate = readRate
        self.loopTime = loopTime

        # Configure QCar properties
        self.myQCar = QCar(frequency = self.readRate, readMode = 1)


    # Timing function used to send timestamp to sigmoid generator.
    def elapsedTime(self,startTime):
        return time.time()-startTime

    def drive(self):
        t0       = time.time()
        print("Sim time: ",self.loopTime)
        self.timeStamp = 0

        # Run the data logging only for the length of time specified
        i = 0
        while self.timeStamp < self.loopTime:
            if self.mode == "read":
                if self.timeStamp < int(self.loopTime/2):
                    self.myQCar.write(throttle=0.9, steering=0.5)
                if self.timeStamp >= int(self.loopTime/2):
                    self.myQCar.write(throttle=0.9, steering=-0.5)


    # ============  SECTION B - Sensor Reading and Data Parsing =============
            self.timeStamp = self.elapsedTime(t0)
            i += 1

        self.myQCar.write(throttle=0, steering=0)


    def start(self):

        mainThread = Thread(target=self.drive)
        mainThread.start()

        time.sleep(15)
        return

def main():
    try:
        '''
        INPUTS
        taskRate = Int The frequency (Hz) at which the read/write operation
                will be performed.
        specifiedSamples = Int Number of samples saved for statistical analysis of
                        sensor data.
        '''
        # ========= SECTION A - Student Inputs for Image Interpretation ===========
        sensorLab = sensorInterfacing(8)

        ''' Students decide the activity they would like to do in the
        sensor interfacing lab
        List of current activities:
        - read (sensor interfacing skills activity)
        - sensor_stats (sensor characterization skill activity)
        '''
        sensorMode = "read"
        sensorLab.start()
    finally:
        if not IS_PHYSICAL_QCAR:
            qlabs_setup.terminate()

        input('Experiment complete. Press any key to exit...')

if __name__ == '__main__':
    main()