# Unreleased

## Updates
* Slider Component - bump javascript dependency and refactor. No changes to the component's public API.
  https://github.com/anvilistas/anvil-extras/pull/112

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
