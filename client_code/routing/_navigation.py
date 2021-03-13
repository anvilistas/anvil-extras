from anvil.js.window import document, window, history, location
from time import sleep
from anvil import get_open_form
from ._logging import logger

# re-initialise the state object which was overridden on load or this is a new session
state = history.state or {"url": location.hash, "pos": 0}
history.replaceState(state, "", state["url"])

# undo and pos are used for unload behavior
current = {"undo": 0, "pos": state["pos"]}


# when the window back or forward button is pressed onPopState is triggered
# a popstate is also triggered from a change in the URL in this case the window.history.state will be None
def onPopState(e):
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

    main_form = get_open_form()
    on_navigation = getattr(main_form, "on_navigation", None)
    if on_navigation is not None:
        on_navigation()
    else:
        logger.print("the open form is not using '@main_router' or has no 'on_navigation' method")


window.onpopstate = onPopState


def pushState(url):
    # set_in_history = True, replace_current_url=False
    current["pos"] += 1
    current["undo"] = -1
    state = {"url": url, "pos": current["pos"]}
    history.pushState(state, "", url)


def replaceState(url):
    # set_in_history=True, replace_current_url=True
    current["undo"] = 0
    state = {"url": url, "pos": history.state["pos"]}
    history.replaceState(state, "", url)


def replaceUrlNotState(url):
    # set_in_history=False, replace_current_url=True
    current["undo"] = 0
    history.replaceState(history.state, "", url)


#### some helpers #####
defaultTitle = document.title


def setTitle(title):
    document.title = defaultTitle if title is None else title


def reloadPage():
    location.reload()


def goBack():
    window.history.back()


def goTo(x):
    window.history.go(x)


def getUrlHash():
    return location.hash[1:]  # without the hash


############ App unload behaviour ############

# app unload behavior
def onBeforeUnload(e):
    e.preventDefault()  # cancel the event
    e.returnValue = ""  # chrome requires a returnValue to be set


def stopUnload():
    window.onpopstate = None
    history.go(current["undo"])
    sleep(0.1)  # allow go to fire
    window.onpopstate = onPopState
    current["pos"] = history.state["pos"]


def setAppUnloadBehaviour(warning):
    window.onbeforeunload = onBeforeUnload if warning else None


def setUnloadPopStateBehaviour(flag):
    # at this point we're waiting for the unload function to complete
    # so we bind to the unloadPopStateTemp which prevents any forward back navigation
    window.onpopstate = unloadPopStateTemp if flag else onPopState


# Form Unload Behaviour - here we prevent the user from navigating away from the current form
# while we wait for the unload function to complete
def unloadPopStateTemp(e):
    e.preventDefault()
    state = e.state
    if state:
        temp_undo = current["pos"] - state["pos"]
        window.onpopstate = None  # unbind onpopstate
        history.go(temp_undo)  # reverse the navigation
        sleep(0.1)  # allow go to fire before rebinding onpopstate
        window.onpopstate = unloadPopStateTemp

    else:
        # the user is determined to navigate away and has changed the url manually so let them!
        # Not letting them will break the app...
        current["pos"] += 1
        state = {"url": location.hash, "pos": current["pos"]}
        history.replaceState(state, "")
        window.onbeforeunload = None
        location.reload()
