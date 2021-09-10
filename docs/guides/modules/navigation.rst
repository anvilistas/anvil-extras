Navigation
==========
A client module for that provides dynamic menu construction.

Introduction
------------
This module builds a menu of link objects based on a simple dictionary definition.

Rather than manually adding links and their associated click event handlers, the module does that for you!

Usage
-----

Forms
+++++

In order for a form to act as a target of a menu link, it has to register a name with the navigation module using a decorator
on its class definition. e.g. Assuming the module is installed as a dependency named 'Extras':

.. code-block:: python

    from ._anvil_designer import HomeTemplate
    from anvil import *
    from anvil_extras import navigation


    @navigation.register(name="home")
    class Home(HomeTemplate):
      def __init__(self, **properties):
        self.init_components(**properties)

Menu
++++
* In the Main form for your app, add a content panel to the menu on the left hand side and call it 'menu_panel'

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
        self.advanced_mode = False
        navigation.build_menu(self.menu_panel, menu)
        self.init_components(**properties)

will add 'Home' and 'About' links to the menu which will open registered forms named 'home' and 'about' respectively.

Each item in the dict needs the 'text' and 'target' keys as a minimum. It may also include 'full_width', 'routing' and 'visibility' keys:

 * 'full_width' can be True or False to indicate whether the target form should be opened with 'full_width_row' or not.
 * 'routing' can be either 'classic' or 'hash' to indicate whether clicking the link should use Anvil's `add_component` function or hash routing to open the target form. Classic routing is the default if the key is not present in the menu dict.
 * 'visibility' can be a dict mapping an anvil event to either True or False to indicate whether the link should be made visible when that event is raised.

 All other keys in the menu dict are passed to the Link constructor.

 For example, to add icons to each of the examples above, a 'Contact' item that uses hash routing and a 'Settings' item that should only be visible when advanced mode is enabled:

.. code-block:: python

    from ._anvil_designer import MainTemplate
    from anvil import *
    from anvil_extras import navigation
    from HashRouting import routing

    menu = [
      {"text": "Home", "target": "home", "icon": "fa:home"},
      {"text": "About", "routing": "hash", "target": "about", "icon": "fa:info"},
      {"text": "Contact", "routing": "hash", "target": "contact", "icon": "fa:envelope"},
      {
        "text": "Settings",
        "target": "settings",
        "icon": "fa:gear",
        "visibility": {
          "x-advanced-mode-enabled": True,
          "x-advanced-mode-disabled": False
        }
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

Note - since this example includes hash routing, it also requires a decorator from the `Hash Routing App <https://github.com/s-cork/HashRouting>`_ on the Main class.

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
By default, the menu builder will also add a Label to the title slot of your Main form. If you register a form with a title as well as a name, the module will update that label as you navigate around your app. e.g. to add a title to the home page example:

.. code-block:: python

    from ._anvil_designer import HomeTemplate
    from anvil import *
    from anvil_extras import navigation


    @navigation.register(name="home", title="Home")
    class Home(HomeTemplate):
      def __init__(self, **properties):
        self.init_components(**properties)

If you want to disable this feature, set the `with_title` argument to `False` when you call `build_menu` in your Main form. e.g.

.. code-block:: python

    class Main(MainTemplate):

      def __init__(self, **properties):
        self.advanced_mode = False
        navigation.build_menu(self.menu_column_panel, menu, with_title=False)
        self.init_components(**properties)

Navigate with Code
++++++++++++++++++
You can emulate clicking a menu link using the go_to function, which takes a 'target' key as its only parameter, e.g.

.. code-block:: python

    navigation.go_to("contact")
