from anvil.js.window import jQuery as _S
from anvil.js.window import location

__version__ = "1.0.0"

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
