Serialisation
=============
A server module that provides dynamic serialisation of data table rows.

A single data table row is converted to a dictionary of simple Python types.
A set of rows is converted to a list of those dictionaries.

Usage
-----
Let's imagine we have a data table named 'books' with columns 'title' and 'publication_date'.

In a server module, import and call the function `datatable_schema` to get a `marshmallow <https://marshmallow.readthedocs.io/en/stable/>`_ Schema instance:

.. code-block:: python

   from anvil.tables import app_tables
   from anvil_extras.serialisation import datatable_schema
   from pprint import pprint

   schema = datatable_schema("books")

To serialise a row from the books table, call the schema's `dump` method:

.. code-block:: python

   book = app_tables.books.get(title="Fluent Python")
   result = schema.dump(book)
   pprint(result)

   >> {"publication_date": "2015-08-01", "title": "Fluent Python"}

To serialise several rows from the books table, set the `many` argument to True:

.. code-block:: python

   books = app_tables.books.search()
   result = schema.dump(books, many=True)
   pprint(result)

   >> [{'publication_date': '2015-08-01', 'title': 'Fluent Python'},
   >>  {'publication_date': '2015-01-01', 'title': 'Practical Vim'},
   >>  {'publication_date': None, 'title': "The Hitch Hiker's Guide to the Galaxy"}]


To exclude the publication date from the result, pass its name to the server function:

.. code-block:: python

   from anvil.tables import app_tables
   from anvil_extras.serialisation import datatable_schema
   from pprint import pprint

   schema = datatable_schema("books", ignore_columns="publication_date")
   books = app_tables.books.search()
   result = schema.dump(books, many=True)
   pprint(result)

   >> [{'title': 'Fluent Python'},
   >>  {'title': 'Practical Vim'},
   >>  {'title': "The Hitch Hiker's Guide to the Galaxy"}]

You can also pass a list of column names to ignore.

If you want the row id included in the results, set the `with_id` argument:

.. code-block:: python

   from anvil.tables import app_tables
   from anvil_extras.serialisation import datatable_schema
   from pprint import pprint

   schema = datatable_schema("books", ignore_columns="publication_date", with_id=True)
   books = app_tables.books.search()
   result = schema.dump(books, many=True)
   pprint(result)

   >> [{'_id': '[169162,297786594]', 'title': 'Fluent Python'},
   >>  {'_id': '[169162,297786596]', 'title': 'Practical Vim'},
   >>  {'_id': '[169162,297786597]',
   >>   'title': "The Hitch Hiker's Guide to the Galaxy"}]


Linked Tables
+++++++++++++
Let's imagine we also have an 'authors' table with a 'name' column and that we've added
an 'author' linked column to the books table.

To include the author in the results for a books search, create a dict to define, for each table, the linked columns in that table the linked table they refer to:

.. code-block:: python

   from anvil.tables import app_tables
   from anvil_extras.serialisation import datatable_schema
   from pprint import pprint

   # The books table has one linked column named 'author' and that is a link to the 'authors' table
   linked_tables = {"books": {"author": "authors"}}
   schema = datatable_schema(
       "books",
       ignore_columns="publication_date",
       linked_tables=linked_tables,
    )
   books = app_tables.books.search()
   result = schema.dump(books, many=True)
   pprint(result)

   >> [{'author': {'name': 'Luciano Ramalho'}, 'title': 'Fluent Python'},
   >>  {'author': {'name': 'Drew Neil'}, 'title': 'Practical Vim'},
   >>  {'author': {'name': 'Douglas Adams'},
   >>   'title': "The Hitch Hiker's Guide to the Galaxy"}]

Finally, let's imagine the 'authors' table has a 'date_of_birth' column but we don't want to include that in the results:


.. code-block:: python

   from anvil.tables import app_tables
   from anvil_extras.serialisation import datatable_schema
   from pprint import pprint

   linked_tables = {"books": {"author": "authors"}}
   ignore_columns = {"books": "publication_date", "authors": "date_of_birth"}
   schema = datatable_schema(
       "books",
       ignore_columns=ignore_columns,
       linked_tables=linked_tables,
    )
   books = app_tables.books.search()
   result = schema.dump(books, many=True)
   pprint(result)

   >> [{'author': {'name': 'Luciano Ramalho'}, 'title': 'Fluent Python'},
   >>  {'author': {'name': 'Drew Neil'}, 'title': 'Practical Vim'},
   >>  {'author': {'name': 'Douglas Adams'},
   >>   'title': "The Hitch Hiker's Guide to the Galaxy"}]
