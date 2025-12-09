# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil
from anvil.js import import_from
from anvil.js import window as _window

from ._component_helpers import _html_injector

__version__ = "3.6.1"

config = anvil.app.get_client_config("anvil_extras")
cdn = bool(config.get("cdn", True))

# Asset configuration specifying CSS, JS loading method, and access patterns
# CDN and local can have different types (e.g., CDN uses ESM, local uses window)
asset_config = {
    "quill": {
        "css": {
            "cdn": [
                "https://cdn.quilljs.com/1.3.6/quill.snow.css",
                "https://cdn.quilljs.com/1.3.6/quill.bubble.css",
            ],
            "local": [
                "_/theme/anvil-extras/cdn/quill.snow.css",
                "_/theme/anvil-extras/cdn/quill.bubble.css",
            ],
        },
        "js": {
            "cdn": {
                "type": "window",
                "url": "https://cdn.quilljs.com/1.3.6/quill.min.js",
            },
            "local": {
                "type": "window",
                "url": "_/theme/anvil-extras/cdn/quill.min.js",
            },
            "window_property": "Quill",
            "access": "window",
        },
    },
    "floating-ui": {
        "css": None,
        "js": {
            "cdn": {
                "type": "esm",
                "url": "https://cdn.jsdelivr.net/npm/@floating-ui/dom@1.7.4/+esm",
            },
            "local": {
                "type": "window",
                "url": "_/theme/anvil-extras/cdn/floating-ui.min.js",
                "dependencies": ["_/theme/anvil-extras/cdn/floating-ui.core.min.js"],
            },
            "window_property": "FloatingUIDOM",
            "access": "direct",  # For CDN ESM
        },
    },
    "nouislider": {
        "css": {
            "cdn": [
                "https://cdn.jsdelivr.net/npm/nouislider@15.4.0/dist/nouislider.min.css"
            ],
            "local": ["_/theme/anvil-extras/cdn/nouislider.min.css"],
        },
        "js": {
            "cdn": {
                "type": "esm",
                "url": "https://cdn.jsdelivr.net/npm/nouislider@15.4.0/+esm",
            },
            "local": {
                "type": "window",
                "url": "_/theme/anvil-extras/cdn/nouislider.min.js",
            },
            "window_property": "noUiSlider",
            "access": "default",  # For CDN ESM
        },
    },
    "localforage": {
        "css": None,
        "js": {
            "cdn": {
                "type": "esm",
                "url": "https://cdn.jsdelivr.net/npm/localforage@1.10.0/+esm",
            },
            "local": {
                "type": "window",
                "url": "_/theme/anvil-extras/cdn/localforage.min.js",
            },
            "window_property": "localforage",
            "access": "default",  # For CDN ESM
        },
    },
    "tanstack-virtual-core": {
        "css": None,
        "js": {
            "cdn": {
                "type": "esm",
                "url": "https://cdn.jsdelivr.net/npm/@tanstack/virtual-core@3.13.12/+esm",
            },
            "local": {
                "type": "esm",
                "url": "./_/theme/anvil-extras/cdn/tanstack-virtual-core.min.js",
            },
            "window_property": "tanstackvirtualCore",
            "access": "direct",
        },
    },
}


def _load_local_js(js_config):
    """Load JavaScript from local files using local configuration."""
    local_config = js_config["local"]
    js_type = local_config["type"]
    js_url = local_config["url"]

    # Load dependencies first (if any)
    if "dependencies" in local_config:
        for dep_url in local_config["dependencies"]:
            _html_injector.cdn(dep_url)

    if js_type == "window":
        # Load via script tag - puts on window
        _html_injector.cdn(js_url)
        window_prop = js_config["window_property"]
        return _window[window_prop]
    elif js_type in ("esm", "cjs"):
        # Load via import_from
        module = import_from(js_url)
        access = js_config.get("access", "direct")
        if access == "default":
            return module.default
        elif access == "direct":
            return module
        elif access == "window":
            window_prop = js_config["window_property"]
            return _window[window_prop]
        else:
            return module
    else:
        raise ValueError(f"Unknown local JS type: {js_type}")


def _load_cdn_js(js_config):
    """Load JavaScript from CDN using CDN configuration."""
    cdn_config = js_config["cdn"]
    js_type = cdn_config["type"]
    js_url = cdn_config["url"]

    if js_type == "window":
        # Load via script tag - puts on window
        _html_injector.cdn(js_url)
        window_prop = js_config["window_property"]
        return _window[window_prop]
    elif js_type in ("esm", "cjs"):
        # Load via import_from
        module = import_from(js_url)
        access = js_config.get("access", "direct")
        if access == "default":
            return module.default
        elif access == "direct":
            return module
        elif access == "window":
            window_prop = js_config["window_property"]
            return _window[window_prop]
        else:
            return module
    else:
        raise ValueError(f"Unknown CDN JS type: {js_type}")


def load_asset(asset_name):
    """
    Load an asset (CSS and JS) based on configuration.
    Returns the loaded JavaScript module/object.

    Args:
        asset_name: Name of the asset to load (e.g., "quill", "floating-ui")

    Returns:
        The loaded JavaScript module/object, accessed according to the asset's access pattern.
    """
    if asset_name not in asset_config:
        raise ValueError(f"Unknown asset: {asset_name}")

    config = asset_config[asset_name]
    js_config = config["js"]

    # Check if already loaded via window property (for assets that support it)
    if "window_property" in js_config:
        window_prop = js_config["window_property"]
        if window_prop in _window:
            return _window[window_prop]

    # Load CSS first (if any)
    if config["css"] is not None:
        css_urls = config["css"]["cdn"] if cdn else config["css"]["local"]

        if cdn:
            # Try CDN first, fall back to local if it fails
            try:
                for url in css_urls:
                    _html_injector.cdn(url)
            except Exception:
                # Fallback to local
                css_urls = config["css"]["local"]
                for url in css_urls:
                    _html_injector.cdn(url)
        else:
            # Use local directly
            for url in css_urls:
                _html_injector.cdn(url)

    # Load JavaScript
    if cdn:
        # Try CDN first, fall back to local if it fails
        try:
            return _load_cdn_js(js_config)
        except Exception:
            # Fallback to local (independent of CDN configuration)
            return _load_local_js(js_config)
    else:
        # Use local directly
        return _load_local_js(js_config)
