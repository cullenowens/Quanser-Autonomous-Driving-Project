# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports
"""
sensor_interfacing.py

Skills acivity code for sensor interfacing lab guide.
Students will read sensor information and characterize the noise of the IMU in
the QCar.
Please review Lab Guide - Sensor Interfacing PDF
"""

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
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : SensorInterfacing Class Setup

class sensorInterfacing():
    def __init__(self, taskRate,specifiedSamples):

        # QCar DAQ configuration
        self.readRate = int(taskRate) #Hz
        self.samples  = int(specifiedSamples)
        self.mode     = "read"

        # Configure QCar properties
        self.myQCar = QCar(frequency = self.readRate, readMode = 1)

        # Variable for saving sensor readings
        self.accelerometerData = np.zeros(3)
        self.gyroscopeData     = np.zeros(3)

        #Preallocate Arrays for recording data
        self.plotData = np.zeros((self.samples,6))
        self.time = np.zeros(self.samples)

        '''# Define scopes for plotting
        txt = "Accelerometer Data Scope"
        self.accelPlot = MultiScope(title=txt, rows=1, cols=1, fps=taskRate)
        self.accelPlot.addAxis(row = 0,col= 0,
                            timeWindow=int(self.samples*(1/self.readRate)),
                            yLabel='m/s^2',
                            xLabel='time (s)')

        self.accelPlot.axes[0].attachSignal(name = 'Accel in x')
        self.accelPlot.axes[0].attachSignal(name = 'Accel in y')
        self.accelPlot.axes[0].attachSignal(name = 'Accel in z')
        self.accelPlot.axes[0].yLim = (-11, 11)

        txt = "Gyroscope Data Scope"
        self.gyroPlot = MultiScope(title=txt,rows=1, cols=1, fps=taskRate)

        self.gyroPlot.addAxis(row =0, col = 0,
                            timeWindow=int(self.samples*(1/self.readRate)),
                            yLabel='rad/s',
                            xLabel='time (s)')

        self.gyroPlot.axes[0].attachSignal(name = 'Gyro in x')
        self.gyroPlot.axes[0].attachSignal(name = 'Gyro in y')
        self.gyroPlot.axes[0].attachSignal(name = 'Gyro in z')
        self.gyroPlot.axes[0].yLim = (-2.5, 2.5)'''


    # Timing function used to send timestamp to sigmoid generator.
    def elapsedTime(self,startTime):
        return time.time()-startTime

    def sensor_read(self):
        t0       = time.time()
        loopTime = self.samples*(1/self.readRate) # Simulation Time
        print(f"Sim time: {loopTime:.1f} seconds")
        self.timeStamp = 0

        # Run the data logging only for the length of time specified
        i = 0
        try:
            while i < self.samples:
                if self.mode == "read":
                    if self.timeStamp < loopTime/2:
                        self.myQCar.write(throttle=0.075, steering=0.5)
                    if self.timeStamp >= loopTime/2:
                        self.myQCar.write(throttle=0.075, steering=-0.5)


        # ============  SECTION B - Sensor Reading and Data Parsing =============
                self.timeStamp = self.elapsedTime(t0)

                # implementation for parsing out the IMU information
                self.myQCar.read()
                accel_data = self.myQCar.accelerometer
                gyro_data = self.myQCar.gyroscope
                self.plotData[i, 0:3] = accel_data
                self.plotData[i, 3:6] = gyro_data
                self.time[i] = self.timeStamp

                '''# Data sent to scope class for visualization
                self.accelPlot.axes[0].sample(self.timeStamp,
                                    [self.accelerometerData[0],
                                    self.accelerometerData[1],
                                    self.accelerometerData[2]].copy())

                self.gyroPlot.axes[0].sample(self.timeStamp,
                                    [self.gyroscopeData[0],
                                    self.gyroscopeData[1],
                                    self.gyroscopeData[2]].copy())
                                    
                self.accelPlot.refresh()
                self.gyroPlot.refresh()
                                    '''

                i += 1
        finally:
            self.myQCar.write(throttle=0, steering=0)
            print(f"Collected {i} Samples")
            print("Time:", self.time[:10])
            print("Time range:", self.time.min(), self.time.max())

            print("Accelerometer samples:\n", self.plotData[:5, 0:3])
            print("Gyroscope samples:\n", self.plotData[:5, 3:6])

        if self.mode == "read":
            self.plot_sensor_data()

    def plot_sensor_data(self):
        # Accelerometer data
        fig1, ax1 = plt.subplots()

        ax1.plot(self.time, self.plotData[:, 0], label="Accel X")
        ax1.plot(self.time, self.plotData[:, 1], label="Accel Y")
        ax1.plot(self.time, self.plotData[:, 2], label="Accel Z")

        ax1.set_title("Accelerometer Data")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel(r"Acceleration (m/s$^2$)")
        ax1.set_ylim(-11, 11)
        ax1.grid()
        ax1.legend()

        # Gyroscope data
        fig2, ax2 = plt.subplots()

        ax2.plot(self.time, self.plotData[:, 3], label="Gyro X")
        ax2.plot(self.time, self.plotData[:, 4], label="Gyro Y")
        ax2.plot(self.time, self.plotData[:, 5], label="Gyro Z")

        ax2.set_title("Gyroscope Data")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Angular velocity (rad/s)")
        ax2.set_ylim(-2.5, 2.5)
        ax2.grid()
        ax2.legend()

        plt.show()

    def sensor_stats(self):

        # ========== SECTION C - Statistical Properties ==========
        '''mu = np.zeros(6)
        var = np.zeros(6)'''
        mu = np.mean(self.plotData, axis=0)
        var = np.mean(self.plotData, axis=0)
        
        # implementation for calculating miu and variance

        print("Mean: ", mu)
        print("Variance: ",var)

        # ========== SECTION D - Data Plotting  ==========
        # Example plot for gyroscope z values:
        fig1 = plt.figure()
        plt.plot(self.time, self.plotData[:,5])
        plt.title("Gyro z-axis data")
        plt.xlabel('time (s)')
        plt.ylabel(r'$\omega_z$ (rad/s)')
        plt.grid()

        fig2 = plt.figure()
        plt.hist(self.plotData[:,5], bins=9)
        plt.title("Gyro z-axis histogram")
        plt.xlabel(r'$\omega_z$ (rad/s)')
        plt.ylabel('samples')
        plt.grid()
        plt.show()

        #  implementation for plotting sensor characteristics


    def start(self, mode = "read"):
        self.mode = mode

        if mode == "read":
            self.sensor_read()

        if mode == "sensor_stats":
            self.sensor_read()
            self.sensor_stats()

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Main Loop
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
        sensorLab = sensorInterfacing(taskRate = 120, specifiedSamples = 600)

        ''' Students decide the activity they would like to do in the
        sensor interfacing lab
        List of current activities:
        - read (sensor interfacing skills activity)
        - sensor_stats (sensor characterization skill activity)
        '''
        sensorMode = "read"
        sensorLab.start(mode = sensorMode)
    finally:
        if not IS_PHYSICAL_QCAR:
            qlabs_setup.terminate()

        input('Experiment complete. Press any key to exit...')


#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run
if __name__ == '__main__':
    main()
#endregion