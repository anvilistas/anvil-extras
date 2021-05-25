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

__version__ = "1.2.0"


from anvil.js.window import jQuery as _S
from anvil.js.window import location

modal = _S("#session-expired-modal")
modal_button = _S("#session-expired-modal .modal-footer button")
modal_close = _S("#session-expired-modal .modal-header button")


def trigger_refresh(e):
    modal.off("click")
    modal_button.trigger("click")


def reload_page(e):
    location.reload()


def session_expired_handler(reload_hash, allow_cancel):
    if reload_hash:
        modal_button.removeClass("refresh").off("click").on("click", reload_page)
    else:
        modal_button.addClass("refresh").off("click")

    if not allow_cancel:
        modal_button.css("display", "none")
        modal_close.css("display", "none")
        modal.off("click", trigger_refresh).on("click", trigger_refresh)
    else:
        modal_close.removeAttr("style")
        modal_button.removeAttr("style")
        modal.off("click", trigger_refresh)
