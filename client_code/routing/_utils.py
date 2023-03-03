# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from collections import namedtuple

import anvil
from anvil.js.window import location

from ._logging import logger

__version__ = "2.2.3"


ANY = object()


def get_url_components(url_hash=None):
    """returns  url_hash, url_pattern, url_dict
    this will get the components from the current addressbar url_hash unless you provide a url_hash to decode
    """
    if url_hash is None:
        # url_hash = anvil.get_url_hash()  #changed since anvil decodes the url_hash
        url_hash = location.hash[1:]  # without the hash
    elif isinstance(url_hash, str):
        url_hash = url_hash if not url_hash.startswith("#") else url_hash[1:]

    if isinstance(url_hash, dict):
        # this is the case when anvil converts the url hash to a dict automatically
        url_pattern = ""
        url_dict = {
            k: (anvil.http.url_decode(v) if v != "undefined" else "")
            for k, v in url_hash.items()
        }  # anvil.get_url_hash return 'undefined' for empty parameters
        url_hash = "?" + "&".join(
            f"{key}={anvil.http.url_encode(value)}" for key, value in url_dict.items()
        )
    elif "?" not in url_hash:  # then we have no parameters as part of the url
        url_pattern = url_hash
        url_dict = {}
    else:
        url_pattern, url_dict = url_hash.split("?", 1)
        key_value_pairs = url_dict.split("&")
        for i, pair in enumerate(key_value_pairs):
            if "=" not in pair:
                logger.debug(
                    f"\n\n**WARNING**:\ngot an unusual url parameter with no '=': {pair!r}"
                    f"\nIf this parameter split unexpectedly it probably contains '&'. Use:"
                    f"\nrouting.set_url_hash(url_pattern=url_pattern, url_dict=url_dict)"
                    f"\nFor correct encoding\n"
                )
                key_value_pairs[i] = pair = pair + "="
            key, value = pair.split("=", 1)
            key_value_pairs[i] = f"{key}={anvil.http.url_decode(value)}"
        url_dict = dict(pair.split("=", 1) for pair in key_value_pairs)

    return url_hash, url_pattern, url_dict


def get_url_hash(url_hash=None) -> str:
    """returns the current url_hash"""
    if url_hash is None:
        return location.hash[1:]
    return get_url_components(url_hash=url_hash)[0]


def get_url_pattern(url_hash=None) -> str:
    """returns the current url_dict unless a url_pattern is provided"""
    return get_url_components(url_hash=url_hash)[1]


def get_url_dict(url_hash=None) -> dict:
    """returns the current url_dict unless a url_hash is provided"""
    return get_url_components(url_hash=url_hash)[2]


def _process_url_arguments(url_hash=None, *, url_pattern=None, url_dict=None):
    """
    check and set_up the url_hash, url_pattern and url_dict
    """
    if url_dict is not None and url_pattern is None:
        raise TypeError(
            "if you provide a url_dict you must provide a url_pattern as a keyword argument url_pattern="
        )
    if url_hash is None and url_pattern is None:
        url_hash = ""  # default behaviour should be an empty string
    elif url_hash is None:
        url_dict = {} if url_dict is None else url_dict
        url_hash = _get_url_hash(url_pattern, url_dict)
    url_hash, url_pattern, url_dict = get_url_components(
        url_hash
    )  # will convert to a string
    return url_hash, url_pattern, url_dict


def _get_url_hash(url_pattern, url_dict):
    url_params = "&".join(
        f"{key}={anvil.http.url_encode(str(value))}" for key, value in url_dict.items()
    )
    url_params = "?" + url_params if url_params else ""
    return url_pattern + url_params


def _as_frozen_str_iterable(obj, attr, allow_none=False, factory=frozenset):
    if isinstance(obj, str) or (allow_none and obj is None) or obj is ANY:
        return factory([obj])
    rv = []
    for o in obj:
        if not isinstance(o, str) and o is not ANY:
            msg = f"expected an iterable of strings or a string for {attr} argument"
            raise TypeError(msg)
        rv.append(o)
    return factory(rv)


_RouteInfoBase = namedtuple(
    "route_info",
    ["form", "template", "url_pattern", "url_keys", "title", "fwr", "url_parts"],
)

TemplateInfo = namedtuple("template_info", ["form", "path", "condition"])
RedirectInfo = namedtuple("redirect_info", ["redirect", "path", "condition"])


class RouteInfo(_RouteInfoBase):
    @staticmethod
    def as_dynamic_var(part):
        if len(part) > 1 and part[0] == "{" and part[-1] == "}":
            return part[1:-1], True
        return part, False

    def __new__(cls, form, template, url_pattern, url_keys, title, fwr, url_parts=()):
        if url_pattern.endswith("/"):
            url_pattern = url_pattern[:-1]

        url_parts = tuple(cls.as_dynamic_var(part) for part in url_pattern.split("/"))

        return _RouteInfoBase.__new__(
            cls, form, template, url_pattern, url_keys, title, fwr, url_parts
        )
