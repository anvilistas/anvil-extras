# MIT License
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "1.0.0"


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
