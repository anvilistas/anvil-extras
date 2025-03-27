# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil_extras import ProgressBar
from anvil_extras.utils._component_helpers import _html_injector

from ._anvil_designer import IndeterminateTemplate

__version__ = "3.1.0"

_html_injector.css(ProgressBar.css)


class Indeterminate(ProgressBar.Mixin, IndeterminateTemplate):
    def __init__(self, **properties):
        ProgressBar.Mixin.__init__(self, **properties)
        self.init_components(**properties)
