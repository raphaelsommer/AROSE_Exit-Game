import RPi.GPIO as GPIO
import time
import threading

# GPIO-Pin-Nummern (angepasst an Ihr Setup)
LED_PIN_MORSE = 23
LED_PIN_DONE = 18
RGB_RED_PIN = 17
RGB_GREEN_PIN = 27
RGB_BLUE_PIN = 22

COLUMNS = [21, 20, 16, 12]  # GPIO pins for the rows
ROWS = [26, 19, 13, 6]  # GPIO pins for the columns

# Define the keypad mapping
KEYPAD = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Morsecode-Dictionary für das komplette Alphabet und Zahlen
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.'
}

SHORT = 0.2
LONG = 0.7
BETWEEN = 0.7
PAUSE = 1.5

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_MORSE, GPIO.OUT)
GPIO.setup(LED_PIN_DONE, GPIO.OUT)
GPIO.setup(RGB_RED_PIN, GPIO.OUT)
GPIO.setup(RGB_GREEN_PIN, GPIO.OUT)
GPIO.setup(RGB_BLUE_PIN, GPIO.OUT)
for pin in COLUMNS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
for pin in ROWS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

input_received_event = threading.Event()

### FUNCTIONS
# Function to blink LED
def blink_rgb(color, times, interval):
    for _ in range(times):
        set_rgb_color(color)
        time.sleep(interval)
        set_rgb_color('none')
        time.sleep(interval)

# Function to set LED color
def set_rgb_color(color):
    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'white': (255, 255, 255),
        'yellow': (255, 120, 0),
        'none': (0, 0, 0)
    }
    GPIO.output(RGB_RED_PIN, colors[color][0])
    GPIO.output(RGB_GREEN_PIN, colors[color][1])
    GPIO.output(RGB_BLUE_PIN, colors[color][2])

def blink_morse(signal):
    if not input_received_event.is_set():
        time.sleep(PAUSE)
        for symbol in signal:
            if not input_received_event.is_set():
                GPIO.output(LED_PIN_MORSE, GPIO.HIGH)
                time.sleep(SHORT if symbol == '.' else LONG)
                GPIO.output(LED_PIN_MORSE, GPIO.LOW)
                time.sleep(BETWEEN)

def morse_blinker():
    letters_numbers = ['E', '4', 'C', '3', 'D', '7', 'O', '2']
    while not input_received_event.is_set():
        for character in letters_numbers:
            blink_morse(morse_code[character])
        if not input_received_event.is_set():
            GPIO.output(LED_PIN_DONE, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(LED_PIN_DONE, GPIO.LOW)
            time.sleep(1)

def read_keypad(correct_code):
    inputted_values = []
    while True:  # Loop indefinitely until the correct code is entered
        for col_num, col_pin in enumerate(COLUMNS):
            GPIO.output(col_pin, GPIO.LOW)
            for row_num, row_pin in enumerate(ROWS):
                if GPIO.input(row_pin) == GPIO.LOW:
                    pressed_key = KEYPAD[row_num][col_num]
                    print(f"Key Pressed: {pressed_key}")
                    inputted_values.append(pressed_key)
                    try:
                        blink_rgb('yellow', int(pressed_key), 0.2)
                    except:
                        blink_rgb('red', 1, 0.5)
                    time.sleep(0.3)  # Debounce time
                    while GPIO.input(row_pin) == GPIO.LOW:
                        pass  # Wait for key release
                    if len(inputted_values) == len(correct_code):  # Check if we have enough digits
                        if inputted_values == correct_code:
                            print("Correct code entered!")
                            input_received_event.set()
                            blink_rgb('green', 4, 0.5)
                            return
                        else:
                            print(f"Incorrect code: {''.join(inputted_values)}. Try again.")
                            blink_rgb('red', 4, 0.2)
                            inputted_values = []  # Reset the inputted values for a new attempt
            GPIO.output(col_pin, GPIO.HIGH)
            time.sleep(0.1)  # Column switching delay

def main():
    correct_code = ['3', '2', '7', '4']  # The correct code as a list of strings
    morse_thread = threading.Thread(target=morse_blinker)
    input_thread = threading.Thread(target=read_keypad, args=(correct_code,))  # Pass the correct code to the thread

    morse_thread.start()
    input_thread.start()

    morse_thread.join()  # Wait for the Morse thread to finish if the correct code is entered
    input_thread.join()  # Ensure the input thread also finishes

##### MAIN #####
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("INTERRUPT")
    finally:
        GPIO.cleanup()