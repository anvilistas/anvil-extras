# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import wraps

from . import _router
from ._utils import RouteInfo, TemplateInfo

__version__ = "2.0.1"


def template(path="", priority=0, condition=None, redirect=None):
    if not isinstance(path, str):
        raise TypeError("the first argument to template must be a str")
    if not isinstance(priority, int):
        raise TypeError("the template priority must be an int")
    if condition is not None and not callable(condition):
        raise TypeError("the condition must be None or a callable")
    if redirect is not None and not isinstance(redirect, str):
        raise TypeError("redirect must be set to a str")

    def template_wrapper(cls):
        info = TemplateInfo(cls, path, condition, redirect)
        _router.add_template_info(cls, priority, info)

        cls_init = cls.__init__

        def on_show(sender, **e):
            sender.remove_event_handler("show", on_show)
            # wait till the show event so that this template is the open_form before re-navigating
            _router.launch()

        @wraps(cls_init)
        def init_and_route(self, *args, **kws):
            _router._ready = False
            try:
                cls_init(self, *args, **kws)
                handlers = self.get_event_handlers("show")
                self.set_event_handler("show", on_show)
                # make us the first show event handler and re-add existing
                for handler in handlers:
                    self.add_event_handler("show", handler)
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

    def __init__(
        self,
        url_pattern="",
        url_keys=[],
        title=None,
        full_width_row=False,
        template=None,
    ):
        self.url_pattern = url_pattern
        self.url_keys = url_keys
        self.title = title
        self.fwr = full_width_row
        self.url_parts = []
        self.templates = template

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

    def __call__(self, cls):
        self.validate_args(cls)
        info = RouteInfo(form=cls, **self.__dict__)
        _router.add_route_info(info)
        return cls


def error_form(cls):
    """optional decorator - this is the error form simply use the decorator above your error Form
    @routing.error_form
    """
    cls._route_props = {"title": None, "layout_props": {}}
    _router._error_form = cls
    return cls
