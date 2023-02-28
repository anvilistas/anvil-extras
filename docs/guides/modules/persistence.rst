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


Methods and Server Functions
----------------------------
Each persisted class will have methods `add`, `update` and `delete` as well as
a classmethods `get` and `search`. Each of these will expect a matching server function to exist.

The server functions should be named with the relevant method followed by the persisted
class name in snake case.

For example, the `Book` class in the example above would require the following server
functions in order to operate fully:

.. code-block:: python

   import anvil.server

   @anvil.server.callable
   def search_book(*args, **kwargs):
       ...

    @anvil.server.callable
    def get_book(title):
        ...

    @anvil.server.callable
    def add_book(delta):
        ...

    @anvil.server.callable
    def update_book(row, delta):
        ...

    @anvil.server.callable
    def delete_book(row):
        ...

Where `row` will be the relevant data table row and `delta` will be a dict of attribute
names and values that have changed.

Any other args and kwargs passed to the persisted class methods will be passed to the
relevant server function.

Caching
-------
Calling the `get` method will attempt to retrieve the matching object from a cache maintained by the persisted class. If there's no cached entry, the relevant server call is made and the resulting object added to the cache.

For the `search` method, the default behaviour is to clear the cache, add entries for each of the objects found and return a list of those results. This behaviour can be disabled by setting the `lazy` argument of the method to `True` whereby the cache is left unaltered and the method will instead return a generator of the objects found.
