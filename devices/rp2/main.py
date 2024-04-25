import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import threading
from midi_ip_game import MidiIpGame
from general_timer import Timer

# MQTT Konfigurationen
MQTT_BROKER = "192.168.0.102"  # Beispiel-Broker, ersetze diesen durch deinen Broker
MQTT_PORT = 1883
MQTT_TRANSPORT_PROTOCOL = "tcp"

# Topics for General and Timer
MQTT_TOPIC_GEN_START = "/gen/start"
MQTT_TOPIC_GEN_STOP = "/gen/stop"
# Topics for the MIDI-IP-Game
MQTT_TOPIC_DOOR_A5 = "/door/a5"
# Topics for the RFID-Reader
MQTT_TOPIC_C1_RFID = "/c1/rfid"
# Topics for the Button-Sequence
MQTT_TOPIC_A3_BUTTON = "/a3/button"

# Flags for the MIDI-IP-Game and Timer
isStartMIDIIPGame = False
isStartTimer = False
isStartButtonSequence = False


### MQTT Methods
def on_message(client, userdata, msg):
    global isStartMIDIIPGame, isStartTimer, isStartButtonSequence
    # print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_START and msg.payload.decode() == '1':
        print("Timer start")
        isStartTimer = True
    if msg.topic == MQTT_TOPIC_DOOR_A5 and msg.payload.decode() == '1':
        print("Door from A-4 to A-5 opened, starting MIDI-IP-Game")
        isStartMIDIIPGame = True
    if msg.topic == MQTT_TOPIC_A3_BUTTON and msg.payload.decode() == '1':
        print("Button-Sequence started")
        isStartButtonSequence = True


##### Client Setup
client = mqtt.Client(client_id="rp3", protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="rp3_sub", password="rp3arose1234!")
'''client.on_connect = on_connect'''
client.on_message = on_message
properties = Properties(PacketTypes.CONNECT)
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
client.subscribe([(MQTT_TOPIC_GEN_START, 2), (MQTT_TOPIC_GEN_STOP, 2), (MQTT_TOPIC_DOOR_A5, 2), (MQTT_TOPIC_C1_RFID, 2), (MQTT_TOPIC_A3_BUTTON, 2)])

MIDIIpGame = MidiIpGame()
MainTimer = Timer()

thread1 = threading.Thread(target=MainTimer.startTimer)
thread2 = threading.Thread(target=MIDIIpGame.startGame)

stop = False
while not stop:
    if isStartTimer:
        print("Starting Timer")
        thread1.start()
    if isStartMIDIIPGame:
        print("Starting MIDI-IP-Game")
        thread2.start()
        isStartMIDIIPGame = False
    if MIDIIpGame.getFinished():
        print("Stopping MIDI-IP-Game")
        MIDIIpGame.stopGame()
        client.publish(topic=MQTT_TOPIC_C1_RFID, payload="1", qos=2)
    if MainTimer.getFinished():
        print("Stopping Timer")
        client.publish(topic=MQTT_TOPIC_GEN_STOP, payload="1", qos=2)

    if thread2.is_alive():
        thread1.join()
        thread2.join()

client.disconnect()
client.loop_stop()