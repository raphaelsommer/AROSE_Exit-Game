import RPi.GPIO as GPIO
import time

class Wire:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # Set the GPIO mode
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 4 as input with a pull-down resistor
        GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 5 as input with a pull-down resistor
        self.gameState = 0

    def get_game_state(self):
        return self.gameState

    def change_state(self, state):
        self.gameState = state

    def start_game(self):
        print("Game started! Monitoring voltage...")
        while self.gameState == 0:
            if GPIO.input(5):
                self.gameState = 1
                print("Voltage detected on pin 5 - State changed to 1")
            if GPIO.input(4):
                self.gameState = 2
                print("Voltage detected on pin 4 - State changed to 2")
            time.sleep(0.05)  # Loop delay to reduce CPU usage

# Usage
if __name__ == "__main__":
    wire_game = Wire()
    wire_game.start_game()
