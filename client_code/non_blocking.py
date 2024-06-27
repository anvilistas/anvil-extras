# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import partial as _partial

from anvil.js import report_exceptions as _report
from anvil.js import window as _W
from anvil.server import call_s as _call_s

__version__ = "2.6.2"

try:
    # just for a nice repr by default
    _call_s.__name__ = "call_s"
    _call_s.__qualname__ = "anvil.server.call_s"
except AttributeError:
    pass

# python errors get wrapped when called from a js function in python
# so instead reject the error from a js function in js
_deferred = _W.Function(
    "fn",
    """
const deferred = { status: "PENDING", error: null };

deferred.promise = new Promise(async (resolve, reject) => {
    try {
        resolve(await fn());
        deferred.status = "FULFILLED";
    } catch (e) {
        deferred.status = "REJECTED";
        deferred.error = e;
        reject(e);
    }
});

let handledResult = deferred.promise;
let handledError = null;

return Object.assign(deferred, {
    on_result(resultHandler, errorHandler) {
        if (!errorHandler && handledError) {
            // the on_error was already called so provide a dummy handler;
            errorHandler = () => {};
        }
        handledResult = deferred.promise.then(resultHandler, errorHandler);
        handledError = null;
    },
    on_error(errorHandler) {
        handledError = handledResult.catch(errorHandler);
        handledResult = deferred.promise;
    },
    await_result: async () => await deferred.promise,
});
""",
)


class _Result:
    # dicts may come back as javascript object literals
    # so wrap the results in a more opaque python object
    def __init__(self, value):
        self.value = value

    @staticmethod
    def wrap(fn):
        def wrapper():
            return _Result(fn())

        return wrapper

    @staticmethod
    def unwrap(fn):
        def unwrapper(res):
            return fn(res.value)

        return unwrapper


class _AsyncCall:
    def __init__(self, fn, *args, **kws):
        self._fn = _partial(fn, *args, **kws)
        self._deferred = _deferred(_Result.wrap(self._fn))

    def _check_pending(self):
        if self._deferred.status == "PENDING":
            raise RuntimeError("the async call is still pending")

    @property
    def result(self):
        """If the function call is not complete, raises a RuntimeError
        If the function call is complete:
        Returns: the return value from the function call
        Raises: the error raised by the function call
        """
        self._check_pending()
        return self.await_result()

    @property
    def error(self):
        """Returns the error raised by the function call, else None"""
        self._check_pending()
        return self._deferred.error

    @property
    def status(self):
        """Returns: 'PENDING', 'FULFILLED', 'REJECTED'"""
        return self._deferred.status

    @property
    def promise(self):
        """Returns: JavaScript Promise that resolves to the value from the function call"""
        return _W.Promise(
            lambda resolve, reject: resolve(
                self._deferred.promise.then(lambda r: r.value, reject)
            )
        )

    def on_result(self, result_handler, error_handler=None):
        error_handler = error_handler and _report(error_handler)
        result_handler = _Result.unwrap(_report(result_handler))
        self._deferred.on_result(result_handler, error_handler)
        return self

    def on_error(self, error_handler):
        self._deferred.on_error(_report(error_handler))
        return self

    def await_result(self):
        return self._deferred.await_result().value

    def __repr__(self):
        fn_repr = repr(self._fn).replace("functools.partial", "")
        return f"<non_blocking.AsyncCall{fn_repr}>"


def call_async(fn_or_name, *args, **kws):
    """
    Call a function or a server function (if a string is provided) in a non-blocking way.

    Parameters
    ----------
    fn_or_name: A function or the name of a server function to call.
    """
    if isinstance(fn_or_name, str):
        return _AsyncCall(_call_s, fn_or_name, *args, **kws)
    if callable(fn_or_name):
        return _AsyncCall(fn_or_name, *args, **kws)
    msg = "the first argument must be a callable or the name of a server function"
    raise TypeError(msg)


def wait_for(async_call_object):
    "Wait for a non-blocking function to complete its execution"
    if not isinstance(async_call_object, _AsyncCall):
        raise TypeError(
            f"expected an AsyncCall object, got {type(async_call_object).__name__}"
        )
    return async_call_object.await_result()


class _AbstractTimerRef:
    def _clear(self, id):
        raise NotImplementedError("implemented by subclasses")

    def __init__(self, id):
        self._id = id

    def cancel(self):
        self._clear(self._id)


class _DeferRef(_AbstractTimerRef):
    _clear = _W.clearTimeout


class _RepeatRef(_AbstractTimerRef):
    _clear = _W.clearInterval


def cancel(ref):
    """Cancel an active call to delay or defer
    Parameters
    ----------
    ref: should be None, or the return value from calling delay/defer

    e.g.
    >>> ref = defer(fn, 1)
    >>> cancel(ref)
    """
    if ref is None:
        return
    if not isinstance(ref, _AbstractTimerRef):
        msg = "Invalid argumnet to cancel(), expected None or the return value from calling delay/defer"
        raise TypeError(msg)
    return ref.cancel()


def defer(fn, delay):
    """Defer a function call after a set period of time has elapsed (in seconds)

    Parameters
    ----------
    fn : a callable that takes no args
    delay : int | float
        the time delay in seconds to wait before calling fn

    Returns
    -------
    DeferRef
        a reference to the deferred call that can be cancelled
        either with ref.cancel() or non_blocking.cancel(ref)
    """
    return _DeferRef(_W.setTimeout(fn, delay * 1000))


def repeat(fn, interval):
    """Repeatedly call a function with a set interval (in seconds)

    Parameters
    ----------
    fn : a callable that takes no args
    interval : int | float
        the time between calls to fn

    Returns
    -------
    RepeatRef
        a reference to the repeated call that can be cancelled
        either with ref.cancel() or non_blocking.cancel(ref)
    """
    return _RepeatRef(_W.setInterval(fn, interval * 1000))


if __name__ == "__main__":
    # TESTS
    from time import sleep as _sleep

    _v = 0

    def _f():
        global _x, _v
        _v += 1
        if _v >= 5:
            cancel(_x)

    print("Testing repeat")
    _x = repeat(_f, 0.01)
    _x.cancel()
    assert _v == 0
    _x = repeat(_f, 0.01)
    _sleep(0.1)
    assert _v == 5
    _x = repeat(_f, 0.01)
    assert _v == 5
    _sleep(0.1)
    assert _v == 6

    print("Testing defer")
    _v = 0
    _x = defer(_f, delay=0.05)
    _sleep(0.01)
    cancel(_x)
    _x = defer(_f, delay=0.05)
    _sleep(0.1)
    assert _v == 1

    print("Testing Async Call")
    _x = call_async(lambda v: v + 1, 42)
    assert _x.status == "PENDING"
    try:
        _x.result
    except RuntimeError:
        pass
    else:
        assert False
    _v = _x.await_result()
    assert _x.status == "FULFILLED"
    assert _x.result == 43
    assert _x.error is None
    _v = None

    def _f(v):
        global _v
        _v = v

    _x.on_result(_f)
    assert _v is None
    _sleep(0)
    assert _v == 43
    _v = None
    _x = call_async(lambda v: v + 1, "foo")
    _x.on_result(_f)
    _x.on_error(_f)
    _sleep(0)
    assert _x.status == "REJECTED"
    assert isinstance(_v, TypeError)
    assert _v is _x.error
    try:
        _x.result
    except TypeError:
        pass
    else:
        assert False
    _v = call_async(lambda: {}).await_result()
    assert type(_v) is dict
    print("PASSED")
