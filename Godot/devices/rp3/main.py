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


# MQTT Methods
def on_message(client, userdata, msg):
    global start, stopped
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_START and msg.payload.decode() == '1':
        print("Timer start")
        start = True
    if msg.topic == MQTT_TOPIC_CO2_MASKS and msg.payload.decode() == '1':
        print("CO2 mask detected, extending timer")
        ###extend_timer(8)
    if msg.topic == MQTT_TOPIC_GEN_STOP and msg.payload.decode() == '1':
        print("Timer stopped")
        stopped = True


# Client Setup
client = mqtt.Client(client_id="rp3", protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="rp3_sub", password="rp3arose1234!")
###client.on_connect = on_connect
client.on_message = on_message

properties = Properties(PacketTypes.CONNECT)
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
###client.publish("/test", "Test 2")
client.subscribe([(MQTT_TOPIC_GEN_START, 0), (MQTT_TOPIC_CO2_MASKS, 0), (MQTT_TOPIC_GEN_STOP, 0)])


# MAIN LOOP
finished = False
while not finished:
    print("...waiting...")
    if start:
        print("doing something")
        ###startTimer()
    time.sleep(1)

""" if __name__ == '__main__':
    startTimer()
 """

client.disconnect()
client.loop_stop()