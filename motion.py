#!/usr/bin/python
import daemonize
import os
from gpiozero import LED
from gpiozero import MotionSensor
from time import sleep
from threading import Thread
import threading
from datetime import datetime, timedelta
import argparse

ALERT_TIME_SECONDS = 10
green_led = LED(18)
PIR_sensor = MotionSensor(4)
# initialize last_time to 1 minute before the program starts
signal_event = threading.Event()
run_in_foreground = True

def seconds_since_last_time():
    global last_time
    now = datetime.now()
    diff_time = now - last_time
    seconds = diff_time.total_seconds()
    return int(seconds)

def motion_detected():
    global last_time
    last_time = datetime.now()
    print("Motion Detected!")
    signal_event.set()

def motion_thread():
    while True:
        PIR_sensor.wait_for_motion()
        motion_detected()


# next lines define the variables with their input
# GPIO pin numbers and type of input they are
def run_motion():
    global last_time
    last_time = datetime.now() - timedelta(60)
    signal_sent = False
    # Spin off a thread for the IR sensor
    motion_detection_thread = Thread(target=motion_thread)
    motion_detection_thread.start()

    try:
        while True:
            # Wait for the event to be set (signal received)
            signal_event.wait(timeout=ALERT_TIME_SECONDS)
            last_signal_time = seconds_since_last_time()  
            print("last signal time = " + str(last_signal_time))
            if last_signal_time > ALERT_TIME_SECONDS:
                if not signal_sent:
                    # send email here
                    print("Signal Sent")
                    green_led.on()
                    signal_sent = True
            else:
                signal_sent = False
                green_led.off()
                print("Turning off LED")
                
            # return the signal to the thread
            signal_event.clear()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("Exiting...")
        # Wait for the motion detection thread to finish
        motion_detection_thread.join()  
        #pir.close() 

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
        app='alarmbbox',
        pid='/tmp/alarmbox.pid',
        action=run_motion,
        foreground=run_in_foreground,
    )
    # Start the daemon)
    daemon.start()
    
if __name__ == '__main__':
    run()
