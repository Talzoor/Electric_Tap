class Solenoid:
    import time as time_lib

    def __init__(self, _log, _pin, _no, _color_print):
        self.pin = _pin
        self.start_time = 0
        self.no = _no
        self.log = _log
        self.ColorPrint = _color_print

    def open(self):
        self.start_time = self.unix_time()
        solenoid_change(self.log, self.no)

    def close(self):
        self.start_time = 0

    def state(self):
        _tmp_state = not GPIO.input(self.pin)
        return _tmp_state

    def time_open(self):
        _tmp_time = self.unix_time()
        _time_open = _tmp_time - self.start_time
        return self.state() and _time_open or -1

    def restart(self):
        self.solenoid_change(self.log, self.no)
        self.time_lib.sleep(ms(50))
        self.solenoid_change(self.log, 0)

    def solenoid_change(self, _log, _int_tap_number):
        # global SOLENOID_OPEN
        print_color = self.ColorPrint(log)
        to_close = []
        to_open = []
        try:
            if _int_tap_number == 1:
                to_close = [PIN_TAP_2, ]
                to_open = [PIN_TAP_1, ]
                self.log.info(print_color("OPENING tap 1", color_code=34) +
                         "(pin {})".format([PIN_TAP_1]))

            if _int_tap_number == 2:
                to_close = [PIN_TAP_1, ]
                to_open = [PIN_TAP_2, ]
                self.log.info(print_color("CLOSING tap 1", color_code=160) +
                         " (pin {}), ".format([PIN_TAP_1]) +
                         print_color("OPENING 2", color_code=34) +
                         " (pin {})".format([PIN_TAP_2]))

            if _int_tap_number == 0:
                to_close = [PIN_TAP_1, PIN_TAP_2]
                to_open = [0, ]
                self.log.info(print_color("CLOSING taps 1 and 2", color_code=160) +
                         " (pins {},{})".format([PIN_TAP_1], [PIN_TAP_2]))

            for tap_to_close in to_close:
                if not tap_to_close == 0:
                    GPIO.output(tap_to_close, True)  # close

            self.time_lib.sleep(ms(200))

            for tap_to_open in to_open:
                if not tap_to_open == 0:
                    GPIO.output(tap_to_open, False)  # open

            # SOLENOID_OPEN = _int_tap_number

        except:
            raise_exception(self.log, "open_solenoid({})".format(_int_tap_number))

    def unix_time(self):
        return int(round(self.time_lib.time()))