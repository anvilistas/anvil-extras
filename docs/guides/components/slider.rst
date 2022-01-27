Slider
======
Slider component based on the Javascript library noUiSlider.

Properties
----------

:start: number | list[number]

    The initial values of the slider. This property determines the number of handles. It is a required property.
    In the designer use comma separated values which will be parsed as JSON.

:connect: "upper" | "lower" | bool | list[bool]

    The connect option can be used to control the bar color between the handles or the edges of the slider.
    When using one handle, set the value to either ``'lower'`` or ``'upper'`` (equivalently ``[True, False]`` or ``[False, True]``).
    For sliders with 2 or more handles, pass a list of True, False values. One value per gap. A single value of ``True`` will result in
    a coloured bar between all handles.


:min: number

    Lower bound. This is a required property

:max: number

    Upper bound. This is a required property

:range: object

    An object with ``'min'``, ``'max'`` as keys. For additional options see noUiSlider documentation. This does not need to be set and will be inferred from the ``min``, ``max`` values.

:step: number

    By default, the slider slides fluently. In order to make the handles jump between intervals, the step option can be used.

:format:

    Provide a format for the values. This can either be a string to call with .format or a format spec.
    e.g. ``"{:.2f}"`` or just ``".2f"``. See python''s format string syntax for more options.

    For a mapping of values to descriptions, e.g. ``{1: 'strongly disagree', 2: 'agree', ...}`` use a custom formatter.
    This is a dictionary object with ``'to'`` and ``'from'`` as keys and can be set at runtime.
    The ``'to'`` function takes a float or int and returns a str. The ``'from'`` takes a str and returns a float or int. See the anvil-extras Demo for an example.


:value: number

    returns the value of the first handle. This can only be set after initialization or with a databinding.

:values: list[numbers]

    returns a list of numerical values. One value for each handle. This can only be set after initialization or with a databinding.

:formatted_value: str

    returns the value of the first handle as a formatted string, based on the format property

:formatted_values: list[str]

    returns the a list of values as formatted strings, based on the format property

:padding: number | list[number, number]

    Padding limits how close to the slider edges handles can be. Either a single number for both edges.
    Or a list of two numbers, one for each edge.

:margin: number

    When using two handles, the minimum distance between the handles can be set using the margin option. The
    margin value is relative to the value set in ``range``.


:limit: number

    The limit option is the opposite of the margin option, limiting the maximum distance between two handles


:animate: bool

    Set the animate option to False to prevent the slider from animating to a new value with when setting values in code.


:behaviour: str

    This option accepts a ``"-"`` separated list of ``"drag"``, ``"tap"``, ``"fixed"``, ``"snap"``, ``"unconstrained"`` or ``"none"``

:tooltips: bool

    Adds tooltips to the sliders. Uses the same formatting as the format property.


:pips: bool

    Sets whether the slider has pips (ticks).

:pips_mode: str

    One of ``'range'``, ``'steps'``, ``'positions'``, ``'count'``, ``'values'``

:pips_values: list[number]

    a list of values. Interpreted differently depending on the mode

:pips_density: int

    Controls how many pips are placed. With the default value of 1, there is one pip per percent.
    For a value of 2, a pip is placed for every 2 percent. A value of zero will place
    more than one pip per percentage. A value of -1 will remove all intermediate pips.

:pips_stepped: bool

    the stepped option can be set to true to match the pips to the slider steps

:color: str

    The color of the bars. Can be set to theme colors like ``'theme:Primary 500'`` or hex values ``'#2196F3'``.

:color: str

    The color of the bars. Can be set to theme colors like ``'theme:Primary 500'`` or hex values ``'#2196F3'``.

:bar_height: str | int

    The height of the bar. Can be a css length or an integer, which will be set to the pixel height. Defaults to 18.

:handle_size: str

    The size of the handle. Can be a css length or an integer, which will be the diameter of the handle. Defaults to 34.

:enabled: bool

    Disable interactivity

:visible: bool

    Is the component visible

:spacing_above: str

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:spacing_below: str

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``



Methods
-------

:reset:
    Resets the slider to its initial position i.e. it's ``start`` property


Events
------

:slide:

    Raised whenever the slider is sliding. The handle is provided as an argument to determine which handle is sliding.

:change:

    Raised whenever the slider has finished sliding. The handle is provided as an argument to determine which handle is sliding.
    Change is the writeback event.


:show:

    Raised when the component is shown.


:hide:

    Raised when the component is hidden.
