# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from logging import Logger
__version__ = "3.0.0"


class Message:
    def __init__(self, title, content=None):
        self.title = title
        self.content = content


class Subscriber:
    def __init__(self, subscriber, handler):
        self.subscriber = subscriber
        self.handler = handler


class Publisher:
    def __init__(self, with_logging=True, log_level="INFO"):
        self.with_logging = with_logging
        self.subscribers = {}
        self.log_level = log_level

    def publish(self, channel, title, content=None, with_logging=None, log_level=None):
        if with_logging is None:
            with_logging = self.with_logging
        if log_level is None:
            log_level = self.log_level
        message = Message(title, content)
        subscribers = self.subscribers.get(channel, [])
        for subscriber in subscribers:
            subscriber.handler(message)
        if with_logging:
            if isinstance(with_logging, Logger):
                with_logging.log(
                    log_level,
                    f"Published '{message.title}' message on '{channel}' channel to "
                    f"{len(subscribers)} subscriber(s)"
                )
            else:
                print(
                    f"Published '{message.title}' message on '{channel}' channel to "
                    f"{len(subscribers)} subscriber(s)"
                )

    def subscribe(self, channel, subscriber, handler, with_logging=None, log_level=None):
        if with_logging is None:
            with_logging = self.with_logging
        if log_level is None:
            log_level = self.log_level
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(Subscriber(subscriber, handler))
        if with_logging:
            if isinstance(with_logging, Logger):
                with_logging.log(log_level, f"Added subscriber to {channel} channel")
            else:
                print(f"Added subscriber to {channel} channel")

    def unsubscribe(self, channel, subscriber, with_logging=None, log_level=None):
        if with_logging is None:
            with_logging = self.with_logging
        if log_level is None:
            log_level = self.log_level
        if channel in self.subscribers:
            self.subscribers[channel] = [
                s for s in self.subscribers[channel] if s.subscriber != subscriber
            ]
        if with_logging:
            if isinstance(with_logging, Logger):
                with_logging.log(log_level, f"Removed subscriber from {channel} channel")
            else:
                print(f"Removed subscriber from {channel} channel")

    def close_channel(self, channel, with_logging=None, log_level=None):
        if with_logging is None:
            with_logging = self.with_logging
        if log_level is None:
            log_level = self.log_level
        subscribers_count = len(self.subscribers[channel])
        del self.subscribers[channel]
        if with_logging:
            if isinstance(with_logging, Logger):
                with_logging.log(log_level, f"{channel} closed ({subscribers_count} subscribers)")
            else:
                print(f"{channel} closed ({subscribers_count} subscribers)")
