Theme
=====
Define colour schemes for your app and switch between them easily.

The module includes the definition of the anvil standard Material Design colour schemes and those are used as the default. You can also define your own colour schemes and use them in the same way.

Examples
--------
Create an instance of the `theme.Colours` class:

.. code-block:: python

    from anvil_extras import theme

    colours = theme.Colours()

By default, that instance will have a `schemes` attribute that contains the standard Material Design colour schemes.

You can use the instance to set the colour scheme of your app to either the 'light' or 'dark' variant of one of those standard schemes.

When the object is instantiated, it will set the current scheme to the first defined scheme - 'Material' in this case - and the variant to the first defined within that scheme - 'dark' in this case.

You can change those defaults by passing arguments to the constructor. e.g. to set 'Manarola Dark' as the default scheme:

.. code-block:: python

    from anvil_extras import theme

    colours = theme.Colours(scheme="Manarola", variant="dark")


You can then use the your `Colours` instance to set the colour scheme or variant of your app at any time:

.. code-block:: python

   colours.scheme = "Mykonos"
   colours.variant = "light"

If your scheme has two variants, you can toggle between them:

.. code-block:: python

   colours.toggle()

If you want to set both the scheme and variant at the same time, you can use the `set_scheme` method:

.. code-block:: python

    colours.set_scheme("Material", "dark")

.. code-block:: python

    colours.set_scheme("Material", "dark")

You can define your own colour schemes and use them in the same way. For a material
design scheme, follow the `Creating a custom Material Design 3 colour scheme <https://anvil.works/docs/how-to/creating-material-3-colour-scheme>`_ docs.

.. code-block:: python

   my_schemes = {
        "scheme_one": {
            "light": {
                "primary": "#ff0000",
                "secondary": "#00ff00",
                "background": "#0000ff",
                "text": "#ffffff",
                "accent": "#ffff00",
                "disabled": "#888888",
                "divider": "#444444",
            },
            "dark": {
                "primary": "#ff0000",
                "secondary": "#00ff00",
                "background": "#0000ff",
                "text": "#ffffff",
                "accent": "#ffff00",
                "disabled": "#888888",
                "divider": "#444444",
            }
        },
        "scheme_two": {
            "light": {
                "primary": "#ff0000",
                "secondary": "#00ff00",
                "background": "#0000ff",
                "text": "#ffffff",
                "accent": "#ffff00",
                "disabled": "#888888",
                "divider": "#444444",
            },
            "dark": {
                "primary": "#ff0000",
                "secondary": "#00ff00",
                "background": "#0000ff",
                "text": "#ffffff",
                "accent": "#ffff00",
                "disabled": "#888888",
                "divider": "#444444",
            }
        }
   }

   colours = theme.Colours(schemes=my_schemes)
   colours.scheme = "scheme_two"
   colours.variant = "light"
