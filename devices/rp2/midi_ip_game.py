# Import libraries for handling: LCD Display, MIDI input, Tonal GPIO Buzzer, Time (for artificial delays)
import Adafruit_CharLCD as LCD
import mido
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time

##### Define a class for the MIDI IP Game which is going to be instantiated in the main.py file
class MidiIpGame:
    ### Define the constructor of the class
    def __init__(self):
        # Configure the USB MIDI Port:
        self.PORT = 'Akai LPK25 Wireless:Akai LPK25 Wireless MIDI 1 24:0'
        
        # Configure the Raspberry Pi pins for the LCD Display and the Buzzer:
        self.lcd_rs = 24
        self.lcd_en = 23
        self.lcd_d4 = 22
        self.lcd_d5 = 27
        self.lcd_d6 = 17
        self.lcd_d7 = 25
        self.buzzer = TonalBuzzer(18)
        
        # Define LCD column and row size
        self.lcd_columns = 16
        self.lcd_rows = 2
        
        # Initialize the LCD using the pins
        self.lcd = LCD.Adafruit_CharLCD(self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7,
                                   self.lcd_columns, self.lcd_rows)
        # Clear the LCD Display to avoid any previous messages and to prevent any errors and glitches
        self.lcd.clear()
        
        # Initialize the IP input which is going to be "entered" by the user via the MIDI Piano and is the foundation for the IP address of the doors: if both are right, then the "big door to the cockpit" can be opened
        self.IP1_entered = []
        self.IP2_entered = []
        self.areBothIPsRight = False

    ### Define a method to revert the entered IP address back to the initial state so that it can be re-entered
    def resetIP(self, IP):
        IP = []
        return IP
    
    ### Define a method to convert the entered IP address from a list of integers to a string
    def IPToString(self, IP):
        IP_string = '.'.join(str(ip) for ip in IP)
        return IP_string

    ### Define a method to enter the IP address via the MIDI Piano
    def enterIP(self, IP_entered, door):
        with mido.open_input(self.PORT) as listener:
            for input in listener:
                if len(IP_entered) > 3:
                          break
                if not input.is_meta and input.type == 'note_on':
                    IP_part = input.note
                    self.buzzer.play(Tone(midi=IP_part))
                    IP_entered.append((IP_part-32)*6)
                    self.lcd.clear()
                    self.lcd.message(f'Change door{door} IP:\n{self.IPToString(IP_entered)}')
                    time.sleep(0.5)
                    self.buzzer.stop()

    ### Define a method to start the IP Game from the main.py file
    def startGame(self):
        try:
            while not self.areBothIPsRight:
                self.enterIP(self.IP1_entered, 1)
                self.enterIP(self.IP2_entered, 2)
                if (self.IP1_entered == [192, 168, 180, 198] and self.IP2_entered == [192, 168, 222, 210]):
                    self.areBothIPsRight = True
                    self.lcd.clear()
                    self.lcd.message('Both IPs are\nright!')
                    time.sleep(1)
                    self.lcd.clear()
                    self.lcd.message('You can open the\ndouble door now!')
                    time.sleep(2)
                    self.lcd.clear()
                else:
                    self.lcd.clear()
                    self.lcd.message('At least one IP\nis wrong!')
                    time.sleep(1)
                    self.lcd.clear()
                    self.lcd.message('Please try\nagain... ')
                    time.sleep(1)
                    self.lcd.clear()
                    self.IP1_entered = self.resetIP(self.IP1_entered)
                    self.IP2_entered = self.resetIP(self.IP2_entered)
        except KeyboardInterrupt:
            self.lcd.clear()

    ### Define a method to stop/interrupt the IP Game from the main.py file
    def stopGame(self):
        self.lcd.clear()
        self.buzzer.stop()
        self.resetIP(self.IP1_entered)
        self.resetIP(self.IP2_entered)
        self.areBothIPsRight = False