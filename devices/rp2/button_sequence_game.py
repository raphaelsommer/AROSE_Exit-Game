import RPi.GPIO as GPIO
import time
import random

##### Define a class for the Button Sequence Game which is going to be instantiated in the main.py file
class ButtonSequenceGame:

    # Pin configuration
    RED_PIN = 26
    GREEN_PIN = 19
    BLUE_PIN = 13
    BUTTON1 = 4
    BUTTON2 = 5
    BUTTON3 = 6

    # Variables for debouncing softening
    last_press_time = 0
    debounce_treshold = 0.8

    # Initialize the variables
    button_sequence = []
    finished = False
    correct_sequence = random.sample([BUTTON1, BUTTON2, BUTTON3], 3)
    wrong_sequence_counter = 0

    ### Define the constructor of the class
    def __init__(self):
        # Set up the GPIO
        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.BLUE_PIN, GPIO.OUT)
        GPIO.setup(self.BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    ### Callback function to handle button presses
    def button_callback(self, channel):
        if time.time() - self.last_press_time > self.debounce_treshold:
            self.last_press_time = time.time()
            self.button_sequence.append(channel)
            print(str(channel) + ", " + str(len(self.button_sequence)))
            # Check the length of the button sequence
            if len(self.button_sequence) == 1:
                self.blink_led('white', 1, 0.25)
            elif len(self.button_sequence) == 2:
                self.blink_led('white', 2, 0.25)
            elif len(self.button_sequence) == 3:
                self.check_sequence()
            else:
                self.button_sequence.clear()    

    ### Define a method to check the button sequence
    def check_sequence(self):
        if self.button_sequence == self.correct_sequence:
            self.blink_led('green', 2, 0.25)
            self.blink_led('green', 1, 1)  # Long green blink
            self.set_led_color('none')    # Turn off the LED
            self.finished = True
        else:
            correct_onces = 0
            for i in range(3):
                if self.button_sequence[i] == self.correct_sequence[i]:
                    correct_onces += 1
            for i in range(3):
                if correct_onces > 0:
                    self.blink_led('green', 1, 0.25)
                    correct_onces -= 1
                else:
                    self.blink_led('red', 1, 0.25)
            self.set_led_color('none')
            self.wrong_sequence_counter += 1
            if self.wrong_sequence_counter >= 3:
                time.sleep(0.5)
                self.correct_sequence = random.sample([self.BUTTON1, self.BUTTON2, self.BUTTON3], 3)
                print(str(self.correct_sequence))
                self.blink_led('white', 3, 1)
            self.button_sequence.clear()
    
    ### Function to blink LED
    def blink_led(self, color, times, interval):
        for _ in range(times):
            self.set_led_color(color)
            time.sleep(interval)
            self.set_led_color('none')
            time.sleep(interval)

    ### Function to set LED color
    def set_led_color(self, color):
        colors = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'white': (255, 255, 255),
            'none': (0, 0, 0)
        }
        GPIO.output(self.RED_PIN, colors[color][0])
        GPIO.output(self.GREEN_PIN, colors[color][1])
        GPIO.output(self.BLUE_PIN, colors[color][2])

    ### Define a method to get the finish state of the game
    def getFinished(self):
        return self.finished

    ### Define a method to start the Button Sequence Game from the main.py file
    def startGame(self):

        # Set the LED color to none
        self.set_led_color('none')
        # Blink the LED white 3 times
        self.blink_led('white', 3, 0.5)

        # Add the button callback function to the GPIO event detection
        GPIO.add_event_detect(self.BUTTON1, GPIO.FALLING, callback=self.button_callback, bouncetime=int(self.debounce_treshold*1000))
        GPIO.add_event_detect(self.BUTTON2, GPIO.FALLING, callback=self.button_callback, bouncetime=int(self.debounce_treshold*1000))
        GPIO.add_event_detect(self.BUTTON3, GPIO.FALLING, callback=self.button_callback, bouncetime=int(self.debounce_treshold*1000))

        # Wait until the game is finished
        while not self.finished:
            time.sleep(0.1)
        #self.stopGame()
    
    ### Define a method to stop/interrupt the Button Sequence Game from the main.py file
    def stopGame(self):
        # Set the LED color to none
        self.set_led_color('none')
        # Reset the variables
        self.button_sequence.clear()
        self.wrong_sequence_counter = 0
        # Clean up the GPIO
        #GPIO.cleanup()
        # Remove the event detection
        GPIO.remove_event_detect(self.BUTTON1)
        GPIO.remove_event_detect(self.BUTTON2)
        GPIO.remove_event_detect(self.BUTTON3)
