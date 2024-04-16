import RPi.GPIO as GPIO
from gpiozero import Buzzer
import spidev
import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import ssl

# MQTT Konfigurationen
MQTT_BROKER = "192.168.0.102"  # Beispiel-Broker, ersetze diesen durch deinen Broker
MQTT_PORT = 1883
MQTT_TRANSPORT_PROTOCOL = "tcp"

MQTT_TOPIC_GEN_START = "/gen/start"
MQTT_TOPIC_GEN_STOP = "/gen/stop"
MQTT_TOPIC_GEN_TIME = "/gen/time"
MQTT_TOPIC_CO2_MASKS = "/B-3b/CO2-masks"


# Define segment codes for 0-9 on a 7-segment display
SEGMENT_MAP = {
    '0': 0b01111110,
    '1': 0b00110000,
    '2': 0b01101101,
    '3': 0b01111001,
    '4': 0b00110011,
    '5': 0b01011011,
    '6': 0b01011111,
    '7': 0b01110000,
    '8': 0b01111111,
    '9': 0b01111011,
}

# Buzzer Configuration
buzzer = Buzzer(21)

# SPI Configuration
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 5000

# Display configuration
DISPLAY_BRIGHTNESS = 8
NUM_DIGITS = 4

# Timer variables
start = False
stopped = False
INITTIME = 18
timerMin10 = (INITTIME - (INITTIME % 10)) // 10
timerMin1 = INITTIME % 10
timerSec10 = 0
timerSec1 = 0


# Display and Logic Functions
def write_byte(register, data):
    spi.xfer2([register, data])

def setup_display():
    # Initialize display
    write_byte(0x0c, 0x01)  # Shutdown register
    write_byte(0x0a, DISPLAY_BRIGHTNESS)  # Intensity register
    write_byte(0x0b, 0x07)  # Scan limit register (show all digits)
    clear_display()

def clear_display():
    for digit in range(1, 9):
        write_byte(digit, 0x00)

def display_digit(position, value, colon=False):
    if 0 <= value <= 9:
        data = SEGMENT_MAP[str(value)]
        if colon:
            data |= 0x80  # Turn on decimal point/colon
        write_byte(position, data)

def set_digits():
    global timerMin10, timerMin1, timerSec10, timerSec1
    display_digit(1, timerMin10, False)
    display_digit(2, timerMin1, (int(timerSec1) % 2) == 0)  # Assume colon should blink here
    display_digit(3, timerSec10, False)
    display_digit(4, timerSec1, False)

def countdown():
    global timerMin10, timerMin1, timerSec10, timerSec1
    if timerSec1 == 0:
        if timerSec10 == 0:
            if timerMin1 == 0:
                if timerMin10 == 0:
                    timerMin10 = 6
                timerMin1 = 10
                timerMin10 -= 1
            timerSec10 = 6
            timerMin1 -= 1
        timerSec1 = 10
        timerSec10 -= 1
    timerSec1 -= 1

def alarm():
    count5sec = 0
    start_time = time.time()
    while count5sec < 5:
        current_time = time.time()
        elapsed = current_time - start_time
        if elapsed >= 0.5:
            buzzer.on()
            display_digit(1, 0, True)
            display_digit(2, 0, True)
            display_digit(3, 0, True)
            display_digit(4, 0, True)
            time.sleep(0.5)
            buzzer.off()
            clear_display()
            time.sleep(0.5)
            count5sec += 1
            start_time = current_time 

def extend_timer(min):
    global timerMin1, timerMin10
    # Implement timer extension logic
    timerMin1 += min
    if timerMin1 > 9:
        timerMin10 += (timerMin1 - (timerMin1 % 10)) // 10
        timerMin1 = timerMin1 % 10


# MQTT Methods
def on_message(client, userdata, msg):
    global start, stopped
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_START and msg.payload.decode() == '1':
        print("Timer start")
        start = True
    if msg.topic == MQTT_TOPIC_CO2_MASKS and msg.payload.decode() == '1':
        print("CO2 mask detected, extending timer")
        extend_timer(8)
    if msg.topic == MQTT_TOPIC_GEN_STOP and msg.payload.decode() == '1':
        print("Timer stopped")
        stopped = True


# Timer Method
def startTimer():
    global stopped, finished
    setup_display()
    start_time = time.time()
    timer_over = False
    while (not timer_over):
        current_time = time.time()
        set_digits()
        elapsed = current_time - start_time
        if elapsed >= 0.01:  # Update alle Sekunde
            countdown()
            start_time = current_time
        if stopped:
            alarm()
            client.publish(MQTT_TOPIC_GEN_TIME, "0")  # Veröffentliche "0" bei Ablauf
            timer_over = True
            finished = True
        if timerMin10 == 0 and timerMin1 == 0 and timerSec10 == 0 and timerSec1 == 0:
            alarm()
            client.publish(MQTT_TOPIC_GEN_TIME, "0")  # Veröffentliche "0" bei Ablauf
            timer_over = True
            finished = True


# Client Setup
client = mqtt.Client(client_id="rp3", protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="rp3_sub", password="rp3arose1234!")
###client.on_connect = on_connect
client.on_message = on_message

properties = Properties(PacketTypes.CONNECT)
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
client.publish("/test", "Test 2")
client.subscribe([(MQTT_TOPIC_GEN_START, 0), (MQTT_TOPIC_CO2_MASKS, 0), (MQTT_TOPIC_GEN_STOP, 0)])


# MAIN LOOP
finished = False
while not finished:
    print("...waiting...")
    if start:
        startTimer()
    time.sleep(1)

""" if __name__ == '__main__':
    startTimer()
 """

client.disconnect()
client.loop_stop()