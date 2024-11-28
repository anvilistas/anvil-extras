# v3.1.0

## Bug Fixes
* tabs - tab color was not being applied to inactive tabs
  https://github.com/anvilistas/anvil-extras/issues/570
* persistence - orginal class was missing from the resulting base classes
  https://github.com/anvilistas/anvil-extras/pull/573
* persistence - linked class attributes were not handling None values correctly
  https://github.com/anvilistas/anvil-extras/pull/577
* popover - fix bug with popovers not handling dom nodes correctly
  https://github.com/anvilistas/anvil-extras/pull/580
* theme - fix Colors() without a variant argument
  https://github.com/anvilistas/anvil-extras/pull/581

## Enhancements
* tabs - tab color can now be a css var and better support for css colors in general
  https://github.com/anvilistas/anvil-extras/pull/570
* messaging - support custom loggers in messaging module
  https://github.com/anvilistas/anvil-extras/issues/569
* persistence - Handle addition and updates of instances with linked classes
  https://github.com/anvilistas/anvil-extras/pull/575

## Deprecations
- messaging - with_logging argument is deprecated and maybe removed in a future version
  logging messages is now off by default - to turn it on provide a custom `logger` argument
  https://github.com/anvilistas/anvil-extras/pull/572/files
- persistence - LinkedAttribute is deprecated and will be removed in a future version  https://github.com/anvilistas/anvil-extras/pull/578

# v3.0.0

## Bug Fixes
* popover - fix bug where popovers could not be used on forms using layouts
  https://github.com/anvilistas/anvil-extras/issues/553
* ChipsInput - Chip close icon color is fixed for the last highlighted chip
  https://github.com/anvilistas/anvil-extras/issues/567

## Breaking Changes
* popover - rewritten without bootstrap, now uses floating-ui
  `dismiss_on_scroll` is deprecated
  class names on the popover element have changed
  https://github.com/anvilistas/anvil-extras/pull/563
* multi-select - rewritten without bootstrap, now uses popover and basic anvil components
  https://github.com/anvilistas/anvil-extras/pull/566
* classic editor - design components are no longer supported
  https://github.com/anvilistas/anvil-extras/issues/567
* class-names and roles - all anvil extras components now use class names and roles prefixed with `ae-`
  https://github.com/anvilistas/anvil-extras/issues/567


# v2.7.0 05-Sep-2024

## New Features
* theme module - Define and switch between colour schemes via code
  https://github.com/anvilistas/anvil-extras/pull/551
* quill - implement get_markdown()
  https://github.com/anvilistas/anvil-extras/pull/557

## Minor Changes
* persistence - add reset method
  https://github.com/anvilistas/anvil-extras/pull/542
* persistence - add set behaviour for linked classes

## Bug Fixes
* multiselect - fix bug where enable_selct_all was not being set correctly
  https://anvil.works/forum/t/anvil-extras-2-6/21252/4
* non-blocking - fix catching exceptions when accessing a non-blocking promise
  https://github.com/anvilistas/anvil-extras/pull/543
* multiselect - fix select all buttons overlapping when using width=fit
  https://github.com/anvilistas/anvil-extras/issues/545
* mulitselect - fix bug where properties were not being set correctly
  https://github.com/anvilistas/anvil-extras/issues/554
* augment - fix bug where event couldn't be used as a raise_event kw
  https://anvil.works/forum/t/tabulator-multiple-value-error-on-row-click/22158/9


# v2.6.2 13-Jun-2024

## Minor Changes
* authorisation - added config option to avoid adding a roles column to the users table
  https://github.com/anvilistas/anvil-extras/pull/516
* storage - proxyobjects are passed to the underlying storage so that those implementing the serializable interface can be stored
  https://github.com/anvilistas/anvil-extras/pull/533

## Bug Fixes
* Slider - allow connect and behaviour to be set at runtime
  https://github.com/anvilistas/anvil-extras/issues/538
* persistence - fix get method
  https://github.com/anvilistas/anvil-extras/issues/523
* persistence - fix handling of Linked Attributes with no row
  https://github.com/anvilistas/anvil-extras/issues/534
* MultiSelect - fix an issue with multiselect on the self hosted app server
  https://github.com/anvilistas/anvil-extras/issues/525
* routing - fix redirect with None conditions
  https://github.com/anvilistas/anvil-extras/pull/532
* MultiSelect - fix an issue where the dropdown menu would remain open when the form is hidden
  https://github.com/anvilistas/anvil-extras/issues/536


# v2.6.1 27-Mar-2024

## Bug Fixes
* routing - fix initialisation of history state
  https://github.com/anvilistas/anvil-extras/discussions/519
* multiselect - fix visible False property in the designer
  https://github.com/anvilistas/anvil-extras/issues/510
* multiselect - fix toggling enabled property loses selected state
  https://github.com/anvilistas/anvil-extras/issues/513
* switch - fix lever color when switch is checked
  https://github.com/anvilistas/anvil-extras/pull/517
* routing - fix on_form_load might fire stale value if form_show event is slow
  https://github.com/anvilistas/anvil-extras/discussions/521

## Minor Changes
* designer hints - add some designer hints to components
  https://github.com/anvilistas/anvil-extras/pull/512
* authorisation - added config option to avoid adding a roles column to the users table
  https://github.com/anvilistas/anvil-extras/pull/516

# v2.6.0 09-Feb-2024

## Bug Fixes
* routing - fix rendering slow loading pages
  https://github.com/anvilistas/anvil-extras/pull/501
* logging - add missing date format parameter
  https://github.com/anvilistas/anvil-extras/pull/502
* logging - fix critical error message displays as warning
  https://github.com/anvilistas/anvil-extras/pull/505

## Minor Changes
* tabs - add better support for using faded colors e.g. `tabs.active_background = "#2196F344"`
  https://github.com/anvilistas/anvil-extras/pull/483
* augment - use python implementation
  https://github.com/anvilistas/anvil-extras/pull/488
* non-blocking: add a getter to expose the raw javascript promise
  https://github.com/anvilistas/anvil-extras/pull/475

## Deprecations
* augment - trigger("writeback") is now deprecated - use the native version instead `raise_event('x-anvil-write-back-<property-name>)`
  https://github.com/anvilistas/anvil-extras/issues/429


# v2.5.4 15-Nov-2023

## Enhancements
* Tabs - adds active_background property
  https://github.com/anvilistas/anvil-extras/issues/481

## Bug Fixes
* storage - fix a bug in ios when indexed db accessed in a webworker and closed
  https://github.com/anvilistas/anvil-extras/discussions/484
* routing - preserve properties when changing templates
  https://github.com/anvilistas/anvil-extras/discussions/486


# v2.5.2 25-Oct-2023
* storage - fix bug with deserializing

# v2.5.0 3-Oct-2023

## New Features
* authorisation - adds `check_permissions` and `has_permission` functions
  https://github.com/anvilistas/anvil-extras/issues/382
* `routing.lazy_route` - allows you to lazily load Forms whilst using routing
  https://github.com/anvilistas/anvil-extras/pull/442
* Autocompletion: adds filter_mode property - either contains or startswith
  https://github.com/anvilistas/anvil-extras/discussions/444
* navigation - ``set_mode("hash")`` can be used to set the default navigation mode to hash routing
  https://github.com/anvilistas/anvil-extras/discussions/458
* navigation - menu definition can include ``title``, rather than registering a form with a title
  https://github.com/anvilistas/anvil-extras/discussions/453
* navigation - set menu item visibility using conditions defined in the menu definition
  https://github.com/anvilistas/anvil-extras/pull/460
* view transitions - routing and navigation use a transition on page changes (can be turned off)
  https://github.com/anvilistas/anvil-extras/pull/465
* Progress Bars - support dynamic property changes
  https://github.com/anvilistas/anvil-extras/pull/466

## Bug Fixes
* pivot - don't fail if self.items is not set
  https://github.com/anvilistas/anvil-extras/pull/468
* routing was no longer dismissing alerts on navigation
  you will now need to use `routing.alert` in place of `anvil.alert` for an alert to be dismissed on navigation
  non-dismissible alerts will block the navigation
  https://github.com/anvilistas/anvil-extras/pull/437
* tabs - ensure the selected tab indicator adjusts when the tab component changes size
  https://github.com/anvilistas/anvil-extras/pull/467

## Minor Changes
* Slider - improve behaviour in the designer
  https://github.com/anvilistas/anvil-extras/pull/472
* wait_for_writeback is now written in pure python
  https://github.com/anvilistas/anvil-extras/pull/431
* Switch - improve designer behaviour
  https://github.com/anvilistas/anvil-extras/pull/470

# v2.4.0 14-Jun-2023

## New Features
* Add non-blocking module
  https://github.com/anvilistas/anvil-extras/pull/411

## Bug Fixes
* augment - adding event handler like click to a button will no longer fire twice
  https://github.com/anvilistas/anvil-extras/pull/412
* autocomplete - fix suggestions position on mobile in M3 design
  https://github.com/anvilistas/anvil-extras/issues/413
* tabs - tweak css for better mobile experience
  https://github.com/anvilistas/anvil-extras/issues/421
* autocomplete - changing the suggestions will force the UI to change
  https://github.com/anvilistas/anvil-extras/issues/426

# v2.3.0 10-Apr-2023

## New Features
* add zod validation library
  https://github.com/anvilistas/anvil-extras/pull/406

## Minor Changes
* Add use of kwargs in persistent class init method
  https://github.com/anvilistas/anvil-extras/pull/408

# v2.2.3 03-Mar-2023
## Bug Fixes
* Raise TableError when accessing non-existent columns on persisted class

# v2.2.2 02-Mar-2023
## Bug Fixes
* Fix attribute handling for new instances

# v2.2.1 01-Mar-2023
## Bug Fixes
* Typo in persistence module fixed

# v2.2.0 01-Mar-2023
## Notable Change
* persistence - Define simple classes for use in client side code and have instances of those classes synchronised with data tables rows.

## Minor Changes
* add `tag` property to custom components
  https://anvil.works/forum/t/chip-tag-initialization/15461
* add `format_selected_text` method override for multi-select-dropdown
  https://github.com/anvilistas/anvil-extras/issues/398

* add `selected_keys` property for multi-select-dropdown
  https://github.com/anvilistas/anvil-extras/issues/398

## Bug Fixes
* `navigation` - Add args and kwargs to `open_form`
  https://github.com/anvilistas/anvil-extras/pull/393
* `storage` - fix serialisation of dictionary values
  https://github.com/anvilistas/anvil-extras/pull/395

# v2.1.4 01-Dec-2022
## Bug Fixes
* `routing` - fix `routing.ANY` within `url_keys`
  https://github.com/anvilistas/anvil-extras/pull/388

## Deprecations

* `anvil_extras.uuid` module can be replaced wholesale by uuid from stdlib
  DeprecatedWarning added to `uuid.uuid4()`

## Minor Changes
* Some component properties adjusted to type enum so they can be selected, rather than typed, in the designer


# v2.1.3 03-Nov-2022

## Minor Changes
* `uuid` and `storage` will check if `uuid` and `localforage` are aleady installed before importing them from cdn
  https://github.com/anvilistas/anvil-extras/pull/381

## Bug Fixes
* `routing` - `form.url_dict` will be updated when `redirect=False`
  https://github.com/anvilistas/anvil-extras/issues/374

# v2.1.2 01-Sep-2022

## Bug Fixes
* `routing` - remove_from_cache will work across templates
  https://github.com/anvilistas/anvil-extras/issues/367
* `MultiSelectDropDown` - fix setting certain attributes dynamically cause events to stop firing
  https://github.com/anvilistas/anvil-extras/issues/365


# v2.1.1 22-Jun-2022

## Minor changes
* `augment` ensure that `"mouseenter"` is always correct event type in `"hover"` events
  https://github.com/anvilistas/anvil-extras/discussions/319
* `augment` adjust handling of RadioButton to work correctly with the augment module
  https://github.com/anvilistas/anvil-extras/pull/325
* `routing` - to catch arbirtrary query params in a route use `url_keys=[routing.ANY]`
  https://github.com/anvilistas/anvil-extras/issues/342

## Bug fixes
* `augment` - DataGrid's pagination click event prevented other events from being added
  https://github.com/anvilistas/anvil-extras/pull/325
* `MultiSelectDropDown` - all properties are now dynamic and can be updated in code
  https://github.com/anvilistas/anvil-extras/pull/331
* `serialisation` - support accelerated tables with linked columns
  https://github.com/anvilistas/anvil-extras/issues/350
* `navigation` - Now handles links with roles defined when setting 'selected'
  https://github.com/anvilistas/anvil-extras/issues/352
* `popovers` fix bug scrolling on mobile
  https://github.com/anvilistas/anvil-extras/discussions/324

## New Features
* `MultiSelectDropDown`: add `width` property with options for `fit` and `auto` sizing
  https://github.com/anvilistas/anvil-extras/issues/329
* `navigation` - new `set_title` function for custom click handlers
  https://github.com/anvilistas/anvil-extras/issues/358

# v2.1.0 20-Apr-2022

## Notable Change
* `@auto_refreshing` - the original item will now be proxied rather than copied.
  Changes to the proxied item will make changes to the original item.
  https://github.com/anvilistas/anvil-extras/pull/311
* `MultiSelectDropDown` - the change event will **only** fire with user interaction.
  Previously also fired when the `selected` property was changed in code.
  This behaviour now matches other anvil Components - e.g. changing the `selected_value`
  of a DropDown does **not** fire the DropDown change event.
  https://github.com/anvilistas/anvil-extras/issues/307

## New Features
* routing - a template argument was added to the `@routing.route` decorator.
  This argument determines which templates a route can be added to.
  https://github.com/anvilistas/anvil-extras/issues/293
* routing - a tempalate can take multiple paths `@routing.template(path=["admin", "user"])`
  https://github.com/anvilistas/anvil-extras/pull/298
* routing - `@routing.redirect()` decorator added
  https://github.com/anvilistas/anvil-extras/pull/298
* hashlib module added
  https://github.com/anvilistas/anvil-extras/pull/301
* `utils.import_module`: similar implementation to python's `importlib.import_module`
  https://github.com/anvilistas/anvil-extras/pull/302
* `MultiSelectDropDown`: add events `opened` and `closed`
  https://github.com/anvilistas/anvil-extras/issues/279

## Bug Fixes
* `MultiSelectDropDown`: fix change event should only fire on user interaction
  https://github.com/anvilistas/anvil-extras/issues/307
* `@auto_refreshing`: support auto_refreshing when the item is not explicitly set
  https://github.com/anvilistas/anvil-extras/issues/250

# v2.0.1 16-Mar-2022

## BugFixes:
* routing - fix regression with before unload
  https://github.com/anvilistas/anvil-extras/issues/289

# v2.0.0 15-Mar-2022

## Breaking Changes
* `routing.load_form()` was removed. Use `routing.set_url_hash()` instead.

## New Features
* Popovers - supports changing the default container to something other than `"body"`
  add `dismiss_on_scroll()` and `set_default_container()` methods
  https://github.com/anvilistas/anvil-extras/pull/268
* Quill - adds a sanitize property and a sanitize kwarg to the `set_html()` method
  https://github.com/anvilistas/anvil-extras/issues/273
* routing - adds support for multiple top level forms
  https://github.com/anvilistas/anvil-extras/pull/281
  * **`@routing.template(path='', priority=0, condition=None)`**
     A template form is a top level form that holds the header, navigation bar, side panel and an empty `content_panel`.
     When navigating the routing module will ensure the correct template is the current `open_form` based on the `priority`, `path`, and `condition`. The current `url_hash` must start with the `path`, and if a `condition` is set it must return `True`.
     Templates are checked order of priority, highest values first.
  * **`@routing.default_template` replaces `@routing.main_router`**.
     The `@main_router` decorator is still available. `@default_template` is equivalent to `@template()`
  * **`routing.NavigationExit()`**
     when raised within a `template`'s `on_navgation` callback, this will prevent the `routing` module from changing the `content_panel`.
     This is useful if you have a `LoginForm` as a `template` whose content should remain unchanged when the user tries to navigate to other `routes`.
  * **`routing.launch()`**
    called within a startup module, replaces the call to `open_form()`.
    `routing.launch()` checks the current `url_hash` and ensures that the correct template is loaded based on the paramaters of each template.
    Calling `routing.set_url_hash()` in a Startup Module will have no effect on form loading until `routing.launch()` has been called. (This allows you to change the `url_hash` within the startup logic)
* `logging` module
  https://github.com/anvilistas/anvil-extras/pull/282
  Small, simple, lightweight API for logging in anvil apps, a bit like the Python logging module.
  See the docs:
  * `Logger` https://anvil-extras.readthedocs.io/en/latest/guides/modules/logging.html#logger
  * `TimerLogger` https://anvil-extras.readthedocs.io/en/latest/guides/modules/logging.html#timerlogger

## Bug fixes
* Multi-select - fix button clicks don't always close the dropdown menu
  https://github.com/anvilistas/anvil-extras/issues/271
* fix bug with `@timed` decorator if used with keyword logger and level arguments
  https://github.com/anvilistas/anvil-extras/pull/282


# v1.9.0 27-Jan-2022

## New Features
* Select All functionality added to MultiSelect component
* Dynamic serialisation of data tables rows
  https://github.com/anvilistas/anvil-extras/pull/191
* `utils.correct_canvas_resolution()` - canvas elements can look blurry on retina displays
  This function sharpens the resolution of a canvas element when called in the reset event
  https://github.com/anvilistas/anvil-extras/pull/202
* `augment.remove_event_handler()` added to the augment module
  https://github.com/anvilistas/anvil-extras/pull/259
* Slider - visual properties - `handle_size`, `bar_height`, and `role` added
  https://github.com/anvilistas/anvil-extras/pull/261

## Updates:
* storage supports `datetime` and `date` objects
  https://github.com/anvilistas/anvil-extras/pull/179
* `on_form_load()` can be used in a `routing.main_router` Form
  This method will be fired with the current `url_hash` and the `form` that was added to the `content_panel`.
  https://github.com/anvilistas/anvil-extras/pull/180
* `animate` duration argument is no longer keyword only i.e. `animate(self, fade_in, 300)` is valid
  https://github.com/anvilistas/anvil-extras/pull/182

## Bug fixes
* MultiSelect component works correctly in a popover
  https://github.com/anvilistas/anvil-extras/pull/187
* popover `is_visible` bug when using `pop("toggle")`
  https://github.com/anvilistas/anvil-extras/pull/199
* Using routing load_from_cache=False to reload the current form works correctly
  https://github.com/anvilistas/anvil-extras/issues/243
* PageBreak retains its thickness in print mode
  https://github.com/anvilistas/anvil-extras/issues/263

# v1.8.1 14-Oct-2021

## Updates
* `has_popover()` function added to the popover module
  https://github.com/anvilistas/anvil-extras/pull/171

* `Transition` class in the animate module is more flexible for combining transitions.
  Some pre-computed transitions adjusted. `rotate_in/rotate_out` replaced by `rotate`
  https://github.com/anvilistas/anvil-extras/pull/173

# v1.8.0 13-Oct-2021

## New Features
* animation module - Wrap the Web Animations API around a convenient set of python tools for anvil
  https://github.com/anvilistas/anvil-extras/pull/169

## Bug Fixes
* MultiSelectDropdown - Fix "Hides menu when component is removed from the page"
  https://github.com/anvilistas/anvil-extras/pull/170

# v1.7.1 06-Oct-2021
## Bug Fixes
*

# v1.7.0 06-Oct-2021

## New Features
* Pivot - Dynamic pivot table component
  https://github.com/anvilistas/anvil-extras/pull/165

## Bug Fixes
* MultiSelectDropdown - Hides menu when component is removed from the page
  https://github.com/anvilistas/anvil-extras/pull/149
* Popover - content's show and hide events will be triggered when the popover shows and hides
  https://github.com/anvilistas/anvil-extras/pull/150
* Autocomplete - Add missing TextBox properties to design view
  https://github.com/anvilistas/anvil-extras/pull/160

# v1.6.0 17-Sep-2021

## New Features
* Quill - dynamically add custom modules
  https://github.com/anvilistas/anvil-extras/pull/117
* routing - adjusts the behaviour of anvil.alert to ensure dismissible alerts are closed on navigation. And navigation prevented for non-dismissible alerts.
  https://github.com/anvilistas/anvil-extras/pull/132
* `storage.indexed_db` - Now supports the browser's `IndexedDB` with a dictionary like api
  https://github.com/anvilistas/anvil-extras/pull/135
* storage - additional store objects can be created inside the browsers `localStorage` or `IndexedDB`. e.g. `todo_store = indexed_db.get_store('todos')`
  Each store object behaves like a dictionary object.
  https://github.com/anvilistas/anvil-extras/pull/135
* PageBreak - `border` property added and documentation updated.
  https://github.com/anvilistas/anvil-extras/pull/139

## Bug Fixes
* Autocomplete - can now be used inside an alert
  https://github.com/anvilistas/anvil-extras/pull/114
* Popover - fix stickyhover
  https://github.com/anvilistas/anvil-extras/pull/121
* storage - update and clear were missing from the documented api
  https://github.com/anvilistas/anvil-extras/pull/125
* PageBreak - fix margin_top property and make it optional
  https://github.com/anvilistas/anvil-extras/pull/137
* PageBreak and Multi-select - fix illegal HTML
  https://github.com/anvilistas/anvil-extras/pull/139
* Popover - remove the requirement for delays in show/hide/destroy transitions
  https://github.com/anvilistas/anvil-extras/pull/146

## Deprecated
* storage.session_storage was deprecated. Use local_storage instead
  https://github.com/anvilistas/anvil-extras/pull/135

## Updates
* Slider Component - bump javascript dependency and refactor. No changes to the component's public API.
  https://github.com/anvilistas/anvil-extras/pull/112
* Autocomple - duplicate suggestions are ignored and a warning is printed
  https://github.com/anvilistas/anvil-extras/pull/116
* Popover - documentation added and clone link updated. The example now imports `anvil_extras`
  https://github.com/anvilistas/anvil-extras/pull/121

# v1.5.2 23-Aug-2021

## New Features
* `augment` - `add_event_handler()` method added. `original_event` passed as an `event_arg`.
  https://github.com/anvilistas/anvil-extras/pull/109

## Bug Fixes
* Add missing support for binding writeback on the Switch component
  https://github.com/anvilistas/anvil-extras/pull/111

# v1.5.1 05-Jul-2021

## Bug Fixes
* Autocompleter suggestions on mobile
  https://github.com/anvilistas/anvil-extras/issues/103

# v1.5.0 29-Jun-2021

## New Features
* `local_storage` - wrapper around the browser localStorage object
  https://github.com/anvilistas/anvil-extras/pull/93

## Changes
* Quill editor supports a toolbar and theme set at runtime.
  https://github.com/anvilistas/anvil-extras/pull/80
* Add navigation.go_to function, improved navigation error messages
  https://github.com/anvilistas/anvil-extras/pull/99

## Bug Fixes
* Autocompleter focus method doesn't trigger autocomplete suggestions
  https://github.com/anvilistas/anvil-extras/issues/94
* Improve error reporting when passing an invalid content object to a popover
  https://github.com/anvilistas/anvil-extras/issues/90
* Fixed the publisher.unsubscribe method in the Messaging module, making it functional
  https://github.com/anvilistas/anvil-extras/pull/92
* Fix indeterminate progress bar not always displaying
  https://github.com/anvilistas/anvil-extras/issues/95

# v1.4 07-June-2021

## New Features
* Tabs Component
  https://github.com/anvilistas/anvil-extras/pull/64
* uuid4 in the browser
  https://github.com/anvilistas/anvil-extras/pull/67
* Chip Component and ChipsInput Component
  https://github.com/anvilistas/anvil-extras/pull/68
* AutoComplete Component
  https://github.com/anvilistas/anvil-extras/pull/70

## Changes
* Improved dynamic designer support for Switch, MultiSelectDropDown, Tabs, Quill and Slider
  https://github.com/anvilistas/anvil-extras/pull/66

# v1.3.1 31-May-2021
* Improved slider formatting
  https://github.com/anvilistas/anvil-extras/pull/61

# v1.3.0 31-May-2021

## New Features
* Update styling of switch component
  https://github.com/anvilistas/anvil-extras/pull/56
* Include pagination_click event in augment module
  https://github.com/anvilistas/anvil-extras/pull/55
* Slider Component
  https://github.com/anvilistas/anvil-extras/pull/60

## Changes
* Refactor of progress bars
  https://github.com/anvilistas/anvil-extras/pull/59

# v1.2.0 25-May-2021

## New Features
* component.trigger('writeback')
  https://github.com/anvilistas/anvil-extras/pull/47
* MultiSelectDropDown component
  https://github.com/anvilistas/anvil-extras/pull/44
* @wait_for_writeback decorator
  https://github.com/anvilistas/anvil-extras/pull/50
* Quill component
  https://github.com/anvilistas/anvil-extras/pull/52
* Switch component
  https://github.com/anvilistas/anvil-extras/pull/31

# v1.1.0 27-Mar-2021

## New Features
* Auto Refreshing Item
  https://github.com/anvilistas/anvil-extras/pull/39

# v1.0.0 11-Mar-2021

* Initial release
