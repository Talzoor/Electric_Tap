
class RaiseException:
    import sys
    import linecache

    def __init__(self, log, _str_func, ColorPrint, _GPIO):
        self.print_color = ColorPrint(log)
        self.log = log
        self.str_func = _str_func
        self.GPIO = _GPIO

    def raise_excp(self):
        exc_type, exc_obj, tb = self.sys.exc_info()
        frm = tb.tb_frame
        lineno = tb.tb_lineno
        filename = frm.f_code.co_filename
        self.linecache.checkcache(filename)
        line = self.linecache.getline(filename, lineno, frm.f_globals)

        self.print_color.color(196)
        self.log.critical("\n\nfucn '{}' error: \n{}, {} \nline:{}- {}"
                     .format(self.str_func, exc_type, exc_obj, lineno, line))
        self.print_color.reset()

        if exc_type == KeyboardInterrupt:
            raise KeyboardInterrupt
        self.close(self.log, 99)

    def close(self, log, _code=None):
        log.debug("Cleaning GPIOs")
        self.GPIO.cleanup()
        log.info(self.print_color("Bye.", color_code=69))
        exit(_code is None and 0 or _code)
