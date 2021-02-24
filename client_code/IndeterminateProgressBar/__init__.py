from ._anvil_designer import IndeterminateProgressBarTemplate


class IndeterminateProgressBar(IndeterminateProgressBarTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    @property
    def track_colour(self):
        return self._track_colour

    @track_colour.setter
    def track_colour(self, value):
        self._track_colour = value
        self.call_js("setTrackColour", value)

    @property
    def indicator_colour(self):
        return self._indicator_colour

    @indicator_colour.setter
    def indicator_colour(self, value):
        self._indicator_colour = value
        self.call_js("setIndicatorColour", value)