
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime

def time_stamp():
    return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.output(6, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(19, GPIO.LOW)

try:
    print("Started! {}".format(time_stamp()))
    print("Opening 6 and 13")

    GPIO.output(6, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    sleep(1000)
finally:
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    sleep(1)
    GPIO.cleanup


