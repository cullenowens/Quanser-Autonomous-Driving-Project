import threading
import time
from pynput import keyboard

import time

from Libraries.pal.products.qcar import QCar, IS_PHYSICAL_QCAR
from Libraries.pal.utilities.scope import Signal
from threading import Thread

if not IS_PHYSICAL_QCAR:
    import scripts.qlabs_setup as qlabs_setup
    qlabs_setup.setup()

Signal.maxChunks = 1500

#Keys held down
pressed_keys = set()
lock = threading.Lock()

def on_press(key):
    try:
        with lock:
            pressed_keys.add(key.char.lower())
    except AttributeError:
        if key == keyboard.Key.esc:
            with lock:
                pressed_keys.add('esc')

def on_release(key):
    try:
        with lock:
            pressed_keys.discard(key.char.lower())
    except AttributeError:
        with lock:
            pressed_keys.discard(key)

#Keyboard listener in background
listener = keyboard.Listener(on_press=on_press, on_release=on_release)


class KeyboardInterfacing():
    def __init__(self, readRate=120):

        # QCar DAQ configuration
        self.readRate = readRate

        # Configure QCar properties
        self.myQCar = QCar(frequency = self.readRate, readMode = 1)

        # Configure driving settings
        self.throttle = 0
        self.steering = 0
        self.reverse = 0

    def driving_loop(self):
        while True:
            with lock:
                keys = pressed_keys.copy()

            #Calculate controls
            self.throttle = 0.1 if 'w' in keys else 0
            self.reverse = -0.1 if 's' in keys else 0
            self.steering = 0.5 if 'a' in keys else -0.5 if 'd' in keys else 0

            if 'esc' in keys:
                self.myQCar.write(throttle=0, steering=0)
                break
            elif 'r' in keys:
                #Try to get reset to work
                pass

            self.update_controls()
        return

    def update_controls(self):
        movymoving = self.throttle + self.reverse
        self.myQCar.write(throttle=movymoving, steering=self.steering)
        return

    def start(self):
        self.driving_loop()
        return


Controller = KeyboardInterfacing()
listener.start()
try:
    Controller.start()

finally:
    listener.stop()
    qlabs_setup.terminate()