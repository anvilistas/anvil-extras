# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas

__version__ = "2.2.2"


def err_to_obj(message):
    if type(message) is str:
        return {"message": message}
    return message or {"message": ""}
