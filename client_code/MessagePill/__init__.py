from ._anvil_designer import MessagePillTemplate


class MessagePill(MessagePillTemplate):
    backgrounds = dict(
        info="#bde5f8", success="#dff2bf", warning="#feefb3", error="#ffd2d2"
    )
    foregrounds = dict(
        info="#00529b", success="#4f8a10", warning="#9f6000", error="#d8000c"
    )
    icons = dict(
        info="fa:info-circle",
        success="fa:check",
        warning="fa:warning",
        error="fa:times-circle",
    )

    def __init__(self, **properties):
        self.init_components(**properties)

    @property
    def level(self):
        return self.item["level"]

    @level.setter
    def level(self, value):
        self.item["level"] = value
        self.label.background = self.backgrounds[value]
        self.label.foreground = self.foregrounds[value]
        self.label.icon = self.icons[value]

    @property
    def message(self):
        return self.item["message"]

    @message.setter
    def message(self, value):
        self.item["message"] = value
        self.label.text = value