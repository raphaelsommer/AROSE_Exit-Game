import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import ssl
import threading

# MQTT Konfigurationen
MQTT_BROKER = "192.168.0.102"  # Beispiel-Broker, ersetze diesen durch deinen Broker
MQTT_PORT = 1883
MQTT_TRANSPORT_PROTOCOL = "tcp"

MQTT_TOPIC_GEN_START = "/gen/start"
MQTT_TOPIC_GEN_STOP = "/gen/stop"
MQTT_TOPIC_DOOR_A5 = "/door/a5"
MQTT_TOPIC_C1_RFID = "/c1/rfid"

isStartMIDIIPGame = False
isStartTimer = False

# MQTT Methods
def on_message(client, userdata, msg):
    global isStartMIDIIPGame, isStartTimer
    # print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_START and msg.payload.decode() == '1':
        print("Timer start")
        isStartTimer = True
    if msg.topic == MQTT_TOPIC_DOOR_A5 and msg.payload.decode() == '1':
        print("Door from A-4 to A-5 opened, starting MIDI-IP-Game")
        isStartMIDIIPGame = True



# Client Setup
client = mqtt.Client(client_id="rp3", protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="rp3_sub", password="rp3arose1234!")
###client.on_connect = on_connect
client.on_message = on_message

properties = Properties(PacketTypes.CONNECT)
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
###client.publish("/test", "Test 2")
client.subscribe([(MQTT_TOPIC_GEN_START, 2), (MQTT_TOPIC_GEN_STOP, 2), (MQTT_TOPIC_DOOR_A5, 2)])


# MAIN LOOP
stop = False
while not stop:
    if isStartTimer:
        print("Starting Timer")
        Timer = Timer()
        thread1 = threading.Thread(target=Timer.startTimer).start()
    if isStartMIDIIPGame:
        print("Starting MIDI-IP-Game")
        MIDIIpGame = MIDIIpGame()
        thread2 = threading.Thread(target=MIDIIpGame.startGame).start()
        isStartMIDIIPGame = False
    if MIDIIpGame.getFinished():
        print("Stopping MIDI-IP-Game")
        MIDIIpGame.stopGame()
        client.publish(topic=MQTT_TOPIC_C1_RFID, payload="1", qos=2)

    
    thread1.join()
    thread2.join()

client.disconnect()
client.loop_stop()