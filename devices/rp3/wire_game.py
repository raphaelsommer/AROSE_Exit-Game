import RPi.GPIO as GPIO
import time

# Set up the GPIO pins
#GPIO.setmode(GPIO.BCM)

class Wire:

    # Flags for the Wire Game
    gameState = 0

    # Constructor
    def __init__(self):
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def getGameState(self):
        return self.gameState

    def changeState(self, state):
        self.gameState = state

    # Start the Wire Game from the main.py
    def startGame(self):
        while self.gameState == 0:

            # GPIO5 ist mit dem Draht verbunden. Wenn hierüber ein Strom länger als 0,2 Sekunden fließt hat der Spieler verloren und das Spiel wird beendet.
            # GPIO4 ist mit dem Nagel verbunden. Wenn der Spieler den Nagel erreicht ohne den Draht zu lange zu berühren, fließt ein Strom und das Spiel wird erfolgreich beendet.
            if GPIO.input(5):
                time.sleep(0.2)
                if GPIO.input(5):
                    self.gameState = 1
                    print(self.gameState)
            if GPIO.input(4):
                self.gameState = 2
                print(self.gameState)
            time.sleep(0.05)

    def stopGame(self):
        self.changeState(3)
