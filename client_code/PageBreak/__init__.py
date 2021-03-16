# MIT License
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software is published at https://github.com/anvilistas/anvil-extras
#
# Based on the snippet at
# https://anvil.works/forum/t/plots-in-pdf-being-divided-between-two-pages/7774/5
from .. import session
from ._anvil_designer import PageBreakTemplate

__version__ = "1.0.0"

css = """
<style>
  .break-container {
    border: 1px solid grey;
  }
  @media print {
    .break-container {
      border: none;
    }
  }
</style>
"""
session.style_injector.inject(css)


class PageBreak(PageBreakTemplate):
    def __init__(self, margin_top, **properties):
        self.html = f"""
<div class="break-container" style="overflow: hidden;">
  <div style="page-break-after:always;"/>
  <div style="margin-top: {margin_top};"/>
</div>
"""
        self.init_components(**properties)
