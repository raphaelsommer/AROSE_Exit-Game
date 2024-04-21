import RPi.GPIO as GPIO
import time
import threading

# GPIO-Pin-Nummern (angepasst an Ihr Setup)
LED_PIN_MORSE = 17
LED_PIN_DONE = 27

ROWS = [5, 6, 13, 19]  # GPIO pins for the rows
COLUMNS = [26, 16, 20, 21]  # GPIO pins for the columns

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

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_MORSE, GPIO.OUT)
GPIO.setup(LED_PIN_DONE, GPIO.OUT)
for pin in COLUMNS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
for pin in ROWS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

input_received_event = threading.Event()

### FUNCTIONS
def blink_morse(signal):
    time.sleep(1.5)
    for symbol in signal:
        GPIO.output(LED_PIN_MORSE, GPIO.HIGH)
        time.sleep(0.2 if symbol == '.' else 1)
        GPIO.output(LED_PIN_MORSE, GPIO.LOW)
        time.sleep(0.8)

def morse_blinker():
    letters_numbers = ['E', '4', 'C', '3', 'D', '7', 'O', '2']
    while not input_received_event.is_set():
        for character in letters_numbers:
            blink_morse(morse_code[character])
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
                    time.sleep(0.3)  # Debounce time
                    while GPIO.input(row_pin) == GPIO.LOW:
                        pass  # Wait for key release
                    if len(inputted_values) == len(correct_code):  # Check if we have enough digits
                        if inputted_values == correct_code:
                            print("Correct code entered!")
                            input_received_event.set()
                            return
                        else:
                            print(f"Incorrect code: {''.join(inputted_values)}. Try again.")
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