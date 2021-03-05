import anvil.server
from ._anvil_designer import PageBreakTemplate

__version__ = "0.1.7"


class PageBreak(PageBreakTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
