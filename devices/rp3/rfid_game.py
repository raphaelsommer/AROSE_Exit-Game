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

class RFIDReader:
    def __init__(self, device, right_uid):
        self.device = device
        self.right_uid = right_uid
        self.reader = MFRC522(device=self.device)
        self.uid = None
        self.success = False

    def run(self):
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

class RFID:

    finished = False
    RIGHT_CARD_UID1 = {0xB3, 0xD8, 0x61, 0x1A, 0x10}
    RIGHT_CARD_UID2 = {0x3, 0x41, 0x8D, 0x1A, 0xD5}

    scanner1 = RFIDReader(device=0, right_uid=RIGHT_CARD_UID1)
    scanner2 = RFIDReader(device=1, right_uid=RIGHT_CARD_UID2)

    def getFinished(self):
        return self.finished

    def stopGame(self):
        global scanner1, scanner2
        scanner1.reader.Close()
        scanner2.reader.Close()

    def startGame(self):

        thread1 = threading.Thread(target=scanner1.run)
        thread2 = threading.Thread(target=scanner2.run)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        if scanner1.success and scanner2.success:
            print("Success! Both correct cards detected simultaneously.")
            self.finished = True
            self.stopGame(scanners=(scanner1, scanner2))
        else:
            print("The program did not end with both scanners detecting the correct cards.")

    """ if __name__ == "__main__":
        try:
            main()
        except KeyboardInterrupt:
            GPIO.cleanup() """