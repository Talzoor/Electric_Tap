
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime


def time_stamp():
    return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')


GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(27, GPIO.LOW)

try:
    print("Started! {}".format(time_stamp()))
    print("Opening 17 and 22")

    GPIO.output(17, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    sleep(4*60)                 # 4min
finally:
    print("Closing")
    GPIO.output(17, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    sleep(1)
    GPIO.cleanup


