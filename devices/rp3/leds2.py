import RPi.GPIO as GPIO
import time

# GPIO-Pins definieren
DATA_PIN = 17   # Anschluss an SER (Pin 14) des 74HC595
LATCH_PIN = 27  # Anschluss an RCLK (Pin 12) des 74HC595
CLOCK_PIN = 22  # Anschluss an SRCLK (Pin 11) des 74HC595

# GPIO-Pins einrichten
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)

def shift_out(value):
    GPIO.output(LATCH_PIN, 0)
    time.sleep(0.001)  # Kleine Pause, um das Latch zu stabilisieren
    for i in range(8):
        GPIO.output(CLOCK_PIN, 0)
        GPIO.output(DATA_PIN, (value >> (7 - i)) & 1)
        time.sleep(0.001)  # Verzögerung zur Reduzierung des Signalprellens
        GPIO.output(CLOCK_PIN, 1)
        time.sleep(0.001)
    GPIO.output(LATCH_PIN, 1)
    time.sleep(0.001)

def control_leds(w1, w2, w3, red, green, blue):
    byte = (red << 7) | (green << 6) | (blue << 5) | (w1 << 3) | (w2 << 2) | (w3 << 1)
    shift_out(byte)

try:
    while True:
        control_leds(1, 0, 0, 0, 0, 0)
        time.sleep(1)
        control_leds(0, 1, 0, 0, 0, 0)
        time.sleep(1)
        control_leds(0, 0, 1, 0, 0, 0)
        time.sleep(1)
except KeyboardInterrupt:
    control_leds(0, 0, 0, 0, 0, 0)
    GPIO.cleanup()
