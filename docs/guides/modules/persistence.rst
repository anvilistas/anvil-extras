Persistence
===========

Define simple classes for use in client side code and have instances of those classes synchronised with data tables rows.


Example
-------

Let's say we have an app that displays books. It has two tables, author and book, with
columns:

.. code-block::

   author
       name: text

   book
       title: text
       author: linked_column (to author table)


The author table contains a row whose name is "Luciano Ramalho" and the book table a row
with the title "Fluent Python" and author linked to the row in the author table.

Using the persistence module, we can now define a class for book objects:


.. code-block:: python

   from anvil_labs.persistence import persisted_class


   @persisted_class
   class Book:
        key = "title"

The data table must have a column with unique entries for each row and we define which that is using the `key` attribute. In this case, we'll assume every book has a unique title.

We can now use that class by creating an instance and telling it to fetch the associated
row from the database:


.. code-block:: python

   book = Book.get("Fluent Python")


our `book` object will automatically have each of the row's columns as an attribute:


.. code-block:: python

   assert book.title == "Fluent Python"


But what if we wanted our `book` object to include some information from the author table?

There are two ways to go about that: using a LinkedAttribute or a LinkedClass.

LinkedAttribute
+++++++++++++++
We can use a `LinkedAttribute` to fetch data from the linked row and include it as an
attribute on our object. Let's include the author's name as an attribute of a book:


.. code-block:: python

   from anvil_labs.persistence import persisted_class, LinkedAttribute


   @persisted_class
   class Book:
       key = "title"
       author_name = LinkedAttribute(linked_column="author", linked_attr="name")


    book = Book.get("Fluent Python")

    assert book.author_name == "Luciano Ramalho"


LinkedClass
+++++++++++
Alternatively, we can define another persisted class for author objects and use an
instance of that class as an attribute of a Book:

.. code-block:: python

   from anvil_labs.persistence import persisted_class

   @persisted_class
   class Author:
       key = "name"


   @persisted_class
   class Book:
       author = Author


   book = Book.get("Fluent Python")

   assert book.author.name == "Luciano Ramalho"


Customisation
+++++++++++++
We can, of course, add whatever methods we want to our class. Let's add a property to
display the title and author of the book as a single string:


.. code-block:: python

   from anvil_labs.persistence import persisted_class, LinkedAttribute


   @persisted_class
   class Book:
       key = "title"
       author_name = LinkedAttribute(linked_column="author", linked_attr="name")

       @property
       def display_text(self):
           return f"{self.title} by {self.author_name}"

   book = Book.get("Fluent Python")

   assert book.display_text == "Fluent Python by Luciano Ramalho"


*NOTE* If you create attributes with leading underscores, they will not form part of
any update sent to a server function.

Getting and Searching
---------------------
In the example above, we used the `get` method to fetch a single data table row from the database and create a `Book` instance from it.

For that to work, there needs to be a server function that takes the Book's key as an argument and returns a single row. e.g.:

.. code-block:: python

   import anvil.server
   from anvil.tables import app_tables


   @anvil.server.callable
   def get_book(title):
       return app_tables.book.get(title=title)


The server function's name must be the word `get` followed by the class name in snake case. If we had a class named `MyVeryInterestingThing`, we would need a server function named `get_my_very_interesting_thing`.

Often, we'll want to search for a set of data table rows that meet some criteria and create the resulting instances from the results. For that, we use the `search` method.

Let's assume the book table also has a `publisher` text column. To create a list of books published by O'Reilly we'd call `Book.search` on the client side:

.. code-block:: python

   books = Book.search(publisher="O'Reilly")

and, on the server side, we'd need a function named `search_book` that takes search criteria as arguments and returns a SearchIterator. e.g.:

.. code-block:: python

   import anvil.server
   from anvil.tables import app_tables


   @anvil.server.callable
   def search_book(*args, **kwargs):
       return app_tables.book.search(*args, **kwargs)

The server function name follows the same format as for `get` - it must be the word `search` followed by the class name in snake case.

Adding, Updating and Deleting
-----------------------------
There are also methods for sending changes to the server - adding new rows, updating and deleting existing rows.

To add a new book, create a Book instance client side and call its `add` method:

.. code-block:: python

   book = Book(title="JavaScript: The Definitive Guide")
   book.add()

on the server side, we need a `add_book` function that takes a dict of attribute values as its argument and returns the data table row it creates:

.. code-block:: python

   import anvil.server
   from anvil.tables import app_tables


   @anvil.server.callable
   def add_book(attrs):
       return app_tables.book.add_row(**attrs)


There are similar methods to update or delete an existing row. Let's create a new book, change its title and then delete it:

.. code-block:: python

   book = Book(title="My Wonderful Book")
   book.add()

   book.title = "My Not So Wonderful Book"
   book.update()

   book.delete()

As you change an object's attribute values, persistence keeps track of those changes. Calling `update` will send to the server the relevant data table row along with a dict of the changed attribute values. The dict does not contain any attribute whose value has remained unchanged from the underlying row.

So, on the server side, we need `update_book` and `delete_book` functions. The update function must take a data table row and a dict of attribute values as its arguments. The delete function must take a data table row. Neither function needs to return anything:

.. code-block:: python

   import anvil.server
   from anvil.tables import app_tables


   @anvil.server.callable
   def update_book(row, attrs):
       row.update(**attrs)


   @anvil.server.callable
   def delete_book(row):
       row.delete()

Any additional arguments passed to the `add`, `update` or `delete` methods will be passed to the relevant server function.

Caching
-------
Calling the `get` method will attempt to retrieve the matching object from a cache maintained by the persisted class. If there's no cached entry, the relevant server call is made and the resulting object added to the cache.

For the `search` method, the default behaviour is to clear the cache, add entries for each of the objects found and return a list of those results. This behaviour can be disabled by setting the `lazy` argument of the method to `True` whereby the cache is left unaltered and the method will instead return a generator of the objects found.

e.g. in our search example above, we used the default behaviour to return a list of books published by O'Reilly. If, instead, we wanted a generator of those books:

.. code-block:: python

   books = Book.search(lazy=True, publisher="O'Reilly")
