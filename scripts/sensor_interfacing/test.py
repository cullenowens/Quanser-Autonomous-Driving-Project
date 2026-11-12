import time

from Libraries.pal.products.qcar import QCar, IS_PHYSICAL_QCAR
from Libraries.pal.utilities.scope import Signal
from threading import Thread

if not IS_PHYSICAL_QCAR:
    import qlabs_setup as qlabs_setup
    qlabs_setup.setup()

Signal.maxChunks = 1500


class sensorInterfacing():
    def __init__(self, loopTime:int, readRate=120):

        # QCar DAQ configuration
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
            if self.timeStamp < int(self.loopTime/2):
                self.myQCar.write(throttle=0.9, steering=0.5)
            elif self.timeStamp >= int(self.loopTime/2):
                self.myQCar.write(throttle=0.9, steering=-0.5)

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
        sensorLab = sensorInterfacing(8)

        sensorLab.start()
    finally:
        if not IS_PHYSICAL_QCAR:
            qlabs_setup.terminate()

        input('Experiment complete. Press any key to exit...')

if __name__ == '__main__':
    main()