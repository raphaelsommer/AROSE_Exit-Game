import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import threading
from midi_ip_game import MidiIpGame
from general_timer import Timer
from button_sequence_game import ButtonSequenceGame

# MQTT Konfigurationen
MQTT_BROKER = "192.168.0.102"  # Beispiel-Broker, ersetze diesen durch deinen Broker
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
isStartMIDIIPGame = False
isStartTimer = False
isStartButtonSequence = False


### MQTT Methods
def on_message(client, userdata, msg):
    global isStartMIDIIPGame, isStartTimer, isStartButtonSequence
    # print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'start':
        print("Timer start")
        isStartTimer = True
    if msg.topic == MQTT_TOPIC_A5_PIANO and msg.payload.decode() == 'start':
        print("Starting MIDI-IP-Game")
        isStartMIDIIPGame = True
    if msg.topic == MQTT_TOPIC_B2_GRAVITY and msg.payload.decode() == 'off':
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
client.subscribe([(MQTT_TOPIC_GEN_GLOBAL, 2), (MQTT_TOPIC_A5_PIANO, 2), (MQTT_TOPIC_B2_GRAVITY, 2)])

MIDIIpGame = MidiIpGame()
MainTimer = Timer()
ButtonGame = ButtonSequenceGame()

thread1 = threading.Thread(target=MainTimer.startTimer)
thread3 = threading.Thread(target=MIDIIpGame.startGame)
thread2 = threading.Thread(target=ButtonGame.startGame)

stop = False
while not stop:
    if isStartTimer:
        print("Starting Timer")
        thread1.start()
        isStartTimer = False
    if isStartMIDIIPGame:
        print("Starting MIDI-IP-Game")
        thread3.start()
        isStartMIDIIPGame = False
    if isStartButtonSequence:
        print("Starting Button-Sequence-Game")
        thread2.start()
        isStartButtonSequence = False

    
    if MIDIIpGame.getFinished():
        print("Stopping MIDI-IP-Game")
        MIDIIpGame.stopGame()
        client.publish(topic=MQTT_TOPIC_C1_RFID, payload="start", qos=2)
    if ButtonGame.getFinished():
        print("Stopping Button-Sequence-Game")
        ButtonGame.stopGame()
        client.publish(topic=MQTT_TOPIC_B2_GRAVITY, payload="on", qos=2)
        client.publish(topic=MQTT_TOPIC_DOOR_B5, payload="1", qos=2)
        client.publish(topic=MQTT_TOPIC_DOOR_A5, payload="1", qos=2)
        client.publish(topic=MQTT_TOPIC_DOOR_B3, payload="1", qos=2)
        client.publish(topic=MQTT_TOPIC_DOOR_A3, payload="1", qos=2)
        client.publish(topic=MQTT_TOPIC_DOOR_B2, payload="1", qos=2)
    if MainTimer.getFinished():
        print("Stopping Timer")
        client.publish(topic=MQTT_TOPIC_GEN_GLOBAL, payload="stop", qos=2)
        stop = True

    if thread1.is_alive():
        if thread2.is_alive():
            if thread3.is_alive():
                thread3.join()
            thread2.join()
        thread1.join()

client.disconnect()
client.loop_stop()