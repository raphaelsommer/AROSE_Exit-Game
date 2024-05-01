import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import threading
import RPi.GPIO as GPIO

from midi_ip_game import MidiIpGame
from general_timer import Timer
from button_sequence_game import ButtonSequenceGame

# MQTT Konfigurationen
MQTT_BROKER = "localhost"  # Beispiel-Broker, ersetze diesen durch deinen Broker
MQTT_PORT = 1883
MQTT_TRANSPORT_PROTOCOL = "tcp"

### Needed MQTT Topics
# Topics for General and Timer
MQTT_TOPIC_GEN_GLOBAL = "/gen/global" # sub/pub
# Topics for the MIDI-IP-Game
MQTT_TOPIC_A5_PIANO = "/a5/piano" # sub
MQTT_TOPIC_C1_RFID = "/c1/rfid" # pub
# Topics for the Button-Sequence-Game
MQTT_TOPIC_B2_GRAVITY = "/b2/gravity" # sub/pub
# Topics for opening doors
MQTT_TOPIC_DOOR_B5 = "/doors/b5" # pub
MQTT_TOPIC_DOOR_A5 = "/doors/a5" # pub
MQTT_TOPIC_DOOR_B3 = "/doors/b3" # pub
MQTT_TOPIC_DOOR_A3 = "/doors/a3" # pub
MQTT_TOPIC_DOOR_B2 = "/doors/b2" # pub


# Flags for the MIDI-IP-Game, Timer and Button
isStartMidiIpGame = False
isStartTimer = False
isStartButtonSequence = False
isStoppedMidiIpGame = False
isStoppedTimer = False
isStoppedButtonSequence = False


### MQTT Methods
def on_message(client, userdata, msg):
    global isStartMidiIpGame, isStartTimer, isStartButtonSequence
    # print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'start':
        print("Timer start")
        isStartTimer = True
    if msg.topic == MQTT_TOPIC_A5_PIANO and msg.payload.decode() == 'start':
        print("Starting MIDI-IP-Game")
        isStartMidiIpGame = True
    if msg.topic == MQTT_TOPIC_B2_GRAVITY and msg.payload.decode() == 'off':
        print("Button-Sequence started")
        isStartButtonSequence = True

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected: " + str(reason_code))

##### Client Setup
client = mqtt.Client(client_id="rp2", protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="rp2", password="rp2Arose1234!")
client.on_connect = on_connect
client.on_message = on_message
properties = Properties(PacketTypes.CONNECT)
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
client.subscribe([(MQTT_TOPIC_GEN_GLOBAL, 0), (MQTT_TOPIC_A5_PIANO, 2), (MQTT_TOPIC_B2_GRAVITY, 2)])

# Set up GPIO mode once
GPIO.setmode(GPIO.BCM)

# Initialize the games
MIDIIpGame = MidiIpGame()
MainTimer = Timer()
ButtonGame = ButtonSequenceGame()

# "Prepare" (instantiate) threads for the games
thread1 = threading.Thread(target=None)
thread2 = threading.Thread(target=None)
thread3 = threading.Thread(target=None)

stop = False
threads_started = {thread1: False, thread2: False, thread3: False}
try:
    while not stop:
        if not thread1.is_alive() and not threads_started[thread1] and isStartTimer:
            isStartTimer = False
            thread1 = threading.Thread(target=MainTimer.startTimer)
            thread1.start()
            threads_started[thread1] = True
        if not thread3.is_alive() and not threads_started[thread3] and isStartMidiIpGame:
            isStartMidiIpGame = False
            thread3 = threading.Thread(target=MIDIIpGame.startGame)
            thread3.start()
            threads_started[thread3] = True
        if not thread2.is_alive() and not threads_started[thread2] and isStartButtonSequence:
            isStartButtonSequence = False
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
            client.publish(topic=MQTT_TOPIC_B2_GRAVITY, payload="on", qos=2)
            client.publish(topic=MQTT_TOPIC_DOOR_B5, payload="1", qos=2)
            client.publish(topic=MQTT_TOPIC_DOOR_A5, payload="1", qos=2)
            client.publish(topic=MQTT_TOPIC_DOOR_B3, payload="1", qos=2)
            client.publish(topic=MQTT_TOPIC_DOOR_A3, payload="1", qos=2)
            client.publish(topic=MQTT_TOPIC_DOOR_B2, payload="1", qos=2)
        if MainTimer.getFinished() and not isStoppedTimer:
            print("Stopping Timer")
            isStoppedTimer = True
            client.publish(topic=MQTT_TOPIC_GEN_GLOBAL, payload="stop", qos=2)
            stop = True


        for thread in [thread1, thread2, thread3]:
            if threads_started[thread] and not thread.is_alive():
                thread.join()
                threads_started[thread] = False


except KeyboardInterrupt:
    MainTimer.stopTimer()
    MIDIIpGame.stopGame()
    ButtonGame.stopGame()
finally:
    GPIO.cleanup()
    client.disconnect()
    client.loop_stop()
