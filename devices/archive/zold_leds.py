import RPi.GPIO as GPIO
import time

# Define the GPIO pins
DATA_PIN = 17
LATCH_PIN = 27
CLOCK_PIN = 22

# Setup the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)

def shift_out(byte):
    GPIO.output(LATCH_PIN, 0)  # Prepare the latch for data
    for i in range(8):
        GPIO.output(CLOCK_PIN, 0)  # Clock pin low
        GPIO.output(DATA_PIN, (byte >> i) & 1)  # Set the data pin
        GPIO.output(CLOCK_PIN, 1)  # Clock pin high to write data
    GPIO.output(LATCH_PIN, 1)  # Latch the data into the outputs

# Function to control individual LEDs
def control_leds(w1, w2, w3, red, green, blue):
    byte = (w1 << 1) | (w2 << 2) | (w3 << 3) | (red << 4) | (green << 5) | (blue << 6)
    shift_out(byte)

# Main loop
try:
    while True:
        # Sequence through each LED
        control_leds(1, 0, 0, 0, 0, 0)  # First white LED
        time.sleep(1)
        control_leds(0, 1, 0, 0, 0, 0)  # Second white LED
        time.sleep(1)
        control_leds(0, 0, 1, 0, 0, 0)  # Third white LED
        time.sleep(1)
        control_leds(0, 0, 0, 1, 0, 0)  # RGB Red
        time.sleep(1)
        control_leds(0, 0, 0, 0, 1, 0)  # RGB Green
        time.sleep(1)
        control_leds(0, 0, 0, 0, 0, 1)  # RGB Blue
        time.sleep(1)
        control_leds(0, 0, 0, 0, 0, 0)  # All off
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
