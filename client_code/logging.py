# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import sys
from datetime import datetime as _datetime
from functools import wraps
from time import time as _time

__version__ = "2.2.3"

NOTSET = 0
DEBUG = 1
INFO = 2
WARNING = 3
ERROR = 4
CRITICAL = 5

_level_to_name = {
    NOTSET: "NOTSET",
    DEBUG: "DEBUG",
    INFO: "INFO",
    WARNING: "WARNING",
    ERROR: "ERROR",
    CRITICAL: "CRITICAL",
}


def _get_level_name(level):
    return _level_to_name.get(level) or f"Level {level}"


class Logger:
    def __init__(
        self,
        name="root",
        level=NOTSET,
        format="{name}: {level}: {msg}",
        stream=None,
    ):
        self._validate(level, format, stream)
        self.name = name
        self.stream = stream or sys.stdout
        self.level = level
        self.format = format
        self.disabled = False

    def _validate(self, level, format, stream):
        if level not in _level_to_name:
            raise TypeError("level should be a valid logging level e.g. logging.DEBUG")
        if not isinstance(format, str):
            raise TypeError("format must be a string")
        if stream is not None and not (
            hasattr(stream, "write") and hasattr(stream, "flush")
        ):
            raise TypeError("a valid stream must have a .write() and .flush() method")

    def _write(self, msg):
        self.stream.write(msg + "\n")
        self.stream.flush()

    def get_format_params(self, *, level, msg, **params):
        now = _datetime.now()
        return {
            "name": self.name,
            "time": now.time(),
            "datetime": now,
            "level": _get_level_name(level),
            "msg": msg,
            **params,
        }

    def log(self, level, msg):
        """log a message at a given level"""
        if level < self.level or self.disabled:
            return
        params = self.get_format_params(level=level, msg=msg)
        out = self.format.format(**params)
        self._write(out)

    def debug(self, msg):
        """outputs the msg only if the level is set to logging.DEBUG"""
        self.log(DEBUG, msg)

    def info(self, msg):
        """outputs the msg only if the level is set to logging.INFO or logging.DEBUG"""
        self.log(INFO, msg)

    def warning(self, msg):
        """outputs the msg only if the level is set to logging.INFO, logging.DEBUG or logging.WARNING"""
        self.log(WARNING, msg)

    def error(self, msg):
        """outputs the msg only if the level is set to logging.ERROR or below"""
        self.log(ERROR, msg)

    def critical(self, msg):
        """always outputs a message"""
        self.log(WARNING, msg)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} {self.name!r} ({_get_level_name(self.level)})>"
        )


class TimerLogger(Logger):
    def __init__(
        self,
        name="timer_logger",
        level=NOTSET,
        format="{time:%H:%M:%S} | {name}: ({elapsed:6.3f} secs) | {msg}",
        stream=None,
    ):
        Logger.__init__(self, name=name, level=level, format=format, stream=stream)
        self._t = None

    def get_format_params(self, **params):
        if self._t is None:
            raise RuntimeError(f"{self} has not started, or has ended already")
        elapsed = _time() - self._t
        return Logger.get_format_params(self, elapsed=elapsed, **params)

    def start(self, msg="start"):
        if self._t is not None:
            raise RuntimeError(
                f"{self} was already started - call .end() before starting again."
            )
        self._t = _time()
        self.debug(msg)

    def check(self, msg="check", restart=False):
        if not restart:
            self.debug(msg)
        else:
            self.debug(msg + " (restart)")
            self._t = _time()

    def end(self, msg="end"):
        self.debug(msg)
        self._t = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc):
        self.end()

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kws):
            with self:
                return fn(*args, **kws)

        return wrapper
