# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "2.2.3"

from ..logging import DEBUG, INFO
from ..logging import Logger as _Logger


class Logger(_Logger):
    def get_format_params(self, *, msg, **params):
        from . import _router

        indent = "  " * len(_router.navigation_context.contexts)
        msg = msg.replace("\n", "\n" + " " * len(f"{indent}{self.name}: "))
        return super().get_format_params(indent=indent, msg=msg, **params)

    def __setattr__(self, attr: str, value) -> None:
        if attr == "debug":  # backwards compatability
            return _Logger.__setattr__(self, "level", DEBUG if value else INFO)
        return _Logger.__setattr__(self, attr, value)


logger = Logger("#routing", format="{indent}{name}: {msg}", level=INFO)
