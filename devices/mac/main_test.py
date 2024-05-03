import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import time

# MQTT Konfigurationen
MQTT_BROKER = "192.168.0.102"  # Beispiel-Broker, ersetze diesen durch deinen Broker
MQTT_PORT = 1883

### Needed MQTT Topics
# Topics for General and Timer
MQTT_TOPIC_GEN_GLOBAL = "/gen/global" # sub/pub
# Topics for the Morse-Game
MQTT_TOPIC_B3_MORSE = "/b3/morse" # sub
# Topics for the Gravity-Room and Button-Sequence-Game
MQTT_TOPIC_B2_GRAVITY = "/b2/gravity" # sub/pub
MQTT_TOPIC_A3_BUTTON = "/a3/button" # sub
# Topics for the MIDI-IP-Game
MQTT_TOPIC_A5_PIANO = "/a5/piano" # pub
# Topics for the RFID-Game
MQTT_TOPIC_C1_RFID = "/c1/rfid" # sub
# Topics for the IP-Game and Wire-Game
MQTT_TOPIC_C0_IP = "/c0/ip" # sub/pub
MQTT_TOPIC_RK_WIRE = "/rk/wire" # sub/pub

### MQTT Methods
def on_message(client, userdata, msg):
    global stop
    # print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'start':
        print("Starting the game")
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'stop':
        print("Time ran out - Game over!")
        stop = True
    if msg.topic == MQTT_TOPIC_B3_MORSE and msg.payload.decode() == 'finished':
        print("Open door to B3")
        print("Open door to B4")
        print("Open door to A4")
    if msg.topic == MQTT_TOPIC_B2_GRAVITY and msg.payload.decode() == 'off':
        print("Close door to B3")
    if msg.topic == MQTT_TOPIC_A3_BUTTON and msg.payload.decode() == 'finished':
        print("Re-established gravity in B2")
        print("Open door to A3")
        print("Open door to A5")
        print("Open door to B2")
        print("Open door to B3")
    if msg.topic == MQTT_TOPIC_C1_RFID and msg.payload.decode() == 'finished':
        print("Open door to C0 (JnR)")
    if msg.topic == MQTT_TOPIC_C0_IP and msg.payload.decode() == 'finished':
        print("Open door to RK")
    if msg.topic == MQTT_TOPIC_RK_WIRE and msg.payload.decode() == 'win':
        print("Game finished - WIN")
    if msg.topic == MQTT_TOPIC_RK_WIRE and msg.payload.decode() == 'fail':
        print("Game finished - LOSE")
    
    
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected: " + str(reason_code))

##### Client Setup
client = mqtt.Client(client_id="rsMac", protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="rsMac", password="rsMacArose1234!")
client.on_connect = on_connect
client.on_message = on_message
properties = Properties(PacketTypes.CONNECT)
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
client.subscribe([(MQTT_TOPIC_GEN_GLOBAL, 0), (MQTT_TOPIC_B3_MORSE, 2), (MQTT_TOPIC_B2_GRAVITY, 2), (MQTT_TOPIC_A3_BUTTON, 2), (MQTT_TOPIC_C1_RFID, 2), (MQTT_TOPIC_C0_IP, 2), (MQTT_TOPIC_RK_WIRE, 2)])

stop = False

while not stop:
    pass