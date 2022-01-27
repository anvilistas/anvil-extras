# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "1.9.0"

from ._routing import (
    add_to_cache,
    clear_cache,
    error_form,
    get_cache,
    get_url_components,
    get_url_dict,
    get_url_hash,
    get_url_pattern,
    go,
    go_back,
    load_error_form,
    load_form,
    logger,
    main_router,
    on_session_expired,
    reload_page,
    remove_from_cache,
    route,
    set_url_hash,
    set_warning_before_app_unload,
)
