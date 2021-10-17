
# Unreleased

## Updates:
* storage supports `datetime` and `date` objects
  https://github.com/anvilistas/anvil-extras/pull/179
* `on_form_load()` can be used in a `routing.main_router` Form
  This method will be fired with the current `url_hash` and the `form` that was added to the `content_panel`.
  https://github.com/anvilistas/anvil-extras/pull/180

## Bug fixes
* MultiSelect component works correctly in a popover
  https://github.com/anvilistas/anvil-extras/pull/187


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
