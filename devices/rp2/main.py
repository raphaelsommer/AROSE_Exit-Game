import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import threading
import RPi.GPIO as GPIO
import logging
import os

from midi_ip_game import MidiIpGame
from general_timer import Timer
from button_sequence_game import ButtonSequenceGame

# MQTT Konfigurationen
MQTT_BROKER = "192.168.0.102"  # Beispiel-Broker, ersetze diesen durch deinen Broker
MQTT_PORT = 1883
MQTT_TRANSPORT_PROTOCOL = "tcp"
CLIENT_ID = "rp2"

### Needed MQTT Topics
MQTT_TOPIC_RP2 = "/rp2"  # will
# Topics for General and Timer
MQTT_TOPIC_GEN_GLOBAL = "/gen/global" # sub/pub
# Topics for the MIDI-IP-Game
MQTT_TOPIC_A5_PIANO = "/a5/piano" # sub
MQTT_TOPIC_C1_RFID = "/c1/rfid" # pub
# Topics for the Button-Sequence-Game
MQTT_TOPIC_B2_GRAVITY = "/b2/gravity" # sub
MQTT_TOPIC_A3_BUTTON = "/a3/buttons" # pub


# Flags for the MIDI-IP-Game, Timer and Button
isStartMidiIpGame = False
isStartTimer = False
isStartButtonSequence = False

isStoppedMidiIpGame = False
isStoppedTimer = False
isStoppedButtonSequence = False

# Initialize the games
MIDIIpGame = MidiIpGame()
MainTimer = Timer()
ButtonGame = ButtonSequenceGame()

# Set up the logger
log_directory = "/home/rsommer/dhbw-wwi23h-systemanalyse-team1/devices/rp2"
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(log_directory, "rp2.log")
Logger = logging.getLogger("RP2")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set up GPIO mode once
GPIO.setmode(GPIO.BCM)

# "Prepare" (instantiate) threads for the games
thread1 = threading.Thread(target=None)
thread2 = threading.Thread(target=None)
thread3 = threading.Thread(target=None)


### MQTT Methods
def on_message(client, userdata, msg):
    global isStartMidiIpGame, isStartTimer, isStartButtonSequence, stop
    # print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'start':
        print("Timer start")
        isStartTimer = True
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'stop':
        print("Stop Game")
        stop = true
    if msg.topic == MQTT_TOPIC_A5_PIANO and msg.payload.decode() == 'start':
        print("Starting MIDI-IP-Game")
        isStartMidiIpGame = True
    if msg.topic == MQTT_TOPIC_B2_GRAVITY and msg.payload.decode() == 'off':
        print("Button-Sequence started")
        isStartButtonSequence = True
    Logger.info("Received topic: " + msg.topic.decode("utf-8") + ", message: " + msg.payload.decode("utf-8"))

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected: " + str(reason_code))
    Logger.info("Connected client " + CLIENT_ID + " with reason code: " + str(reason_code))
    client.publish(topic=MQTT_TOPIC_RP2, payload="connected", qos=2, retain=True)

def on_connect_fail(client, userdata, properties, reason_code):
    print("Connection failed: " + str(reason_code))
    Logger.ERROR("Connection failed with reason code: " + str(reason_code))

def on_disconnect(client, userdata, flags, reason_code, properties):
    print("Disconnected: " + str(reason_code))
    Logger.info("Disconnected client " + CLIENT_ID + " with reason code: " + str(reason_code))

def on_log(client, userdata, level, buf):
    if level == 1 or level == 2:
        Logger.info(buf)
    elif level == 4:
        Logger.warning(buf)
    elif level == 8:
        Logger.error(buf)
    else:
        Logger.debug(buf)


##### Client Setup
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="rp2", password="rp2Arose1234!")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_connect_fail = on_connect_fail
client.on_log = on_log
properties = Properties(PacketTypes.CONNECT)
client.enable_logger()
client.will_set(MQTT_TOPIC_RP2, payload=f"{MainTimer.getRestTimeInSeconds}", qos=2, retain=True)
client.connect(MQTT_BROKER, MQTT_PORT, properties=properties, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
client.subscribe([(MQTT_TOPIC_GEN_GLOBAL, 0), (MQTT_TOPIC_A5_PIANO, 2), (MQTT_TOPIC_B2_GRAVITY, 2)])



stop = False
threads_started = {thread1: False, thread2: False, thread3: False}

try:
    while not stop:
        if not thread1.is_alive() and not threads_started[thread1] and isStartTimer:
            #isStartTimer = False
            thread1 = threading.Thread(target=MainTimer.startTimer)
            thread1.start()
            threads_started[thread1] = True
        if not thread3.is_alive() and not threads_started[thread3] and isStartMidiIpGame:
            #isStartMidiIpGame = False
            thread3 = threading.Thread(target=MIDIIpGame.startGame)
            thread3.start()
            threads_started[thread3] = True
        if not thread2.is_alive() and not threads_started[thread2] and isStartButtonSequence:
            #isStartButtonSequence = False
            thread2 = threading.Thread(target=ButtonGame.startGame)
            thread2.start()
            threads_started[thread2] = True

        
        if MIDIIpGame.getFinished() and not isStoppedMidiIpGame:
            print("Stopping MIDI-IP-Game")
            MIDIIpGame.stopGame()
            isStoppedMidiIpGame = True
            client.publish(topic=MQTT_TOPIC_C1_RFID, payload="start", qos=2)
        if ButtonGame.getFinished() and not isStoppedButtonSequence:
            print("Stopping Button-Sequence-Game")
            ButtonGame.stopGame()
            isStoppedButtonSequence = True
            client.publish(topic=MQTT_TOPIC_A3_BUTTON, payload="finished", qos=2)
        if MainTimer.getFinished() and not isStoppedTimer:
            print("Time ran out - Game over!")
            isStoppedTimer = True
            '''Timer does not need to be stopped, as it is a one-time countdown.'''
            if not isStoppedMidiIpGame:
                MIDIIpGame.showGameOver()
            client.publish(topic=MQTT_TOPIC_GEN_GLOBAL, payload="timeOver", qos=2)
            stop = True


        for thread in [thread1, thread2, thread3]:
            if threads_started[thread] and not thread.is_alive():
                thread.join()
                threads_started[thread] = False


except KeyboardInterrupt:
    if isStartTimer:
        MainTimer.stopTimer()
    if isStartMidiIpGame:
        MIDIIpGame.stopGame()
    if isStartButtonSequence:
        ButtonGame.stopGame()
finally:
    if not isStoppedTimer:
        MainTimer.stopTimer()
    if not isStoppedMidiIpGame:
        MIDIIpGame.stopGame()
    if not isStoppedButtonSequence:
        ButtonGame.stopGame()
    GPIO.cleanup()
    client.disconnect()
    client.loop_stop()
    #if os.path.exists(log_file):
    #    with open(log_file, 'r') as file:
    #        log_contents = file.read()
    #    print(log_contents)
    #else:
    #    print("Log file not found!")
    Logger.shutdown()
