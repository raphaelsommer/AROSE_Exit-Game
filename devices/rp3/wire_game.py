import RPi.GPIO as GPIO
import time

# Set up the GPIO pins
#GPIO.setmode(GPIO.BCM)

class Wire:

    # Flags for the Wire Game
    gameState = 0

    # Constructor
    def __init__(self):
        GPIO.setup(4, GPIO.IN)
        GPIO.setup(5, GPIO.IN)
    
    def getFailed(self):
        return self.gameState == 1

    def getSuccess(self):
        return self.gameState == 2

    def changeState(self, state):
        self.gameState = state

    # Start the Wire Game from the main.py
    def startGame(self):
        while self.gameState == 0:
            if GPIO.input(4) == 1:
                time.sleep(0.1)
                if GPIO.input(4) == 1:
                    self.gameState = 1
            if GPIO.input(5) == 1:
                self.gameState = 2
            time.sleep(0.05)
