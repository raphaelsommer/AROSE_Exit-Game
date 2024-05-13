from gpiozero import Buzzer
import spidev
import time

##### Define a class for the Timer which is going to be instantiated in the main.py file
class Timer:

    # Define segment codes for 0-9 on a 7-segment display
    SEGMENT_MAP = {
        '0': 0b01111110,
        '1': 0b00110000,
        '2': 0b01101101,
        '3': 0b01111001,
        '4': 0b00110011,
        '5': 0b01011011,
        '6': 0b01011111,
        '7': 0b01110000,
        '8': 0b01111111,
        '9': 0b01111011,
    }

    # Buzzer Configuration
    buzzer = Buzzer(12)

    # Display configuration
    DISPLAY_BRIGHTNESS = 8
    NUM_DIGITS = 4

    # Timer variables
    ''' start = False '''
    start = True
    stopped = False
    timerFinished = False
    INITTIME = 17
    timerMin10 = (INITTIME - (INITTIME % 10)) // 10
    timerMin1 = INITTIME % 10
    timerSec10 = 5
    timerSec1 = 8

    ### Define the constructor of the class
    def __init__(self):
        # SPI Configuration
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Open SPI bus 0, device 0
        self.spi.max_speed_hz = 5000
        self.setup_display()

    ### Define a method to write a byte to the display
    def write_byte(self, register, data):
        self.spi.xfer2([register, data])

    ### Define a method to setup the display
    def setup_display(self):
        # Initialize display
        self.write_byte(0x0c, 0x01)  # Shutdown register
        self.write_byte(0x0a, self.DISPLAY_BRIGHTNESS)  # Intensity register
        self.write_byte(0x0b, 0x07)  # Scan limit register (show all digits)
        self.clear_display()

    ### Define a method to clear the display
    def clear_display(self):
        for digit in range(1, 9):
            self.write_byte(digit, 0x00)
    
    ### Define a method to display a digit on the display
    def display_digit(self, position, value, colon=False):
        if 0 <= value <= 9:
            data = self.SEGMENT_MAP[str(value)]
            if colon:
                data |= 0x80
            self.write_byte(position, data)

    ### Define a method to play the alarm sound
    def alarm(self):
        count5sec = 0
        start_time = time.time()
        while count5sec < 5:
            current_time = time.time()
            elapsed = current_time - start_time
            if elapsed >= 0.5:
                self.buzzer.on()
                self.display_digit(1, 0, True)
                self.display_digit(2, 0, True)
                self.display_digit(3, 0, True)
                self.display_digit(4, 0, True)
                time.sleep(0.5)
                self.buzzer.off()
                self.clear_display()
                time.sleep(0.5)
                count5sec += 1
                start_time = current_time

    ### Define a method to get the status of the timer for the main.py file
    def getFinished(self):
        return self.timerFinished
    
    ### Define a method to get the rest time of the timer for the main.py file (last will message)
    def getRestTimeInSeconds(self):
        return (self.timerMin10 * 600) + (self.timerMin1 * 60) + (self.timerSec10 * 10) + self.timerSec1
    
    ### Define a method to start the timer
    def startTimer(self):
        self.startTime = time.time()
        while ((not self.stopped) and self.start):
            self.currentTime = time.time()
            if (self.currentTime - self.startTime) >= 0.1:
                self.display_digit(1, self.timerMin10, False)
                self.display_digit(2, self.timerMin1, (int(self.timerSec1)%2)==0)
                self.display_digit(3, self.timerSec10, False)
                self.display_digit(4, self.timerSec1, False)
                if self.timerSec1 == 0:
                    if self.timerSec10 == 0:
                        if self.timerMin1 == 0:
                            if self.timerMin10 == 0:
                                self.stopped = True
                    
                            self.timerMin10 -= 1
                            self.timerMin1 = 10
                        
                        self.timerMin1 -= 1
                        self.timerSec10 = 6
                    
                    self.timerSec10 -= 1
                    self.timerSec1 = 10
                
                self.timerSec1 -= 1
                self.startTime = self.currentTime
        self.clear_display()
        self.alarm()
        self.timerFinished = True
        self.stopTimer()

    ### Define a method to stop the timer
    def stopTimer(self):
        self.stopped = True
        self.clear_display()
        self.timerMin10 = (self.INITTIME - (self.INITTIME % 10)) // 10
        self.timerMin1 = self.INITTIME % 10
        self.timerSec10 = 0
        self.timerSec1 = 0
