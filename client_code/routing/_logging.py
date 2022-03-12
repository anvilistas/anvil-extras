# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "1.9.0"

from ..utils._logging import Logger

logger = Logger("#routing", format="{name}: {msg}")
# set to false if you don't wish to debug. You can also - in your main form - do routing.logger.debug = False
_callable = type(lambda: None)


def log(f: _callable):
    if logger.level:
        return
    logger.print(f())
