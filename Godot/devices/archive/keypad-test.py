import RPi.GPIO as GPIO
import time

# Define the GPIO pins for the rows and columns according to the provided setup
ROWS = [5, 6, 13, 19]  # GPIO pins from top to bottom as per your description
COLUMNS = [26, 16, 20, 21]  # GPIO pins from top to bottom as per your description

# Define the keypad mapping
KEYPAD = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Set up the column pins as outputs
for pin in COLUMNS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# Set up the row pins as inputs with pull-up resistors
for pin in ROWS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_keypad():
    try:
        while True:
            for col_num, col_pin in enumerate(COLUMNS):
                # Set the current column to LOW
                GPIO.output(col_pin, GPIO.LOW)
                
                # Check each row to see if a key is pressed
                for row_num, row_pin in enumerate(ROWS):
                    if GPIO.input(row_pin) == GPIO.LOW:
                        print(f"Key Pressed: {KEYPAD[row_num][col_num]}")
                        time.sleep(0.2)  # Debounce time
                        
                        # Wait for the key to be released
                        while GPIO.input(row_pin) == GPIO.LOW:
                            pass
                        time.sleep(0.3)  # Additional debounce time to avoid multiple detections

                # Set the current column back to HIGH
                GPIO.output(col_pin, GPIO.HIGH)
                
                # A short delay to prevent bouncing
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        GPIO.cleanup()  # Clean up GPIO on normal exit

if __name__ == "__main__":
    print("Starting keypad test...")
    read_keypad()
