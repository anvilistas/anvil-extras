# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "1.9.0"

from ..utils.logging import DEBUG, INFO
from ..utils.logging import Logger as _Logger


class Logger(_Logger):
    def __setattr__(self, attr: str, value) -> None:
        if attr == "debug":  # backwards compatability
            return _Logger.__setattr__(self, "level", DEBUG if value else INFO)
        return _Logger.__setattr__(self, attr, value)


logger = Logger("#routing", format="{name}: {msg}", level=INFO)
# set to false if you don't wish to debug. You can also - in your main form - do routing.logger.debug = False
_callable = type(lambda: None)


def log(f: _callable):
    if logger.level > DEBUG:
        return
    logger.debug(f())
