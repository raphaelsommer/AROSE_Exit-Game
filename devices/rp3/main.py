import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import threading
import RPi.GPIO as GPIO

from ip_game import IP
from morse_game import Morse
from rfid_game import RFID
from wire_game import Wire


# MQTT Konfigurationen
MQTT_BROKER = "192.168.0.102"  # Beispiel-Broker, ersetze diesen durch deinen Broker
MQTT_PORT = 1883
MQTT_TRANSPORT_PROTOCOL = "tcp"

### Needed MQTT Topics
# Topics for General and Morse-Game
MQTT_TOPIC_GEN_GLOBAL = "/gen/global" # sub/pub
MQTT_TOPIC_B3_MORSE = "/b3/morse" # pub
# Topics for the RFID-Game
MQTT_TOPIC_C1_RFID = "/c1/rfid" # sub/pub
# Topics for the IP-Game
MQTT_TOPIC_C0_IP = "/c0/ip" # sub/pub
# Topics for the Wire-Game
MQTT_TOPIC_RK_WIRE = "/rk/wire" # sub/pub


# Flags for the Morse, RFID, MAC and Wire Game
isStartMorseGame = False
isStartRfidGame = False
isStartIpGame = False
isStartWireGame = False

isStoppedMorseGame = False
isStoppedRfidGame = False
isStoppedIpGame = False
isStoppedWireGame = False


### MQTT Methods
def on_message(client, userdata, msg):
    global isStartMorseGame, isStartRfidGame, isStartIpGame, isStartWireGame, stop
    #print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'start':
        print("Morse-Game start")
        isStartMorseGame = True
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'stop':
        print("Time ran out - Game over!")
        stop = True
    if msg.topic == MQTT_TOPIC_C1_RFID and msg.payload.decode() == 'start':
        print("RFID-Game start")
        isStartRfidGame = True
    if msg.topic == MQTT_TOPIC_C0_IP and msg.payload.decode() == 'start':
        print("IP-Game start")
        isStartIpGame = True
    if msg.topic == MQTT_TOPIC_RK_WIRE and msg.payload.decode() == 'start':
        print("Wire-Game start")
        isStartWireGame = True
    # TEST MESSAGE FOR THE WIRE GAME
    if msg.topic == MQTT_TOPIC_RK_WIRE and msg.payload.decode() == '1':
        print("Wire touched")
        WireGame.changeState(1)
    if msg.topic == MQTT_TOPIC_RK_WIRE and msg.payload.decode() == '2':
        print("Nail touched - Wire not touched")
        WireGame.changeState(2)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected:" + str(reason_code))


##### Client Setup
client = mqtt.Client(client_id="rp3", protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="rp3", password="rp3Arose1234!")
client.on_connect = on_connect
client.on_message = on_message
properties = Properties(PacketTypes.CONNECT)
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
client.subscribe([(MQTT_TOPIC_GEN_GLOBAL, 0), (MQTT_TOPIC_C1_RFID, 2), (MQTT_TOPIC_C0_IP, 2), (MQTT_TOPIC_RK_WIRE, 2)])

#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

MorseGame = Morse()
RfidGame = RFID()
IpGame = IP()
WireGame = Wire()

thread1 = threading.Thread(target=None)
thread2 = threading.Thread(target=None)
thread3 = threading.Thread(target=None)
thread4 = threading.Thread(target=None)

stop = False
threads_started = {thread1: False, thread2: False, thread3: False, thread4: False}

try:

    while not stop:
        
        if (not thread1.is_alive()) and (not threads_started[thread1]) and isStartMorseGame:
            isStartMorseGame = False
            thread1 = threading.Thread(target=MorseGame.startGame)
            thread1.start()
            threads_started[thread1] = True
        if not thread2.is_alive() and not threads_started[thread2] and isStartRfidGame:
            isStartRfidGame = False
            thread2 = threading.Thread(target=RfidGame.startGame)
            thread2.start()
            threads_started[thread2] = True
        if not thread3.is_alive() and not threads_started[thread3] and isStartIpGame:
            isStartIpGame = False
            thread3 = threading.Thread(target=IpGame.listen)
            thread3.start()
            threads_started[thread3] = True
        if not thread4.is_alive() and not threads_started[thread4] and isStartWireGame:
            isStartWireGame = False
            thread4 = threading.Thread(target=WireGame.startGame)
            thread4.start()
            threads_started[thread4] = True

        
        if MorseGame.getFinished() and not isStoppedMorseGame:
            print("Stopping Morse-Game")
            #MorseGame.stopGame()
            isStoppedMorseGame = True
            client.publish(topic=MQTT_TOPIC_B3_MORSE, payload="finished", qos=2)
        if RfidGame.getFinished() and not isStoppedRfidGame:
            print("Stopping Rfid-Game")
            isStoppedRfidGame = True
            client.publish(topic=MQTT_TOPIC_C1_RFID, payload="finished", qos=2)
        if (IpGame.getIP() != "") and not isStoppedIpGame:
            print("Stopping IP-Game")
            isStoppedIpGame = True
            client.publish(topic=MQTT_TOPIC_C0_IP, payload="finished", qos=2)
        if (WireGame.getSuccess or WireGame.getFailed) and not isStoppedWireGame:
            print("Stopping Wire-Game")
            isStoppedWireGame = True
            if WireGame.getSuccess():
                client.publish(topic=MQTT_TOPIC_RK_WIRE, payload="win", qos=2)
            elif WireGame.getFailed():
                client.publish(topic=MQTT_TOPIC_RK_WIRE, payload="fail", qos=2)
            #stop = True


        for thread in [thread1, thread2, thread3, thread4]:
            if threads_started[thread] and not thread.is_alive():
                thread.join()
                threads_started[thread] = False


except KeyboardInterrupt:
    MorseGame.stopGame()
    RfidGame.stopGame()
    IpGame.stop()
    # WireGame.stopGame()
finally:
    if not isStoppedMorseGame:
        MorseGame.stopGame()
    if not isStoppedRfidGame:
        RfidGame.stopGame()
    if not isStoppedIpGame:
        IpGame.stop()
    # if not isStoppedWireGame:
    #     WireGame.stopGame()
    GPIO.cleanup()
    client.disconnect()
    client.loop_stop()