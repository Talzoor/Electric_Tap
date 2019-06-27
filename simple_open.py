
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime

PIN_A = 17
PIN_B = 22
PIN_C = 27


def time_stamp():
    return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')


GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN_A, GPIO.OUT)
GPIO.setup(PIN_B, GPIO.OUT)
GPIO.setup(PIN_C, GPIO.OUT)
GPIO.output(PIN_A, GPIO.LOW)
GPIO.output(PIN_B, GPIO.LOW)
GPIO.output(PIN_C, GPIO.LOW)

try:
    print("Started! {}".format(time_stamp()))
    print("Opening 17 and 22")

    GPIO.output(PIN_A, GPIO.HIGH)
    GPIO.output(PIN_B, GPIO.HIGH)
    sleep(6*60)                 # 6min
finally:
    print("Closing {}".format(time_stamp()))
    GPIO.output(PIN_A, GPIO.LOW)
    GPIO.output(PIN_B, GPIO.LOW)
    sleep(1)
    GPIO.setup(PIN_A, GPIO.IN)
    GPIO.setup(PIN_B, GPIO.IN)

    GPIO.cleanup()



