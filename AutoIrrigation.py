try:
    import tendo.singleton as tendo_s
    Instance = tendo_s.SingleInstance()
except tendo_s.SingleInstanceException:
    print("Error - SingleInstanceException")
    exit(0)
    pass

try:
    from time import sleep
    import sys
    from datetime import datetime
    from datetime import timedelta
    import linecache

    sys_platform = sys.platform
    print("system platform: " + sys_platform)
    if "linux" in sys_platform.lower():
        import RPi.GPIO as GPIO
    else:
        from GPIOEmulator.EmulatorGUI import GPIO

    # from sty import ef, fg, bg, rs
    from sty.register import FgRegister, BgRegister, RsRegister

except ModuleNotFoundError:
    print("Error (AutoIrrigation.py) - ModuleNotFoundError")
    exit(0)
    pass

try:
    from tools.logger import Logger
except ImportError:
    from .tools.logger import Logger

try:
    from tools.email_script import SendEmail
except ImportError:
    from .tools.email_script import SendEmail

try:
    from tools.ColorPrint import ColorPrint
except ImportError:
    from .tools.ColorPrint import ColorPrint

try:
    from tools.Solenoid import Solenoid
except ImportError:
    from .tools.Solenoid import Solenoid

# noinspection PyPep8
PIN_TAP_1           = 2
PIN_TAP_2           = 3
PIN_TAP_3           = 4

LOG_NAME            = "AutoIrrigation.log"
LOG_FILE_W_PATH     = ""


def check_args(**kwargs):
    debug = [False, "float_on"]
    email = [True, 2, 8]    # [send, how many a day, first one on(24h)]

    if "debug" in kwargs:
        debug = kwargs["debug"]
    if "email" in kwargs:
        email = kwargs["email"]

    print("DEBUG:{}".format(debug))
    print("EMAIL_ALERTS:{}".format(email))

    sys.stdout.flush()
    return debug, email

def run(**kwargs):
    email_alerts, taps = check_args(**kwargs)
    log, tap_1, tap_2, flow_sensor, water_level, email_handle = setup(email_alerts)
    main(log, taps, tap_1, tap_2, flow_sensor, water_level, email_alerts, email_handle)

