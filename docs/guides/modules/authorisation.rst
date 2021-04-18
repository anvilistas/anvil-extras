Authorisation
=============
A server module that provides user authentication and role based authorisation
for server functions.

Installation
------------

You will need to setup the Users and Data Table services in your app:

  * Ensure that you have added the 'Users' service to your app
  * In the 'Data Tables' service, add:
  	* a table named 'permissions' with a text column named 'name'
	* a table named 'roles' with a text column named 'name' and a 'link to table'column named 'permissions' that links to multiple rows of the permissions table
	* a new 'link to table' column in the Users table named 'roles' that links to multiple rows of the 'roles' table

Usage
-----

Users and Permissions
+++++++++++++++++++++

* Add entries to the permissions table. (e.g. 'can_view_stuff', 'can_edit_sensitive_thing')
* Add entries to the roles table (e.g. 'admin') with links to the relevant permissions
* In the Users table, link users to the relevant roles

Server Functions
++++++++++++++++
The module includes two decorators which you can use on your server functions:

`authentication_required`

Checks that a user is logged in to your app before the function is called and raises
an error if not. e.g.:

.. code-block:: python

    import anvil.server
    from anvil_extras.authorisation import authentication_required

    @anvil.server.callable
    @authentication_required
    def sensitive_server_function():
      do_stuff()

`authorisation_required`

Checks that a user is logged in to your app and has sufficient permissions before the
function is called and raises an error if not:

.. code-block:: python

    import anvil.server
    from anvil_extras.authorisation import authorisation_required

    @anvil.server.callable
    @authorisation_required("can_edit_sensitive_thing")
    def sensitive_server_function():
      do_stuff()

You can pass either a single string or a list of strings to the decorator. The function
will only be called if the logged in user has ALL the permissions listed.

Notes:
* The order of the decorators matters. `anvil.server.callable` must come before either of the authorisation module decorators.
