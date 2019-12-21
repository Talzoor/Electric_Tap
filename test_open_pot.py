#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime

PIN_A = 17      # flowerpot
PIN_B_COM = 22  # common
PIN_C = 27      # flowerbed
PIN_LED = 18


def GPIO_def():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PIN_A, GPIO.OUT)
    GPIO.setup(PIN_B_COM, GPIO.OUT)
    GPIO.setup(PIN_C, GPIO.OUT)
    GPIO.output(PIN_A, GPIO.LOW)
    GPIO.output(PIN_B_COM, GPIO.LOW)
    GPIO.output(PIN_C, GPIO.LOW)

    GPIO.setup(PIN_LED, GPIO.OUT)


def time_stamp():
    return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')


def main():

    GPIO_def()
    try:
        print("{}Started!".format(time_stamp()))

        time_to_run_pot = 15            #15 min

        open_valve(PIN_B_COM, PIN_A, time_to_run_pot)

    finally:
        print("{}Closing\n".format(time_stamp()))
        GPIO.output(PIN_A, GPIO.LOW)
        GPIO.output(PIN_B_COM, GPIO.LOW)
        sleep(1)
        GPIO.setup(PIN_A, GPIO.IN)
        GPIO.setup(PIN_B_COM, GPIO.IN)

        GPIO.cleanup()


def open_valve(_pinA, _pinB, _open_time):
    print("Opening {} and {} for {} {}".format(_pinA, _pinB,
                                               _open_time if _open_time >= 1 else  _open_time*60 ,
                                               "min" if _open_time >= 1 else "sec"))
    GPIO.output(_pinA, GPIO.HIGH)
    GPIO.output(_pinB, GPIO.HIGH)
    sleep(_open_time * 60)
    GPIO.output(_pinA, GPIO.LOW)
    GPIO.output(_pinB, GPIO.LOW)


if __name__ == '__main__':
    main()