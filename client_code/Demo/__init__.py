from anvil import *

from ._anvil_designer import DemoTemplate


class Demo(DemoTemplate):
    def __init__(self, **properties):
        self.progress = 0
        self.init_components(**properties)

    def timer_1_tick(self, **event_args):
        if self.progress < 1:
            self.progress_bar.progress = self.progress
            self.progress += 0.01
