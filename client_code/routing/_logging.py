class Logger:
    def __init__(self, debug, msg=""):
        self.debug = debug
        self.msg = msg
        self._log = [(msg,)]

    def print(self, *args, **kwargs):
        if self.debug:
            print(self.msg, *args, **kwargs) if self.msg else print(*args, **kwargs)
        self._log.append(args)

    def show_log(self):
        log_rows = [" ".join(str(arg) for arg in args) for args in self._log]
        return "\n".join(log_rows)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"debug should be a boolean, not {type(value).__name__}")
        self._debug = value

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        if not isinstance(value, str):
            raise TypeError(f"msg should be type str, not {type(value).__name__}")
        self._msg = value


logger = Logger(debug=False, msg="#routing:")
# set to false if you don't wish to debug. You can also - in your main form - do routing.logger.debug = False
