# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import sys
from datetime import date, datetime

__version__ = "1.9.0"

DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4

_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Logger:
    def __init__(
        self,
        name="root",
        level=INFO,
        format="{name}: {level}: {msg}",
        stream=sys.__stdout__,
    ):
        stream, level, format = self._validate(stream, level, format)
        self.name = name
        self.stream = stream
        self.level = level
        self.format = format

    def __setattr__(self, attr: str, value) -> None:
        upper = attr.upper()
        if upper not in _levels:
            return object.__setattr__(self, attr, value)
        level = _levels.index(upper)
        object.__setattr__(self, "level", level if value else level + 1)

    def _validate(self, stream, level, format):
        if not (hasattr(stream, "write") and hasattr(stream, "flush")):
            raise TypeError(
                "stream must be None or have a .write() and .flush() method"
            )

        if level in _levels:
            level = _levels.index(level)
        elif level not in (0, 1, 2, 3, 4):
            raise TypeError(
                "Level should be one of logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR or logging.CRITICAL"
            )

        if not isinstance(format, str):
            raise TypeError("the format must be a string")

        return stream, level, format

    def _write(self, msg):
        self.stream.write(msg + "\n")
        self.stream.flush()

    def log(self, level, msg):
        """log a message at a given level"""
        if level < self.level:
            return
        now = datetime.now()
        out = self.format.format(
            name=self.name,
            time=now.time(),
            datetime=now,
            date=now.date(),
            level=_levels[level],
            msg=msg,
        )
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

    def critical(self, msg):
        """always outputs a message"""
        self.log(WARNING, msg)

    def print(self, msg, level=DEBUG):
        """like logger.log but the default level is set to logging.DEBUG"""
        self.log(level, msg)
