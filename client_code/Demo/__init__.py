from ._anvil_designer import DemoTemplate
from anvil import *

class Demo(DemoTemplate):
  def __init__(self, **properties):
    self.progress = 0
    self.init_components(**properties)


  def timer_1_tick(self, **event_args):
      if self.progress < 100:
          self.progress_bar.progress = self.progress
          self.progress += 0.01