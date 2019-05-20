
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.output(6, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(19, GPIO.LOW)

try:
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    sleep(1000)
finally:
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)

