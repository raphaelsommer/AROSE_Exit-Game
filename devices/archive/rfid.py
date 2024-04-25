from mfrc522 import MFRC522  # Directly using MFRC522 class
import signal
import time

# GPIO Setup
""" 
SDA  = 8   (24)
SCK  = 11  (23)
MOSI = 10  (19)
MISO = 9   (21)
IRQ  = /
GND  = GND (20)
RST  = 25  (22)
3.3V = 3V3 (1)
"""


RIGHT_CARD_UID = {0xB3, 0xD8, 0x61, 0x1A, 0x10}

# Signal handler for a clean shutdown
def end_read():
    global continue_reading
    continue_reading = False
    reader.Close()
    print("Exiting gracefully")

signal.signal(signal.SIGINT, end_read)

# Initialize the RFID reader
reader = MFRC522()  # Ensure it's reinitialized with each loop


print("Ready to scan RFID tags. Please place a tag near the reader.")

try:
    continue_reading = True
    while continue_reading:
        print("... scanning ...")

        # Reinitialize the reader
        #reader.Init()  # Ensure the reader is ready for a new read operation

        # Request for a card
        status, TagType = reader.Request(reader.PICC_REQIDL)

        # If a card is detected, try to get its UID
        if status == reader.MI_OK:
            status, uid = reader.Anticoll()
            uid_str = "-".join(["%X" % x for x in uid])
            print(f"Card detected with UID: {uid_str}")

            if set(uid) == RIGHT_CARD_UID:
                print("You scanned the right card")
                end_read()
            else:
                print("You scanned the wrong one")

                # Halt card to allow new scans
                #reader.AntennaOff()
                #reader.StopCrypto1()

        # Wait a short time before the next iteration to prevent high CPU usage
        time.sleep(0.5)
except KeyboardInterrupt:
    reader.Close()  # Clean up resources