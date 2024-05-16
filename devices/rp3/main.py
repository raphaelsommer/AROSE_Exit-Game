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

# MQTT Configuration
MQTT_BROKER = "192.168.0.102"  # The address of the MQTT broker
MQTT_PORT = 1883  # The port of the MQTT broker
MQTT_TRANSPORT_PROTOCOL = "tcp"  # The transport protocol to use
CLIENT_ID = "rp3"  # The client ID for the MQTT client

# MQTT Topics
MQTT_TOPIC_RP3 = "/rp3" # Last will topic
MQTT_TOPIC_GEN_GLOBAL = "/gen/global" # sub/pub global topic for start/stop signals
MQTT_TOPIC_B3_MORSE = "/b3/morse" # pub Topic for the Morse game
MQTT_TOPIC_C1_RFID = "/c1/rfid" # sub/pub Topic for the RFID game
MQTT_TOPIC_C0_IP = "/c0/ip" # sub/pub Topic for the IP game
MQTT_TOPIC_RK_WIRE = "/rk/wire" # sub/pub Topic for the Wire game

# Game Flags
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
log_directory = "/home/rsommer/Documents/dhbw-wwi23h-systemanalyse-team1/devices/rp3"
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(log_directory, "rp3.log")
Logger = logging.getLogger("RP3")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set up GPIO mode once
GPIO.setmode(GPIO.BCM)

# Prepare threads for the games
threads = {
    'Morse': threading.Thread(target=None),
    'RFID': threading.Thread(target=None),
    'IP': threading.Thread(target=None),
    'Wire': threading.Thread(target=None)
}
threads_started = {key: False for key in threads.keys()}

### MQTT Methods
def on_message(client, userdata, msg):
    global isStartMorseGame, isStartRfidGame, isStartIpGame, isStartWireGame, stop

    if msg.topic == MQTT_TOPIC_GEN_GLOBAL:
        payload = msg.payload.decode()
        if payload == 'start':
            print("Starting Morse Game")
            isStartMorseGame = True
        elif payload == 'stop':
            stop = True
        elif payload == 'timeOver':
            stop = True

    if msg.topic == MQTT_TOPIC_C1_RFID and msg.payload.decode() == 'start':
        print("Starting RFID Game")
        isStartRfidGame = True

    if msg.topic == MQTT_TOPIC_C0_IP and msg.payload.decode() == 'start':
        print("Starting IP Game")
        isStartIpGame = True

    if msg.topic == MQTT_TOPIC_RK_WIRE and msg.payload.decode() == 'start':
        print("Starting Wire Game")
        isStartWireGame = True

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected: " + str(reason_code))
    client.publish(topic=MQTT_TOPIC_RP3, payload="connected", qos=2, retain=True)

def on_connect_fail(client, userdata, properties, reason_code):
    print("Connection failed: " + str(reason_code))

def on_disconnect(client, userdata, flags, reason_code, properties):
    print("Disconnected: " + str(reason_code))

def on_log(client, userdata, level, buf):
    if level in (1, 2):
        Logger.info(buf)
    elif level == 4:
        Logger.warning(buf)
    elif level == 8:
        Logger.error(buf)
    else:
        Logger.debug(buf)

# Client Setup
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv5, transport=MQTT_TRANSPORT_PROTOCOL)
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
client.loop_start()
client.subscribe([(MQTT_TOPIC_GEN_GLOBAL, 0), (MQTT_TOPIC_C1_RFID, 2), (MQTT_TOPIC_C0_IP, 2), (MQTT_TOPIC_RK_WIRE, 2)])

stop = False

try:
    while not stop:
        # Start threads based on game flags
        if not threads['Morse'].is_alive() and not threads_started['Morse'] and isStartMorseGame and not isStoppedMorseGame:
            isStartMorseGame = False
            threads['Morse'] = threading.Thread(target=MorseGame.startGame)
            threads['Morse'].start()
            threads_started['Morse'] = True
        
        if not threads['RFID'].is_alive() and not threads_started['RFID'] and isStartRfidGame and not isStoppedRfidGame:
            isStartRfidGame = False
            threads['RFID'] = threading.Thread(target=RfidGame.startGame)
            threads['RFID'].start()
            threads_started['RFID'] = True
        
        if not threads['IP'].is_alive() and not threads_started['IP'] and isStartIpGame and not isStoppedIpGame:
            isStartIpGame = False
            threads['IP'] = threading.Thread(target=IpGame.listen)
            threads['IP'].start()
            threads_started['IP'] = True
        
        if not threads['Wire'].is_alive() and not threads_started['Wire'] and isStartWireGame and not isStoppedWireGame:
            isStartWireGame = False
            threads['Wire'] = threading.Thread(target=WireGame.startGame)
            threads['Wire'].start()
            threads_started['Wire'] = True

        # Handle game completion and MQTT notifications
        if MorseGame.getFinished() and not isStoppedMorseGame:
            print("Stopping Morse Game")
            isStoppedMorseGame = True
            client.publish(topic=MQTT_TOPIC_B3_MORSE, payload="finished", qos=2)
        
        if RfidGame.getLeft() and not isStoppedRfidGame:
            print("RFID Game: Left scanned")
            client.publish(topic=MQTT_TOPIC_C1_RFID, payload="left", qos=2)
        if RfidGame.getRight() and not isStoppedRfidGame:
            print("RFID Game: Right scanned")
            client.publish(topic=MQTT_TOPIC_C1_RFID, payload="right", qos=2)
        if RfidGame.getFinished() and not isStoppedRfidGame:
            print("Stopping RFID Game")
            isStoppedRfidGame = True
            client.publish(topic=MQTT_TOPIC_C1_RFID, payload="finished", qos=2)
        
        if IpGame.getIP() != "" and not isStoppedIpGame:
            print("IP Game: IP scanned")
            isStoppedIpGame = True
            client.publish(topic=MQTT_TOPIC_C0_IP, payload="finished", qos=2)
        
        if (WireGame.getGameState() in [1, 2]) and not isStoppedWireGame:
            print("Stopping Wire Game")
            isStoppedWireGame = True
            payload = "win" if WireGame.getGameState() == 1 else "fail"
            client.publish(topic=MQTT_TOPIC_RK_WIRE, payload=payload, qos=2)
            stop = True

        # Join finished threads
        for key, thread in threads.items():
            if threads_started[key] and not thread.is_alive():
                thread.join()
                threads_started[key] = False

except KeyboardInterrupt:
    # Ensure all games are stopped
    if isStartMorseGame:
        MorseGame.stopGame()
    if isStartRfidGame:
        RfidGame.stopGame()
    if isStartIpGame:
        IpGame.stop()
    if isStartWireGame:
        WireGame.stopGame()
finally:
    # Ensure proper cleanup
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