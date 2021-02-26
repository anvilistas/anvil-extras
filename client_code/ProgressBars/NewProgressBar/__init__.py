from ._anvil_designer import NewProgressBarTemplate
class NewProgressBar(NewProgressBarTemplate):
    def __init__(self, progress, **properties):
        self.progress = progress
        self.init_components(**properties)
        
    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.refresh_data_bindings()
