import Adafruit_CharLCD as LCD
import time
import mido
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

# USB MIDI Port configuration:
PORT = 'Akai LPK25 Wireless:Akai LPK25 Wireless MIDI 1 20:0'

# Raspberry Pi pin configuration:
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 21
lcd_d7 = 22
buzzer = TonalBuzzer(20)

# Define LCD column and row size
lcd_columns = 16
lcd_rows = 2

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)
lcd.clear()
lcd.message('Enter door IP\nvia MIDI Piano')

# Initialize the IP input
IP_entered = []

### MAIN Program
try:
    with mido.open_input(PORT) as listener:
        for input in listener:
            if len(IP_entered) > 3:
                break
            if not input.is_meta and input.type == 'note_on':
                IP_part = input.note
                buzzer.play(Tone(midi=IP_part))
                IP_entered.append((IP_part-32)*6)
                IP_string = '.'.join(str(ip) for ip in IP_entered)
                lcd.clear()
                lcd.message(f'Change door1 IP:\n{IP_string}')
                time.sleep(0.5)
                buzzer.stop()
    lcd.clear()
    lcd.message(f'door1 IP now is\n{IP_string}')
    time.sleep(1)
    
    ### LATER: Send MQTT Message to door that it can be openend 
    print(f"Send door1 IP {IP_string}")
    lcd.clear()

except KeyboardInterrupt:
    lcd.clear()  
