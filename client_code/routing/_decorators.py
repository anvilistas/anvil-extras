# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from collections import namedtuple
from functools import wraps

from anvil.js.window import setTimeout

from . import _router

__version__ = "2.0.1"

route_info = namedtuple(
    "route_info", ["form", "url_pattern", "url_keys", "title", "fwr", "url_parts"]
)
template_info = namedtuple("template_info", ["form", "path", "condition"])


def template(path="", priority=0, condition=None):
    if not isinstance(path, str):
        raise TypeError("the first argument to template must be a str")
    if not isinstance(priority, int):
        raise TypeError("the template priority must be an int")
    if condition is not None and not callable(condition):
        raise TypeError("the condition must be None or a callable")

    def template_wrapper(cls):
        info = template_info(cls, path, condition)
        _router.add_template_info(cls, priority, info)

        cls_init = cls.__init__

        @wraps(cls_init)
        def init_and_route(self, *args, **kws):
            try:
                _router._ready = False
                cls_init(self, *args, **kws)
                setTimeout(_router.launch)
                # use set timeout so that if called with open_form
                # then the main_router is the open form before we try to navigate

            finally:
                _router.ready = True

        cls.__init__ = init_and_route

        return cls

    return template_wrapper


class route:
    """
    the route decorator above any form you want to load in the content_panel
    @routing.route(url_pattern=str,url_keys=List[str], title=str)
    """

    def __init__(self, url_pattern="", url_keys=[], title=None, full_width_row=False):
        self.url_pattern = url_pattern
        self.url_keys = url_keys
        self.title = title
        self.fwr = full_width_row
        self.url_parts = []

    def as_dynamic_var(self, part):
        if len(part) > 1 and part[0] == "{" and part[-1] == "}":
            return part[1:-1], True
        return part, False

    def validate_args(self, cls):
        if not isinstance(self.url_pattern, str):
            raise TypeError(
                f"url_pattern must be type str not {type(self.url_pattern)} in {cls.__name__}"
            )
        if not (isinstance(self.url_keys, list) or isinstance(self.url_keys, tuple)):
            raise TypeError(
                f"keys should be a list or tuple not {type(self.url_keys)} in {cls.__name__}"
            )
        if not (self.title is None or isinstance(self.title, str)):
            raise TypeError(
                f"title must be type str or None not {type(self.title)} in {cls.__name__}"
            )
        if self.url_pattern.endswith("/"):
            self.url_pattern = self.url_pattern[:-1]
        self.url_keys = frozenset(self.url_keys)
        self.url_parts = [
            self.as_dynamic_var(part) for part in self.url_pattern.split("/")
        ]

    def __call__(self, cls):
        self.validate_args(cls)
        info = route_info(form=cls, **self.__dict__)
        _router.add_route_info(info)
        return cls


def error_form(cls):
    """optional decorator - this is the error form simply use the decorator above your error Form
    @routing.error_form
    """
    cls._route_props = {"title": None, "layout_props": {}}
    _router._error_form = cls
    return cls
