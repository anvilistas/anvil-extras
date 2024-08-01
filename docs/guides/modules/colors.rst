Colors
======
Define color schemes for your app and switch between them easily.

The module includes the definition of the anvil standard Material Design color schemes
and those are available within the `colors.M3_DEFAULT_SCHEMES` dictionary.

The dictionary keys are the names of the standard schemes - "Material", "Rally", "Mykonos"and "Manarola". The value for each key is a dictionary with two keys: "light" and "dark" and the value for each of these keys is a dictionary with the color names as keys and the color values as values.

Examples
--------
Create an instance of the `colors.Manager` class. By default, it uses the `M3_DEFAULT_SCHEMES` color schemes:

.. code-block:: python

    from anvil_extras import colors

    color_manager = colors.Manager()


Use that instance to set the color scheme of your app to either the 'light' or 'dark'
variant of one of the standard schemes:

.. code-block:: python

    color_manager.set_scheme("Material", "dark")

You can also define your own color schemes and use them in the same way. For a material
design scheme, follow the `Creating a custom Material Design 3 colour scheme <https://anvil.works/docs/how-to/creating-material-3-colour-scheme>`_ docs.

.. code-block:: python

   my_schemes = {
        scheme_one: {
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
        scheme_two: {
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

   color_manager = colors.Manager(my_schemes)
   color_manager.set_scheme("scheme_one", "light")
