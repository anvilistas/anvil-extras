Navigation
==========
A client module for that provides dynamic menu construction.

Introduction
------------
This module builds a menu of link objects based on a simple dictionary definition.

Rather than manually adding links and their associated click event handlers, the module does that for you!


Mode
++++

There are two modes for the navigation module: ``"classic"`` and ``"hash"``.
If using ``"classic"`` mode, when a link is clicked, a Form registered with the navigation module is added to the ``content_panel`` element of the currently open form.
If using ``"hash"`` mode, when a link is clicked, navigation is taken care of using the routing module.


.. code-block:: python

    from anvil_extras import navigation

    navigation.set_mode("hash")
    navigation.set_mode("classic")


``"classic"`` mode is the default mode if no mode is set.


Menu
++++
* In the Main form for your app, add a ``ColumnPanel`` to the menu on the left hand side and call it ``"menu_panel"``

* Add a menu definition dict to the code for your Main form and pass the panel and the dict to the menu builder. e.g.

.. code-block:: python

    from ._anvil_designer import MainTemplate
    from anvil import *
    from anvil_extras import navigation
    from HashRouting import routing

    menu = [
      {"text": "Home", "target": "home"},
      {"text": "About", "target": "about"},
    ]


    class Main(MainTemplate):

      def __init__(self, **properties):
        navigation.build_menu(self.menu_panel, menu)
        self.init_components(**properties)

The above code will add 'Home' and 'About' links to the menu, which will open registered forms named with names ``"home"`` and ``"about"`` respectively.
If using ``"hash"`` mode, then the links will set the url hash to ``"home"`` and ``"about"``


Registered Forms
++++++++++++++++

In ``"classic"`` mode, in order for a form to act as a target of a menu link, it has to be registered with a unique name using the ``@navigation.register()`` decorator.

.. code-block:: python

    from ._anvil_designer import HomeTemplate
    from anvil_extras import navigation

    @navigation.register("home")
    class Home(HomeTemplate):
      def __init__(self, **properties):
        self.init_components(**properties)

Menu definition
+++++++++++++++

Each item in the dict needs the ``'text'`` and ``'target'`` keys as a minimum. It may also include ``'title'``, ``'full_width'`` and ``'visibility'`` keys:

 * 'full_width' can be True or False to indicate whether the target form should be opened with 'full_width_row' or not. (Only valid with ``"classic"`` mode - see routing documentation for ``full_width_row`` if using ``"hash"`` mode)
 * 'visibility' can be a dict mapping an anvil event to either True or False to indicate whether the link should be made visible when that event is raised.
 * 'title': optional, can be a string or None. Sets the page title.

 All other keys in the menu dict are passed to the Link constructor.

 For example, to add icons to each of the examples above, a 'Contact' item that uses hash routing and a 'Settings' item that should only be visible when advanced mode is enabled:

.. code-block:: python

    from ._anvil_designer import MainTemplate
    from anvil import *
    from anvil_extras import navigation
    from HashRouting import routing

    navigation.set_mode("hash")

    menu = [
      {"text": "Home", "target": "home", "icon": "fa:home", "title": "Home"},
      {"text": "About", "target": "about", "icon": "fa:info", "title": "About"},
      {"text": "Contact", "target": "contact", "icon": "fa:envelope", "title": "Contact"},
      {
        "text": "Settings",
        "target": "settings",
        "icon": "fa:gear",
        "visibility": {
          "x-advanced-mode-enabled": True,
          "x-advanced-mode-disabled": False
        },
        "title": "Settings"
      }
    ]


    @routing.main_router
    class Main(MainTemplate):

      def __init__(self, **properties):
        self.advanced_mode = False
        navigation.build_menu(self.menu_panel, menu)
        self.init_components(**properties)

      def form_show(self, **event_args):
        self.set_advanced_mode(False)


Startup
+++++++
In order for the registration to occur, the form classes need to be loaded before the menu is constructed. This can be achieved by using a startup module and importing each of the forms in the code for that module.

e.g. Create a module called 'startup', set it as the startup module and import your Home form before opening the Main form:

.. code-block:: python

   from anvil import open_form
   from .Main import Main
   from . import Home

   open_form(Main())


Page Titles
+++++++++++
By default, the menu builder will also add a Label to the title slot of your Main form.
Titles will be set based on the menu definition passed to ``build_menu``.

If you want to disable this feature, set the `with_title` argument to `False` when you call `build_menu` in your Main form. e.g.

.. code-block:: python

    class Main(MainTemplate):

      def __init__(self, **properties):
        navigation.build_menu(self.menu_column_panel, menu, with_title=False)
        self.init_components(**properties)

Navigate with Code
++++++++++++++++++
You can emulate clicking a menu link using the ``go_to`` function, which takes a ``'target'`` key as its only parameter, e.g.

.. code-block:: python

    navigation.go_to("contact")
