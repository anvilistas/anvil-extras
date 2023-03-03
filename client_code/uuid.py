# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil.js
from anvil.js import window as _W

from utils._deprecated import deprecated

__version__ = "2.2.3"

try:
    _js_uuid = _W.uuid
    _v4, _parse, _validate = _js_uuid.v4, _js_uuid.parse, _js_uuid.validate
except AttributeError:
    _js_uuid = anvil.js.import_from("https://jspm.dev/uuid@8.3.2")
    _v4, _parse, _validate = _js_uuid.v4, _js_uuid.parse, _js_uuid.validate


class UUID(str):
    def __init__(self, val):
        if not _validate(val):
            raise ValueError("badly formed hexadecimal UUID string")

    def __repr__(self):
        return "UUID('" + self + "')"

    @property
    def bytes(self):
        return _parse(self)


@deprecated(
    "anvil_extras.uuid.uuid4() should be replaced with uuid.uuid4() and will be removed in a future version"
)
def uuid4():
    """returns a uuid"""
    return UUID(_v4())


if __name__ == "__main__":
    x = uuid4()
    print(repr(x))
    print(x)
    print(x.bytes)
    try:
        UUID("foo")
    except ValueError as e:
        print(f"Succesfully raised - {e!r}")
    else:
        print("Value Error Not Raised")
