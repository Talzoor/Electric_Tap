class ColorPrint:
    def __init__(self, _log):
        self.log = _log
        self.fg = FgRegister()
        self.bg = BgRegister()
        self.rs = RsRegister()
        self.bool_bg = False
        self.color_code = 15        # default white

    def __call__(self, _str, **kwargs):
        try:
            if "color_code" in kwargs:
                self.color_code = kwargs["color_code"]
            if "bg" in kwargs:
                self.bool_bg = kwargs["bg"]
            func = self.bg if self.bool_bg else self.fg
        except:
            raise_exception(self.log, "ColorPrint __call__")
        return func(self.color_code) + _str + self.rs.all

    def color(self, _color_code, _bg=False):
        func = self.bg if self.bool_bg else self.fg
        print(func(_color_code))

    def reset(self):
        print(self.rs.all)