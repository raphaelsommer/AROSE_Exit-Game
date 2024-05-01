import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes

# MQTT Konfigurationen
MQTT_BROKER = "192.168.0.102"  # Beispiel-Broker, ersetze diesen durch deinen Broker
MQTT_PORT = 1883

### Needed MQTT Topics
# Topics for General and Timer
MQTT_TOPIC_GEN_GLOBAL = "/gen/global" # sub/pub
# Topics for the MIDI-IP-Game
MQTT_TOPIC_A5_PIANO = "/a5/piano" # pub
# Topics for the Gravity-Room and Button-Sequence-Game
MQTT_TOPIC_B2_GRAVITY = "/b2/gravity" # sub/pub
# Topics for the IP-Game and Wire-Game
MQTT_TOPIC_C0_IP = "/c0/ip" # sub/pub
MQTT_TOPIC_RK_WIRE = "/rk/wire" # sub/pub
# Topics for opening doors
MQTT_DOORS = "/doors/+" # sub/pub

### MQTT Methods
def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'stop':
        print("Time ran out - Game over!")
    if msg.topic == MQTT_TOPIC_B2_GRAVITY and msg.payload.decode() == 'off':
        print("Closed door to B3")
        client.publish(topic="/doors/b3", payload="0", qos=2)
    if msg.topic == "/doors/b2" and msg.payload.decode() == '1':
        print("Opened door to B2")
    if msg.topic == "/doors/b3" and msg.payload.decode() == '1':
        print("Opened door to B3")
    if msg.topic == "doors/b4" and msg.payload.decode() == '1':
        print("Opened door to B4")
    if msg.topic == "doors/b5" and msg.payload.decode() == '1':
        print("Opened door to B5")
    if msg.topic == "doors/a3" and msg.payload.decode() == '1':
        print("Opened door to A3")
    if msg.topic == "doors/a4" and msg.payload.decode() == '1':
        print("Opened door to A4")
    if msg.topic == "doors/a5" and msg.payload.decode() == '1':
        print("Opened door to A5")
    if msg.topic == "doors/jnr" and msg.payload.decode() == '1':
        print("Opened door to JNR")
    if msg.topic == "doors/rk" and msg.payload.decode() == '1':
        print("Opened door to RK")
    

##### Client Setup
client = mqtt.Client(client_id="rp2", protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="rp2", password="rp2Arose1234!")
'''client.on_connect = on_connect'''
client.on_message = on_message
properties = Properties(PacketTypes.CONNECT)
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
client.subscribe([(MQTT_TOPIC_GEN_GLOBAL, 2), (MQTT_TOPIC_B2_GRAVITY, 2), (MQTT_TOPIC_A5_PIANO, 2), (MQTT_DOORS, 2), (MQTT_TOPIC_C0_IP, 2), (MQTT_TOPIC_RK_WIRE, 2)])