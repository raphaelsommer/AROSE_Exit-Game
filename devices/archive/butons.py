import RPi.GPIO as GPIO
import time
import random

# Pin configuration
RED_PIN = 26
GREEN_PIN = 19
BLUE_PIN = 4
BUTTON1 = 5
BUTTON2 = 6
BUTTON3 = 13

# Variables for debouncing softening
last_press_time = 0
debounce_treshold = 0.5

# Callback function to handle button presses
def button_callback(channel):
    global button_sequence, last_press_time, debounce_treshold
    current_time = time.time()
    if (current_time - last_press_time) < debounce_treshold:
        return
    last_press_time = current_time

    button_sequence.append(channel)
    print(str(channel) + ", " + str(len(button_sequence)))
    if len(button_sequence) == 1:
        blink_led('white', 1, 0.25)
    elif len(button_sequence) == 2:
        blink_led('white', 2, 0.25)
    elif len(button_sequence) == 3:
        check_sequence()
    else:
        button_sequence.clear()    

# Function to check the button sequence
def check_sequence():
    global finished, correct_sequence, wrong_sequence_counter
    if button_sequence == correct_sequence:
        blink_led('green', 2, 0.25)
        blink_led('green', 1, 1)  # Long green blink
        set_led_color('none')    # Turn off the LED
        finished = True
    else:
        blink_led('red', 3, 0.25)  # Blink red 3 times
        set_led_color('none')
        wrong_sequence_counter += 1
        if wrong_sequence_counter == 3:
            time.sleep(0.5)
            correct_sequence = random.sample(options, len(options))
            print(str(correct_sequence))
            blink_led('white', 3, 0.25)
    button_sequence.clear()

# Function to blink LED
def blink_led(color, times, interval):
    for _ in range(times):
        set_led_color(color)
        time.sleep(interval)
        set_led_color('none')
        time.sleep(interval)

# Function to set LED color
def set_led_color(color):
    colors = {
        'red': (True, False, False),
        'green': (False, True, False),
        'blue': (False, False, True),
        'white': (True, True, True),
        'none': (False, False, False)
    }
    GPIO.output(RED_PIN, colors[color][0])
    GPIO.output(GREEN_PIN, colors[color][1])
    GPIO.output(BLUE_PIN, colors[color][2])

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Add event detection to buttons
GPIO.add_event_detect(BUTTON1, GPIO.FALLING, callback=button_callback, bouncetime=1000)
GPIO.add_event_detect(BUTTON2, GPIO.FALLING, callback=button_callback, bouncetime=1000)
GPIO.add_event_detect(BUTTON3, GPIO.FALLING, callback=button_callback, bouncetime=1000)

# Initialize button press sequence list
button_sequence = []
options = [BUTTON1, BUTTON2, BUTTON3]
correct_sequence = random.sample(options, len(options))
print(str(correct_sequence))
wrong_sequence_counter = 0

set_led_color('none')
blink_led('white', 3, 0.25)
finished = False

### MAIN LOOP
try:
    while not finished:
        time.sleep(0.1)
finally:
    GPIO.cleanup()
