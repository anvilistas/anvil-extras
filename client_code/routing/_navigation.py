# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import wraps

from anvil.js.window import history, location, window

from . import _router

__version__ = "2.2.3"

# re-initialise the state object which was overridden on load or this is a new session
state = history.state or {"url": location.hash, "pos": 0}
history.replaceState(state, "", state["url"])

# undo and pos are used for unload behavior
current = {"undo": 0, "pos": state["pos"]}

# Form Unload Behaviour - here we prevent the user from navigating away from the current form
# while we wait for the unload function to complete

undoing = False
waiting = False


# when the window back or forward button is pressed onPopState is triggered
# a popstate is also triggered from a change in the URL in this case the window.history.state will be None
def onPopState(e):
    global undoing, waiting
    if undoing:
        undoing = False
        current["pos"] = history.state["pos"]
        return
    elif waiting:
        return preventUnloadPopState(e)

    state = e.state
    if state:  # then we're loading from back forward navigation
        current["undo"] = current["pos"] - state["pos"]
        current["pos"] = state["pos"]
    else:
        current["undo"] = -1
        current["pos"] += 1
        state = {"url": location.hash, "pos": current["pos"]}

    history.replaceState(state, "", state["url"])
    # we always favour the state['url'] over location.hash
    # since we allow (replace_current_url=True, set_in_history=False)

    _router.navigate()


window.onpopstate = onPopState


def stopUnload():
    global undoing
    undoing = True
    history.go(current["undo"])


def preventUnloadPopState(e):
    global undoing
    e.preventDefault()
    state = e.state
    if state:
        undoing = True
        history.go(current["pos"] - state["pos"])  # reverse the navigation
    else:
        # the user is determined to navigate away and has changed the url manually so let them!
        # Not letting them will break the app...
        current["pos"] += 1
        state = {"url": location.hash, "pos": current["pos"]}
        history.replaceState(state, "")
        window.onbeforeunload = None
        location.reload()


class PreventUnloading:
    def __enter__(self):
        global waiting
        waiting = True

    def __exit__(self, *args):
        global waiting
        waiting = False


def ensure_hash(f):
    @wraps(f)
    def hash_wrapper(url):
        if not url.startswith("#"):
            url = "#" + url
        return f(url)

    return hash_wrapper


@ensure_hash
def pushState(url):
    # set_in_history = True, replace_current_url=False
    current["pos"] += 1
    current["undo"] = -1
    state = {"url": url, "pos": current["pos"]}
    history.pushState(state, "", url)


@ensure_hash
def replaceState(url):
    # set_in_history=True, replace_current_url=True
    current["undo"] = 0
    state = {"url": url, "pos": history.state["pos"]}
    history.replaceState(state, "", url)


@ensure_hash
def replaceUrlNotState(url):
    # set_in_history=False, replace_current_url=True
    current["undo"] = 0
    history.replaceState(history.state, "", url)
