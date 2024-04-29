import RPi.GPIO as GPIO
import time

# Set up the GPIO pins
#GPIO.setmode(GPIO.BCM)

class Wire:

    # Flags for the Wire Game
    failed = False
    success = False

    # Constructor
    def __init__(self):
        GPIO.setup(3, GPIO.IN)
        GPIO.setup(4, GPIO.IN)
    
    def getFailed(self):
        return self.failed

    def getSuccess(self):
        return self.success

    # Start the Wire Game from the main.py
    def startGame(self):
        """ while not self.failed or not self.success:
            if GPIO.input(3) == 1:
                self.failed = True
            elif GPIO.input(4) == 1:
                self.success = True
        self.stopGame() """
        time.sleep(1)
        pass

    # Stop the Wire Game from the main.py
    def stopGame(self):
        pass