# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from .logging import INFO
from .logging import Logger as _Logger
from .utils._warnings import warn as _warn

__version__ = "3.1.0"


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

    def __init__(self, *, logger: _Logger = None, **kwargs):
        self.logger = logger or _null_logger
        self.subscribers = {}
        self._deprecation_warnings(**kwargs)

    def _deprecation_warnings(self, **kwargs):
        if "with_logging" in kwargs:
            _warn(
                "publisher.with_logging",
                "with_logging option is deprecated and it will be removed in future versions. Use the logger options instead, passing an instance of logging.Logger",
                "DEPRECATION WARNING",
            )

    def publish(self, channel, title, content=None, **kwargs):
        self._deprecation_warnings(**kwargs)
        message = Message(title, content)
        subscribers = self.subscribers.get(channel, [])
        for subscriber in subscribers:
            subscriber.handler(message)
        self.logger.log(
            self.default_log_level,
            f"Published '{message.title}' message on '{channel}' channel to "
            f"{len(subscribers)} subscriber(s)",
        )

    def subscribe(self, channel, subscriber, handler, **kwargs):
        self._deprecation_warnings(**kwargs)
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(Subscriber(subscriber, handler))
        self.logger.log(
            self.default_log_level, f"Added subscriber to {channel} channel"
        )

    def unsubscribe(self, channel, subscriber, **kwargs):
        self._deprecation_warnings(**kwargs)
        if channel in self.subscribers:
            self.subscribers[channel] = [
                s for s in self.subscribers[channel] if s.subscriber != subscriber
            ]
        self.logger.log(
            self.default_log_level, f"Removed subscriber from {channel} channel"
        )

    def close_channel(self, channel, **kwargs):
        self._deprecation_warnings(**kwargs)
        subscribers_count = len(self.subscribers[channel])
        del self.subscribers[channel]
        self.logger.log(
            self.default_log_level,
            f"{channel} closed ({subscribers_count} subscribers)",
        )
