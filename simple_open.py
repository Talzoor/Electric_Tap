#!/usr/bin/python3


import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import configparser
import os
from pathlib import Path

PIN_A = 17
PIN_B_COM = 22
PIN_C = 27
PIN_LED = 18

Config = configparser.ConfigParser()


class ConfigSectionMap:
    def __init__(self, _exception=None):
        self.exception = _exception

    def get(self, section):
        dict1 = {}

        script_dir = os.path.dirname(os.path.realpath(__file__))  # script dir
        file_name = 'Settings.ino'

        data_folder = Path(script_dir)
        setting_file = "{}/{}".format(data_folder, file_name)
        # print("Setting file:{}".format(setting_file))

        try:
            with open(setting_file) as f:
                Config.read_file(f)

                if Config.has_section(section):
                    options = Config.options(section)
                    for option in options:
                        try:
                            dict1[option] = Config.get(section, option)
                            if dict1[option] == -1:
                                pass
                        except:
                            print("exception on %s!" % option)
                            dict1[option] = None
                else:   # there is no such option
                    # print("Config file error!")
                    self.exception.error("Config file error! ({})".format(section))
                    dict1 = {}
        except FileNotFoundError:
            self.exception.error("Config file error! (FileNotFoundError), ({})".format(section))
        return dict1


def time_stamp():
    return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')


def take_digits_only(_str):
    start = -1
    end = len(_str)
    int_to_return = ""
    for i, chr in enumerate(_str):
        if chr.isdigit() or chr == '.':
            if start == -1: start = i
        else:
            if start == -1:
                continue
            else:
                end = i
                break
    if not start == -1:
        int_to_return = float(_str[start:end])
    return int_to_return


def main():
    DEFAULT_TIME = 6
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PIN_A, GPIO.OUT)
    GPIO.setup(PIN_B_COM, GPIO.OUT)
    GPIO.setup(PIN_C, GPIO.OUT)
    GPIO.output(PIN_A, GPIO.LOW)
    GPIO.output(PIN_B_COM, GPIO.LOW)
    GPIO.output(PIN_C, GPIO.LOW)

    GPIO.setup(PIN_LED, GPIO.OUT)


    try:
        print("{}Started!".format(time_stamp()))

        ConfigVals = ConfigSectionMap()
        time_to_run_dict = ConfigVals.get("Timing")
        if time_to_run_dict == {}:
            time_to_run = DEFAULT_TIME         # default of 6 min
        else:
            time_to_run = time_to_run_dict["run time"]
            time_to_run = take_digits_only(time_to_run)

        # print("time_to_run:{}".format(time_to_run))
        if (type(time_to_run) is int or type(time_to_run) is float) and time_to_run > 0:
            pass
        else:
            time_to_run = DEFAULT_TIME

        print("Opening 17 and 22 for {} min".format(time_to_run))

        GPIO.output(PIN_B_COM, GPIO.HIGH)
        GPIO.output(PIN_A, GPIO.HIGH)
        sleep(time_to_run * 60)                 # Xmin
    finally:
        print("{}Closing\n".format(time_stamp()))
        GPIO.output(PIN_B_COM, GPIO.LOW)
        GPIO.output(PIN_A, GPIO.LOW)
        sleep(1)
        GPIO.setup(PIN_B_COM, GPIO.IN)
        GPIO.setup(PIN_A, GPIO.IN)

        GPIO.cleanup()


if __name__ == '__main__':
    main()


