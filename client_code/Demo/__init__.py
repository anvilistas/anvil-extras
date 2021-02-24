from ._anvil_designer import DemoTemplate
from anvil import *

class Demo(DemoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.