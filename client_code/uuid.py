# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.js.window import Function as _F

__version__ = "1.3.1"

from time import time

js_uuid4, js_uuid_parse = _F(
    """
return new Promise(resolve => {
    window.anvilExtrasResolve = resolve;
    const s = document.createElement('script');
    s.type = "module";
    s.textContent = `
        import { v4, parse } from 'https://jspm.dev/uuid@8.3.2';
        window.anvilExtrasResolve([v4, parse]);
    `
    document.body.appendChild(s);
  });
"""
)()


class UUID(str):
    def __repr__(self):
        return "UUID('" + self + "')"

    @property
    def bytes(self):
        return js_uuid_parse(self)


def uuid4():
    """returns a uuid"""
    return UUID(js_uuid4())
