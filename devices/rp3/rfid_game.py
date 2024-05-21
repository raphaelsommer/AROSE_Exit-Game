import threading
import time
import RPi.GPIO as GPIO
from mfrc522 import MFRC522

# GPIO Setup
""" 
+-------------------+-----------------------+-----------------------+
| RFID Module Pin   | Connection for RFID 1 | Connection for RFID 2 |
+-------------------+-----------------------+-----------------------+
| SDA (CS)          | GPIO 8 (CE0)          | GPIO 7 (CE1)          |
+-------------------+-----------------------+-----------------------+
| SCK               | GPIO 11 (SPI Clock)   | GPIO 11 (SPI Clock)   |
+-------------------+-----------------------+-----------------------+
| MOSI              | GPIO 10 (SPI MOSI)    | GPIO 10 (SPI MOSI)    |
+-------------------+-----------------------+-----------------------+
| MISO              | GPIO 9 (SPI MISO)     | GPIO 9 (SPI MISO)     |
+-------------------+-----------------------+-----------------------+
| IRQ               | Not connected         | Not connected         |
+-------------------+-----------------------+-----------------------+
| GND               | GND (20)              | GND (30)              |
+-------------------+-----------------------+-----------------------+
| RST               | GPIO 25               | GPIO 24               |
+-------------------+-----------------------+-----------------------+
| 3.3V              | 3.3V Pin              | 3.3V Pin              |
+-------------------+-----------------------+-----------------------+
"""

# Initialize the RFID Reader
class RFIDReader:
    def __init__(self, device, right_uid):
        self.device = device
        self.right_uid = right_uid
        self.reader = MFRC522(device=self.device)
        self.uid = None
        self.success = False

    def run(self):

        # Scans until both cards have been succesfully scanned
        while not self.success:
            print(f"Scanner {self.device} scanning...")
            status, TagType = self.reader.Request(self.reader.PICC_REQIDL)
            if status == self.reader.MI_OK:
                status, uid = self.reader.Anticoll()
                if status == self.reader.MI_OK:
                    self.uid = "-".join(["%X" % x for x in uid])
                    print(f"Scanner {self.device} detected card with UID: {self.uid}")
                    if set(uid) == self.right_uid:
                        print(f"Scanner {self.device}: Correct card!")
                        self.success = True
                    else:
                        print(f"Scanner {self.device}: Incorrect card.")
            time.sleep(0.5)

#Defines Class RFID
class RFID:

    finished = False
    left = False
    right = False

    RIGHT_CARD_UID1 = {0xB3, 0xD8, 0x61, 0x1A, 0x10}
    RIGHT_CARD_UID2 = {0x3, 0x41, 0x8D, 0x1A, 0xD5}

    scanner1 = RFIDReader(device=0, right_uid=RIGHT_CARD_UID1)
    scanner2 = RFIDReader(device=1, right_uid=RIGHT_CARD_UID2)

    stopReader = False

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getFinished(self):
        return self.finished

    def stopGame(self):
        self.scanner1.reader.Close()
        self.scanner2.reader.Close()

    def startGame(self):

        
# Initialize threads for scanners
        thread1 = threading.Thread(target=self.scanner1.run)
        thread2 = threading.Thread(target=self.scanner2.run)

        thread1.start()
        thread2.start()

# Check if scan was successful
        while not self.finished:

            if self.scanner1.success and not self.finished:
                print("Scanned left")
                self.left = True

            if self.scanner2.success and not self.finished:
                print("Scanned right")
                self.right = True

            if self.scanner1.success and self.scanner2.success and not self.finished:
                print("Success! Both correct cards detected simultaneously.")
                self.finished = True
                self.stopGame()
            else:
                print("The program did not end with both scanners detecting the correct cards.")
# Start threads
            thread1.join()
            thread2.join()



    """ if __name__ == "__main__":
        try:
            main()
        except KeyboardInterrupt:
            GPIO.cleanup() """
