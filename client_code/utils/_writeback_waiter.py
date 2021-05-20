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

from functools import cache, wraps

from anvil.js.window import Function, anvilFormTemplates

__version__ = "1.1.0"

_store_writebacks = Function(
    "form",
    """
    const self = PyDefUtils.unwrapOrRemapToPy(form);
    const bindings = self._anvil.dataBindings || [];
    const activeWritebacks = bindings.map(() => null);

    bindings.forEach(({pyComponent}, i) => {
        const bindingFunc = pyComponent._anvil.dataBindingWriteback;
        const wrapper = (component, name, val) => {
            const res = bindingFunc(component, name, val).finally(() => {
                activeWritebacks[i] = null;
            });
            activeWritebacks[i] = res;
            return res;
        };
        pyComponent._anvil.dataBindingWriteback = wrapper;
    });

    self._anvil.activeWritebacks = activeWritebacks;
""",
)

_wait_for_writeback = Function(
    "form",
    """
    const self = PyDefUtils.unwrapOrRemapToPy(form);
    return new Promise((resolve) => {
        setTimeout(() => resolve(Promise.allSettled(self._anvil.activeWritebacks.slice(0))));
    }).then(() => Sk.builtin.none.none$);
""",
)


def _init_wrapper(init):
    @wraps(init)
    def wrapper(self, *args, **kwargs):
        _store_writebacks(self)
        return init(self, *args, **kwargs)

    return wrapper


@cache
def _init_writeback(template):
    template.init_components = template.__init__ = _init_wrapper(template.__init__)


for template in anvilFormTemplates:
    _init_writeback(template)


def wait_for_writeback(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        _wait_for_writeback(self)
        return fn(self, *args, **kwargs)

    return wrapper
