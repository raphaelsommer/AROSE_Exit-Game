import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import threading
import RPi.GPIO as GPIO
import logging
import os

from ip_game import IP
from morse_game import Morse
from rfid_game import RFID
from wire_game import Wire


# MQTT Konfigurationen
MQTT_BROKER = "192.168.0.102"  # Beispiel-Broker, ersetze diesen durch deinen Broker
MQTT_PORT = 1883
MQTT_TRANSPORT_PROTOCOL = "tcp"
CLIENT_ID = "rp3"

### Needed MQTT Topics
MQTT_TOPIC_RP3 = "/rp3"  # will
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

# Initialize the games
MorseGame = Morse()
RfidGame = RFID()
IpGame = IP()
WireGame = Wire()

# Set up the logger
log_directory = "/home/rsommer/dhbw-wwi23h-systemanalyse-team1/devices/rp3"
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(log_directory, "rp3.log")
Logger = logging.getLogger("RP3")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set up GPIO mode once
GPIO.setmode(GPIO.BCM)

# "Prepare" (instantiate) threads for the games
thread1 = threading.Thread(target=None)
thread2 = threading.Thread(target=None)
thread3 = threading.Thread(target=None)
thread4 = threading.Thread(target=None)


### MQTT Methods
def on_message(client, userdata, msg):
    global isStartMorseGame, isStartRfidGame, isStartIpGame, isStartWireGame, stop
    #print(msg.topic + " " + str(msg.payload))
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'start':
        print("Morse-Game start")
        isStartMorseGame = True
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'stop':
        print("Game over!")
        stop = True
    if msg.topic == MQTT_TOPIC_GEN_GLOBAL and msg.payload.decode() == 'timeOver':
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
    '''# TEST MESSAGE FOR THE WIRE GAME
    if msg.topic == MQTT_TOPIC_RK_WIRE and msg.payload.decode() == '1':
        print("Wire touched")
        WireGame.changeState(1)
    if msg.topic == MQTT_TOPIC_RK_WIRE and msg.payload.decode() == '2':
        print("Nail touched - Wire not touched")
        WireGame.changeState(2)'''
    Logger.info("Received topic: " + msg.topic.decode("utf-8") + ", message: " + msg.payload.decode("utf-8"))

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected: " + str(reason_code))
    Logger.info("Connected client " + CLIENT_ID + " with reason code: " + str(reason_code))
    client.publish(topic=MQTT_TOPIC_RP3, payload="connected", qos=2, retain=True)

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
client.username_pw_set(username="rp3", password="rp3Arose1234!")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_connect_fail = on_connect_fail
client.on_log = on_log
properties = Properties(PacketTypes.CONNECT)
client.enable_logger()
client.will_set(MQTT_TOPIC_RP3, payload="disconnected", qos=2, retain=True)
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Starte den MQTT-Client im Hintergrund
client.subscribe([(MQTT_TOPIC_GEN_GLOBAL, 0), (MQTT_TOPIC_C1_RFID, 2), (MQTT_TOPIC_C0_IP, 2), (MQTT_TOPIC_RK_WIRE, 2)])



stop = False
threads_started = {thread1: False, thread2: False, thread3: False, thread4: False}

try:
    while not stop:    
        if not thread1.is_alive() and not threads_started[thread1] and isStartMorseGame:
            #isStartMorseGame = False
            thread1 = threading.Thread(target=MorseGame.startGame)
            thread1.start()
            threads_started[thread1] = True
        if not thread2.is_alive() and not threads_started[thread2] and isStartRfidGame:
            #isStartRfidGame = False
            thread2 = threading.Thread(target=RfidGame.startGame)
            thread2.start()
            threads_started[thread2] = True
        if not thread3.is_alive() and not threads_started[thread3] and isStartIpGame:
            #isStartIpGame = False
            thread3 = threading.Thread(target=IpGame.listen)
            thread3.start()
            threads_started[thread3] = True
        if not thread4.is_alive() and not threads_started[thread4] and isStartWireGame:
            #isStartWireGame = False
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
        if (WireGame.getGameState() == 1 or WireGame.getGameState() == 2) and not isStoppedWireGame:
            print("Stopping Wire-Game")
            isStoppedWireGame = True
            if WireGame.getGameState() == 2:
                client.publish(topic=MQTT_TOPIC_RK_WIRE, payload="win", qos=2)
            elif WireGame.getGameState() == 1:
                client.publish(topic=MQTT_TOPIC_RK_WIRE, payload="fail", qos=2)
            stop = True


        for thread in [thread1, thread2, thread3, thread4]:
            if threads_started[thread] and not thread.is_alive():
                thread.join()
                threads_started[thread] = False


except KeyboardInterrupt:
    if isStartMorseGame:
        MorseGame.stopGame()
    if isStartRfidGame:
        RfidGame.stopGame()
    if isStartIpGame:
        IpGame.stop()
    if isStartWireGame:
        WireGame.stopGame
finally:
    if not isStoppedMorseGame:
        MorseGame.stopGame()
    if not isStoppedRfidGame:
        RfidGame.stopGame()
    if not isStoppedIpGame:
        IpGame.stop()
    if not isStoppedWireGame:
        WireGame.stopGame()
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
