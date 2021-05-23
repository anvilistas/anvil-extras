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

from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S

__version__ = "1.1.0"

_loaded = False


def _onload(e):
    global _loaded
    _loaded = True


def _wait_for_load(interval=0.005):
    global _loaded
    while not _loaded:
        from time import sleep

        sleep(interval)
    _loaded = False


def _add_script(s):
    dummy = _S(s)[0]  # let jquery pass the tag
    s = _document.createElement(dummy.tagName)
    for attr in dummy.attributes:
        s.setAttribute(attr.name, attr.value)
    s.textContent = dummy.textContent
    _document.head.appendChild(s)
    if not s.get("src"):
        return
    s.onload = s.onerror = _onload  # ignore errors
    _wait_for_load()


def _spacing_property(a_b):
    def getter(self):
        return getattr(self, "_spacing_" + a_b)

    def setter(self, value):
        self._dom_node.classList.remove(
            f"anvil-spacing-{a_b}-{getattr(self, '_spacing_' + a_b, '')}"
        )
        self._dom_node.classList.add(f"anvil-spacing-{a_b}-{value}")
        setattr(self, "_spacing_" + a_b, value)

    return property(getter, setter, None, a_b)
