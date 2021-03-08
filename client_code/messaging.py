# MIT License 
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/meatballs/anvil-extras/graphs/contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software is published at https://github.com/meatballs/anvil-extras
__version__ = "0.1.9"


class Message:
    def __init__(self, title, content=None):
        self.title = title
        self.content = content


class Subscriber:
    def __init__(self, subscriber, handler):
        self.subscriber = subscriber
        self.handler = handler


class Publisher:
    def __init__(self, with_logging=True):
        self.with_logging = with_logging
        self.subscribers = {}

    def publish(self, channel, title, content=None, with_logging=None):
        if with_logging is None:
            with_logging = self.with_logging
        message = Message(title, content)
        subscribers = self.subscribers.get(channel, [])
        for subscriber in subscribers:
            subscriber.handler(message)
        if with_logging:
            print(
                f"Published '{message.title}' message on '{channel}' channel to "
                f"{len(subscribers)} subscriber(s)"
            )

    def subscribe(self, channel, subscriber, handler, with_logging=None):
        if with_logging is None:
            with_logging = self.with_logging
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(Subscriber(subscriber, handler))
        if with_logging:
            print(f"Added subscriber to {channel} channel")

    def unsubscribe(self, channel, subscriber, with_logging=None):
        if with_logging is None:
            with_logging = self.with_logging
        if channel in self.subscribers:
            self.subscribers[channel] = [
                s for s in self.subscribers[channel] if s.subscriber == subscriber
            ]
        if with_logging:
            print(f"Removed subscriber from {channel} channel")

    def close_channel(self, channel, with_logging=None):
        if with_logging is None:
            with_logging = self.with_logging
        subscribers_count = len(self.subscribers[channel])
        del self.subscribers[channel]
        if with_logging:
            print(f"{channel} closed ({subscribers_count} subscribers)")
