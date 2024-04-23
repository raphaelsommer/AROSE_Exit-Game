from gpiozero import Buzzer
import time

buzzer = Buzzer(21)

def main():
    count5sec = 0
    start_time = time.time()
    while count5sec < 5:            
        current_time = time.time()
        elapsed = current_time - start_time
        if elapsed >= 0.5:
            buzzer.on()
            time.sleep(0.5)
            buzzer.off()
            time.sleep(0.5)
            count5sec += 1
            start_time = current_time 

if __name__ == '__main__':
    main()