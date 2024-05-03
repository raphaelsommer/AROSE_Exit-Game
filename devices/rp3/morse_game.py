import RPi.GPIO as GPIO
import time
import threading

class Morse:
    # GPIO-Pin-Nummern
    LED_PIN_MORSE = 23
    LED_PIN_DONE = 18
    RGB_RED_PIN = 17
    RGB_GREEN_PIN = 27
    RGB_BLUE_PIN = 22

    COLUMNS = [21, 20, 16, 12] 
    ROWS = [26, 19, 13, 6] 

    # Define the keypad mapping
    KEYPAD = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
    ]

    COLORS = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'white': (255, 255, 255),
        'yellow': (255, 120, 0),
        'none': (0, 0, 0)
    }

    # Morsecode-Dictionary für das komplette Alphabet und Zahlen
    MORSE_TABLE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
        'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
        '9': '----.'
    }

    CODE_TO_MORSE = ['E', '4', 'C', '3', 'D', '7', 'O', '2']
    CORRECT_CODE = [CODE_TO_MORSE[3], CODE_TO_MORSE[7], CODE_TO_MORSE[5], CODE_TO_MORSE[1]]
    SHORT = 0.2
    LONG = 0.8
    BETWEEN = 1
    PAUSE = 2

    input_received_event = threading.Event()
    finished = False

    # Constructor
    def __init__(self):
        # Setup GPIO
        #GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_PIN_MORSE, GPIO.OUT)
        GPIO.setup(self.LED_PIN_DONE, GPIO.OUT)
        GPIO.setup(self.RGB_RED_PIN, GPIO.OUT)
        GPIO.setup(self.RGB_GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.RGB_BLUE_PIN, GPIO.OUT)
        for pin in self.COLUMNS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        for pin in self.ROWS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.blink_rgb('none', 1, 0.5)
        GPIO.output(self.LED_PIN_MORSE, GPIO.LOW)

    # Function to blink LED
    def blink_rgb(self, color, times, interval):
        for _ in range(times):
            self.set_rgb_color(color)
            time.sleep(interval)
            self.set_rgb_color('none')
            time.sleep(interval)
    
    # Function to set LED color
    def set_rgb_color(self, color):
        GPIO.output(self.RGB_RED_PIN, self.COLORS[color][0])
        GPIO.output(self.RGB_GREEN_PIN, self.COLORS[color][1])
        GPIO.output(self.RGB_BLUE_PIN, self.COLORS[color][2])

    # Function to blink LED in morse code
    def blink_led_in_morse(self, signal):
        if not self.input_received_event.is_set():
            time.sleep(self.PAUSE)
            for symbol in signal:
                if not self.input_received_event.is_set():
                    GPIO.output(self.LED_PIN_MORSE, GPIO.HIGH)
                    time.sleep(self.SHORT if symbol == '.' else self.LONG)
                    GPIO.output(self.LED_PIN_MORSE, GPIO.LOW)
                    time.sleep(self.BETWEEN)

    # Function to play morse code
    def play_morse_code(self):
        while not self.input_received_event.is_set():
            for character in self.CODE_TO_MORSE:
                self.blink_led_in_morse(self.MORSE_TABLE[character])
            if not self.input_received_event.is_set():
                GPIO.output(self.LED_PIN_DONE, GPIO.HIGH)
                time.sleep(self.LONG)
                GPIO.output(self.LED_PIN_DONE, GPIO.LOW)
                time.sleep(self.LONG)

    # Function to read the keypad input
    def read_keypad(self):
        
        inputted_values = []
        while (not self.finished) and (self.CORRECT_CODE is not inputted_values):  # Loop indefinitely until the correct code is entered
            for col_num, col_pin in enumerate(self.COLUMNS):
                GPIO.output(col_pin, GPIO.LOW)
                for row_num, row_pin in enumerate(self.ROWS):
                    if GPIO.input(row_pin) == GPIO.LOW:
                        pressed_key = self.KEYPAD[row_num][col_num]
                        print(f"Key Pressed: {pressed_key}")
                        inputted_values.append(pressed_key)
                        try:
                            self.blink_rgb('yellow', int(pressed_key), 0.2)
                        except:
                            self.blink_rgb('red', 1, 0.5)
                        time.sleep(0.3)  # Debounce time
                        while GPIO.input(row_pin) == GPIO.LOW:
                            pass  # Wait for key release
                        if len(inputted_values) == len(self.CORRECT_CODE):  # Check if we have enough digits
                            if inputted_values == self.CORRECT_CODE:
                                self.blink_rgb('green', 4, 0.5)
                                print("Correct code entered!")
                                self.input_received_event.set()
                                self.finished = True
                                return
                            else:
                                print(f"Incorrect code: {''.join(inputted_values)}. Try again.")
                                self.blink_rgb('red', 4, 0.2)
                                inputted_values = []  # Reset the inputted values for a new attempt
                GPIO.output(col_pin, GPIO.HIGH)
                time.sleep(0.1)  # Column switching delay

    # Function to get the finished status in the main.py
    def getFinished(self):
        return self.finished

    # Function to start the game from the main.py
    def startGame(self):
        morse_thread = threading.Thread(target=self.play_morse_code)
        input_thread = threading.Thread(target=self.read_keypad)

        morse_thread.start()
        input_thread.start()

        morse_thread.join()  # Wait for the Morse thread to finish if the correct code is entered
        input_thread.join()  # Ensure the input thread also finishes
    
    # Function to stop the game and cleanup GPIO 
    def stopGame(self):
        self.input_received_event.set()
        self.finished = True
        time.sleep(2)
        #GPIO.cleanup()
