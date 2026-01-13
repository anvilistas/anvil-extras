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
	* a new 'link to table' column in the Users table named 'roles' that links to multiple rows of the 'roles' table (This behaviour is configurable - see below)

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

Configuration Options
+++++++++++++++++++++
Certain default behaviour is configurable.

By default the user's table expects a 'roles' column, that links to multiple rows of the 'roles' table.
Alternatively you can create a table that maps a user to linked rows of the role's table, avoiding adding extra columns to the user's table.

* Create a table called 'usermap' with a column 'user' and a column 'roles'.
* the 'user' column is a link to a row in the user's table. The 'roles' column is a link to multiple rows from the 'roles' table.

.. code-block:: python

    import anvil.server
    from anvil_extras.authorisation

    authorisation.set_config(get_roles="usermap")

Now the authorisation module will use the 'usermap' table to get roles for a user.

API
---

.. function:: authentication_required(fn)

    Use as a decorator for any server function that requires a logged in user

.. function:: authorisation_required(permissions)

    Use as a decorator above a server function
    permissions should be a string or iterable of strings


.. function:: has_permission(permissions[, user])

    Returns True/False on whether a user is logged in and has valid permissions

    If ``user`` is not provided, defaults to ``anvil.users.get_user()``

.. function:: check_permissions(permissions[, user])

    Raises a ValueError if there is no user or the user does not have valid permissions

    If ``user`` is not provided, defaults to ``anvil.users.get_user()``

.. function:: set_config(**kwargs)

    Sets custom configuration of this module. Accepts get_roles='table_name' as a keyword argument.
