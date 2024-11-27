# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from .logging import INFO
from .logging import Logger as _Logger

__version__ = "3.0.0"


_null_logger = _Logger()
_null_logger.disabled = True


class Message:
    def __init__(self, title, content=None):
        self.title = title
        self.content = content


class Subscriber:
    def __init__(self, subscriber, handler):
        self.subscriber = subscriber
        self.handler = handler


class Publisher:
    default_log_level = INFO

    def __init__(self, *, logger: _Logger = None):
        self.logger = logger or _null_logger
        self.subscribers = {}

    def publish(self, channel, title, content=None):
        message = Message(title, content)
        subscribers = self.subscribers.get(channel, [])
        for subscriber in subscribers:
            subscriber.handler(message)
        self.logger.log(
            self.default_log_level,
            f"Published '{message.title}' message on '{channel}' channel to "
            f"{len(subscribers)} subscriber(s)",
        )

    def subscribe(self, channel, subscriber, handler):
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(Subscriber(subscriber, handler))
        self.logger.log(
            self.default_log_level, f"Added subscriber to {channel} channel"
        )

    def unsubscribe(self, channel, subscriber):
        if channel in self.subscribers:
            self.subscribers[channel] = [
                s for s in self.subscribers[channel] if s.subscriber != subscriber
            ]
        self.logger.log(
            self.default_log_level, f"Removed subscriber from {channel} channel"
        )

    def close_channel(self, channel):
        subscribers_count = len(self.subscribers[channel])
        del self.subscribers[channel]
        self.logger.log(
            self.default_log_level,
            f"{channel} closed ({subscribers_count} subscribers)",
        )
