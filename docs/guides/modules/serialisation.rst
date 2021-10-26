Serialisation
=============
A server module that provides dynamic serialisation of data table rows.

Usage
-----
Let's imagine we have a data table named 'books' with columns 'title' and 'publication_date'.

In a server module, call the server function `schema_from_table` get a `marshmallow <https://marshmallow.readthedocs.io/en/stable/>`_ Schema class:

.. code-block:: python

   from anvil.tables import app_tables
   from anvil-extras.server_code.serialisation import schema_from_table

   Schema = schema_from_table("books")

To serialise a row from the books table, create an instance of the Schema class and call its `dumps` method:

.. code-block:: python

   schema = Schema()
   book = app_tables.books.get(title="Fluent Python")
   result = schema.dumps(book)

To serialise all the rows from the books table, set the `many` attribute of the schema object:

.. code-block:: python

   schema = Schema(many=True)
   books = app_tables.books.search()
   result = schema.dumps(books)

To exclude the publication date from the result, pass its name to the server function:

.. code-block:: python

   from anvil.tables import app_tables
   from anvil-extras.server_code.serialisation import schema_from_table

   Schema = schema_from_table("books", ignore_colums="publication_date")
   books = app_tables.books.search()
   schema = Schema(many=True)
   result = schema.dumps(books)

You can also pass a list of column names to ignore.

If you want the row id included in the results, set the `with_id` argument:

.. code-block:: python

   from anvil.tables import app_tables
   from anvil-extras.server_code.serialisation import schema_from_table

   Schema = schema_from_table("books", ignore_colums="publication_date", with_id=True)
   books = app_tables.books.search()
   schema = Schema(many=True)
   result = schema.dumps(books)

Linked Tables
+++++++++++++
Let's imagine we also have an 'authors' table with a 'name' column and that we've added
an 'author' linked column to the books table.

To include the author in the results for a books search, create a dict to define, for each table, the linked columns in that table the linked table they refer to:

.. code-block:: python

   from anvil.tables import app_tables
   from anvil-extras.server_code.serialisation import schema_from_table

   # The books table has one linked column named 'author' and that is a link to the 'authors' table
   linked_tables = {"books": {"author": "authors"}
   Schema = schema_from_table(
       "books",
       ignore_colums="publication_date",
       linked_tables=linked_tables,
    )
   books = app_tables.books.search()
   schema = Schema(many=True)
   result = schema.dumps(books)

Finally, let's imagine the 'authors' table has a 'date_of_birth' column but we don't want to include that in the results:


.. code-block:: python

   from anvil.tables import app_tables
   from anvil-extras.server_code.serialisation import schema_from_table

   # The books table has one linked column named 'author' and that is a link to the 'authors' table
   linked_tables = {"books": {"author": "authors"}
   ignore_columns = {"books": "publication_date", "authors": "date_of_birth"}
   Schema = schema_from_table(
       "books",
       ignore_colums=ignore_columns,
       linked_tables=linked_tables,
    )
   books = app_tables.books.search()
   schema = Schema(many=True)
   result = schema.dumps(books)
