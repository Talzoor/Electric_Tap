#!/usr/bin/python3

try:
    import RPi.GPIO as GPIO
except ImportError:
    import fakeRPiGPIO as GPIO

from time import sleep
from datetime import datetime
import configparser
import os
from pathlib import Path
import argparse

PIN_A = 17      # flowerpot
PIN_B_COM = 22  # common
PIN_C = 27      # flowerbed
PIN_LED = 18

DEFAULT_TIME_BED = 6
DEFAULT_TIME_POT = 4

def argument_program():
    arg_parser = argparse.ArgumentParser(description='-p [N] will choose program number')
    arg_parser.add_argument('-p', action="store", dest="p", type=int)

    results = arg_parser.parse_args()
    if results.p is None:   # if no arg is passed so p=1
        results.p = 1
    return results.p


class ConfigSectionMap:
    def __init__(self, _exception=None):
        self.exception = _exception
        self.config = configparser.ConfigParser()

    def get(self, section):
        dict1 = {}

        script_dir = os.path.dirname(os.path.realpath(__file__))  # script dir
        file_name = 'Settings.ino'

        data_folder = Path(script_dir)
        setting_file = "{}/{}".format(data_folder, file_name)
        # print("Setting file:{}".format(setting_file))

        try:
            with open(setting_file) as f:
                self.config.read_file(f)

                if self.config.has_section(section):
                    options = self.config.options(section)
                    for option in options:
                        try:
                            dict1[option] = self.config.get(section, option)
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


def check_enabled(_dict):
    if _dict is {}:
        state_enable = True
    else:
        state_enable = _dict["enabled"]
        if state_enable.lower() in ['true', 'yes', 'y', '1']:
            state_enable = True
        else:
            state_enable = False
    return state_enable


def main():

    GPIO_def()
    try:
        program = argument_program()
        print("{}Started! - program {}".format(time_stamp(), program))
        ConfigVals = ConfigSectionMap()
        state_dict = ConfigVals.get("State")
        if check_enabled(state_dict):
            time_to_run_dict = ConfigVals.get("Program {}".format(program))
            if time_to_run_dict == {}:
                time_to_run_bed = DEFAULT_TIME_BED         # default of 6 min
                time_to_run_pot = DEFAULT_TIME_POT         # default of 4 min
            else:
                time_to_run_bed = time_to_run_dict["run time (flowerbed)"]
                time_to_run_bed = take_digits_only(time_to_run_bed)
                time_to_run_pot = time_to_run_dict["run time (flowerpot)"]
                time_to_run_pot = take_digits_only(time_to_run_pot)

            time_to_run_bed = check_time_to_run_bed(time_to_run_bed)
            time_to_run_pot = check_time_to_run_pot(time_to_run_pot)

            open_valve(PIN_B_COM, PIN_C, time_to_run_bed)
            open_valve(PIN_B_COM, PIN_A, time_to_run_pot)
        else:
            print("{}not Enabled - Check 'Settings.ino'\n".format(time_stamp()))

    finally:
        print("{}Closing\n".format(time_stamp()))
        GPIO.output(PIN_A, GPIO.LOW)
        GPIO.output(PIN_B_COM, GPIO.LOW)
        GPIO.output(PIN_C, GPIO.LOW)
        sleep(1)
        GPIO.setup(PIN_A, GPIO.IN)
        GPIO.setup(PIN_B_COM, GPIO.IN)
        GPIO.setup(PIN_C, GPIO.IN)

        GPIO.cleanup()


def check_time_to_run_bed(_time_to_run_bed):
    if (type(_time_to_run_bed) is int or type(_time_to_run_bed) is float) and _time_to_run_bed > 0:
        time_to_run_bed = _time_to_run_bed
    else:
        time_to_run_bed = DEFAULT_TIME_BED
    return time_to_run_bed


def check_time_to_run_pot(_time_to_run_pot):
    if (type(_time_to_run_pot) is int or type(_time_to_run_pot) is float) and _time_to_run_pot > 0:
        time_to_run_pot = _time_to_run_pot
    else:
        time_to_run_pot = DEFAULT_TIME_POT
    return time_to_run_pot


def open_valve(_pinA, _pinB, _open_time):
    print("Opening {} and {} for {:.2f} {}".format(_pinA, _pinB,
                                                  _open_time if _open_time >= 1 else _open_time*60,
                                                  "min" if _open_time >= 1 else "sec"))
    GPIO.output(_pinA, GPIO.HIGH)
    GPIO.output(_pinB, GPIO.HIGH)
    sleep(_open_time * 60)
    GPIO.output(_pinA, GPIO.LOW)
    GPIO.output(_pinB, GPIO.LOW)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("{}Quit! (KeyboardInterrupt) - Bye.\n".format(time_stamp()))
        exit(1)







