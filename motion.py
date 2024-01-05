#!/usr/bin/python
import daemonize
import signal
import os
from gpiozero import LED
from gpiozero import MotionSensor
from time import sleep
from threading import Thread
import threading
from datetime import datetime, timedelta
import argparse
import keyboard

ALERT_TIME_SECONDS = 10
green_led_on=False
green_led = LED(18)
red_led_on=False
red_led = LED(17)
blue_LED = LED(27)
PIR_sensor = MotionSensor(4)
# initialize last_time to 1 minute before the program starts
signal_event = threading.Event()
run_in_foreground = True

run_motion_thread=True
app_on=True


def greenled(on):
    global green_led
    global green_led_on
    # if state of led is the same return
    if green_led_on == on:
        return

    if on:
        green_led.on()
        green_led_on=True
    else:
        green_led.off()
        green_led_on=False

def redled(on):
    global red_led
    global red_led_on
    # if state of led is the same return
    if red_led_on == on:
        return

    if on:
        red_led.on()
        red_led_on=True
    else:
        red_led.off()
        red_led_on=False

def blink():
    for x in range(10):    
        blue_LED.off()
        red_led.on()
        green_led.off()
        sleep(0.25)
        green_led.on()
        red_led.off()
        sleep(0.25)
        blue_LED.on()
        sleep(0.25)
    blue_LED.on()

def handle_key_a():
    global app_on
    app_on=True
    blink()
    blue_LED.on()
    greenled(True)
    redled(False)
    print("Key 'a' pressed")

def handle_key_b():
    global app_on
    blink()
    app_on=False
    blue_LED.off()
    greenled(False)
    redled(False)
    print("Key 'b' pressed")

def handle_key_c():
    blink()
    print("Key 'c' pressed")

def handle_default():
    print("Unsupported key pressed")

def keyboard_run():
    key_handlers = {
        'a': handle_key_a,
        'b': handle_key_b,
        'c': handle_key_c,
    }

    while True:
        key_event = keyboard.read_event()

        if key_event.event_type == keyboard.KEY_DOWN:
            key_pressed = key_event.name.lower()
            key_handlers.get(key_pressed, handle_default)()
            
def seconds_since_last_time():
    global last_time
    now = datetime.now()
    diff_time = now - last_time
    seconds = diff_time.total_seconds()
    return int(seconds)

def motion_detected():
    global last_time
    last_time = datetime.now()
    #print("Motion Detected!")
    signal_event.set()
    redled(True)
    
def motion_thread():
    print("motion thread starting")
    global run_motion_thread
    while run_motion_thread:
        PIR_sensor.wait_for_motion()
        motion_detected()
    print("motion thread exiting")

# next lines define the variables with their input
# GPIO pin numbers and type of input they are
def run_motion():
    app_on=False
    blue_LED.on()
    global last_time
    last_time = datetime.now() - timedelta(60)
    signal_sent = False
    # Spin off a thread for the IR sensor
    motion_detection_thread = Thread(target=motion_thread)
    motion_detection_thread.start()
    keyboard_thread = threading.Thread(target=keyboard_run)
    keyboard_thread.start()
    
    try:
        while True:
            if app_on:
                # Wait for the event to be set (signal received)
                signal_event.wait(timeout=ALERT_TIME_SECONDS)
                last_signal_time = seconds_since_last_time()  
                #            print("last signal time = " + str(last_signal_time))
                if last_signal_time > ALERT_TIME_SECONDS:
                    if not signal_sent:
                        # send email here
                        print("Signal Sent")
                        greenled(True)
                        redled(False)
                        signal_sent = True
                    else:
                        signal_sent = False
                        greenled(False)
                        redled(True)
                
                        # return the signal to the thread
                        signal_event.clear()
            else:
                greenled(False)
                redled(False)
                sleep(1)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("Exiting...")
        # Wait for the motion detection thread to finish
        run_motion_thread=False
        motion_detection_thread.join()
        keyboard_thread.join()  
        #pir.close()
    finally:
        blue_LED.off() 
        greenled(False)
        redled(False)

def parse_args():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Motion Alarm')
    # Add the '--fg' argument
    parser.add_argument('--fg', action='store_true', help='Run in the foreground')

    args = parser.parse_args()
    # Access the values of the arguments
    run_in_foreground = args.fg

def run():
    parse_args()
    daemon = daemonize.Daemonize(
        app='motion',
        pid='/run/alarmbox.pid',
        action=run_motion,
        foreground=run_in_foreground,
    )
    # Start the daemon)
    daemon.start()


def sigterm_handler(signum, frame):
    global run_motion_thread
    # HandleSIGTERM (signal 15) here
    print("Received SIGTERM, performing cleanup...")
    blue_LED.off()
    greenled(False)
    redled(False)
    # Add your cleanup code here
    run_motion_thread=False
    print("thread join return")
    PIR_sensor.close()
    print("sensore close")
    sys.exit(0)

if __name__ == '__main__':
    # Set up the signal handler for SIGTERM
    signal.signal(signal.SIGTERM, sigterm_handler)
    run()
