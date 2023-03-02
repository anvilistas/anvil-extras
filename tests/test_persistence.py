# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas
import pytest

from client_code import persistence as ps

__version__ = "0.0.1"


@pytest.fixture
def book_store():
    return {"title": "Fluent Python", "author": {"name": "Luciano Ramalho"}}


@pytest.fixture
def book(book_store):
    """A class that behaves like a persisted class without actually being one"""

    class Book:
        _store = book_store
        _delta = {}
        author_name = ps.LinkedAttribute(linked_column="author", linked_attr="name")

    return Book()


@pytest.fixture
def persisted_book():
    """An ordinary persisted class"""

    @ps.persisted_class
    class Book:
        author_name = ps.LinkedAttribute(linked_column="author", linked_attr="name")

    return Book()


@pytest.fixture
def customised_book():
    """A persisted class with a standard crud method overridden"""

    @ps.persisted_class
    class Book:
        author_name = ps.LinkedAttribute(linked_column="author", linked_attr="name")

        def save(self):
            return "customised save"

    return Book()


@pytest.fixture
def linked_persisted_book(book_store):
    """A persisted class with a linked class attribute"""

    @ps.persisted_class
    class Author:
        pass

    @ps.persisted_class
    class Book:
        author = Author

    return Book(book_store)


def test_linked_attribute(book, book_store):
    """Test that the LinkedAttribute class works independently of persisted_class"""
    assert book.author_name == "Luciano Ramalho"
    book.author_name = "Luciano"
    assert book._delta["author_name"] == "Luciano"
    assert book._store == book_store
    assert book.author_name == "Luciano"


def test_linked_attribute_name_clash():
    with pytest.raises(RuntimeError) as excinfo:

        class Book:
            author = ps.LinkedAttribute(linked_column="author", linked_attr="name")

    assert "Error calling __set_name__" in str(excinfo.value)


def test_persisted_class_attributes(persisted_book, book_store):
    """Test that persisted class attributes behave as expected"""
    persisted_book._store = book_store
    assert persisted_book.title == "Fluent Python"
    assert persisted_book.author_name == "Luciano Ramalho"
    persisted_book.title = "Changed Title"
    persisted_book.author_name = "Luciano"
    assert persisted_book._delta["title"] == "Changed Title"
    assert persisted_book._delta["author_name"] == "Luciano"
    assert persisted_book._store == book_store
    assert persisted_book.title == "Changed Title"
    assert persisted_book.author_name == "Luciano"


def test_persisted_class_indexing(persisted_book, book_store):
    """Test that persisted class also works with index access"""
    persisted_book._store = book_store
    assert persisted_book["title"] == "Fluent Python"
    assert persisted_book["author_name"] == "Luciano Ramalho"
    persisted_book["title"] = "Changed Title"
    persisted_book["author_name"] = "Luciano"
    assert persisted_book._delta["title"] == "Changed Title"
    assert persisted_book._delta["author_name"] == "Luciano"
    assert persisted_book._store == book_store
    assert persisted_book["title"] == "Changed Title"
    assert persisted_book["author_name"] == "Luciano"


def test_default_server_functions(persisted_book):
    """Test that crud methods are added to a persisted class"""
    for key in ["search", "get", "update", "delete"]:
        assert hasattr(persisted_book, key)


def test_customised_book(customised_book):
    """Test that overriding a crud method behaves as expected"""
    for key in ["get", "save", "delete"]:
        assert hasattr(customised_book, key)

    assert customised_book.save() == "customised save"


def test_linked_class(linked_persisted_book):
    """Test that linked classes behave as expected"""
    assert linked_persisted_book.title == "Fluent Python"
    assert linked_persisted_book.author.name == "Luciano Ramalho"


def test_linked_class_set(linked_persisted_book):
    """Test that attempting to change a linked class instance raises an error"""
    with pytest.raises(AttributeError) as excinfo:
        linked_persisted_book.author = "test"

    assert "Linked Class instance is already set" in str(excinfo.value)


def test_non_attributes_in_local_store(persisted_book):
    assert persisted_book.foo is None
    assert persisted_book["foo"] is None
