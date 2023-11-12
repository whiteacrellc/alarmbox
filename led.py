from gpiozero import LED
from time import sleep

def led_test():
    for i in range(15, 31):
        print(i)
        led = LED(i)
        led.led_on()
        sleep(3)
        led.led_off()

if __name__ == '__main__':
    led_test()
