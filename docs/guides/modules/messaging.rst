Messaging
=========

Introduction
------------
This library provides a mechanism for forms (and other components) within an Anvil app
to communicate in a 'fire and forget' manner.

It's an alternative to raising and handling events - instead you 'publish' messages to
a channel and, from anywhere else, you subscribe to that channel and process those
messages as required.


Usage
-----

Create the Publisher
++++++++++++++++++++
You will need to create an instance of the Publisher class somewhere in your application
that is loaded at startup.

For example, you might create a client module at the top level of your app called 'common'
with the following content:

.. code-block:: python

    from anvil_extras.messaging import Publisher

    publisher = Publisher()

and then import that module in your app's startup module/form.

Publish Messages
++++++++++++++++
From anywhere in your app, you can import the publisher and publish messages to a channel.
e.g. Let's create a simple form that publishes a 'hello world' message when it's initiated:


.. code-block:: python

    from ._anvil_designer import MyPublishingFormTemplate
    from .common import publisher


    class MyPublishingForm(MyPublishingFormTemplate):

        def __init__(self, **properties):
            publisher.publish(channel="general", title="Hello world")
            self.init_components(**properties)

The publish method also has an optional 'content' parameter which can be passed any object.

Subscribe to a Channel
++++++++++++++++++++++
Also, from anywhere in your app, you can subscribe to a channel on the publisher by
providing a handler function to process the incoming messages.

The handler will be passed a Message object, which has the title and content of the
message as attributes.

e.g. On a separate form, let's subscribe to the 'general' channel and print any 'Hello
world' messages:


.. code-block:: python

    from ._anvil_designer import MySubscribingFormTemplate
    from .common import publisher


    class MySubscribingForm(MySubscribingFormTemplate):

        def __init__(self, **properties):
            publisher.subscribe(
                channel="general", subscriber=self, handler=self.general_messages_handler
            )
            self.init_components(**properties)

        def general_messages_handler(self, message):
            if message.title == "Hello world":
                print(message.title)

You can unsubscribe from a channel using the publisher's `unsubscribe` method.

You can also remove an entire channel using the publisher's `close_channel` method.

Be sure to do one of these if you remove instances
of a form as the publisher will hold references to those instances and the handlers will
continue to be called.

Logging
+++++++
The publisher can log each message it receieves to your app's logs (and
the output pane if you're in the IDE) using a `Logger` instance.

You can do this by passing a `Logger` instance when you first create a Publisher:

.. code-block:: python

    from anvil_extras.messaging import Publisher
    from anvil_extras.logging import Logger, INFO
    publisher = Publisher(
        logger=Logger(name="publisher", level=INFO, format="{datetime:%Y-%m-%d %H:%M:%S}: {msg}")
    )

The `publish`, `subscribe`, `unsubscribe` and `close_channel` methods will each use the
`logger` informed at creation.

By default, if no logger is informed, no messages will be logged. Also, messages will be logged at INFO level by default.
To change this behavior globally you can do the following:

.. code-block:: python

    from anvil_extras.messaging import Publisher
    from anvil_extras.logging import Logger, ERROR

    # The following line sets the default logger to be used for every new published instance created after it's set
    Publisher.default_logger = Logger(name="publisher", level=INFO, format="{datetime:%Y-%m-%d %H:%M:%S}: {msg}")
    # The following line sets the overrides the default log level (INFO) to ERROR for all publishers that have a logger.
    Publisher.default_log_level = ERROR

For more information, check the Logging page in the docs.
