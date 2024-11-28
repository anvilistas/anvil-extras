# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "3.1.0"


def err_to_obj(message):
    if type(message) is str:
        return {"message": message}
    return message or {"message": ""}
