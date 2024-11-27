# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas
import pytest

from client_code import persistence as ps

__version__ = "2.2.2"


@pytest.fixture
def book_store():
    return {"title": "Fluent Python", "author": {"name": "Luciano Ramalho"}}


@pytest.fixture
def book(book_store):
    """A class that behaves like a persisted class without actually being one"""

    class Book:
        _store = book_store
        _delta = {}

    return Book()


@pytest.fixture
def persisted_book():
    """An ordinary persisted class"""

    @ps.persisted_class
    class Book:
        pass

    return Book()


@pytest.fixture
def customised_book():
    """A persisted class with a standard crud method overridden"""

    @ps.persisted_class
    class Book:
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


@pytest.fixture
def linked_persisted_book_without_author():
    """A persisted class with a linked class attribute

    instantiated without an author
    """

    @ps.persisted_class
    class Author:
        pass

    @ps.persisted_class
    class Book:
        author = Author

    store = {"title": "Fluent Python", "author": None}

    return Book(store)


@pytest.fixture
def douglas_adams():
    @ps.persisted_class
    class Author:
        pass

    return Author({"name": "Douglas Adams"})


def test_persisted_class_attributes(persisted_book, book_store):
    """Test that persisted class attributes behave as expected"""
    persisted_book._store = book_store
    assert persisted_book.title == "Fluent Python"
    persisted_book.title = "Changed Title"
    assert persisted_book._delta["title"] == "Changed Title"
    assert persisted_book._store == book_store
    assert persisted_book.title == "Changed Title"


def test_persisted_class_indexing(persisted_book, book_store):
    """Test that persisted class also works with index access"""
    persisted_book._store = book_store
    assert persisted_book["title"] == "Fluent Python"
    persisted_book["title"] = "Changed Title"
    assert persisted_book._delta["title"] == "Changed Title"
    assert persisted_book._store == book_store
    assert persisted_book["title"] == "Changed Title"


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


def test_linked_class_set(linked_persisted_book, douglas_adams):
    """Test that changing a linked class instance behaves as expected"""
    linked_persisted_book.author = douglas_adams
    assert linked_persisted_book.author.name == "Douglas Adams"


def test_linked_class_set_none(linked_persisted_book_without_author):
    """Test that linked classes can be set to None"""
    assert linked_persisted_book_without_author.author is None


def test_linked_class_change_none(linked_persisted_book):
    """Test that linked classes can be set to None"""
    linked_persisted_book.author = None
    assert linked_persisted_book.author is None


def test_non_attributes_in_local_store(persisted_book):
    assert persisted_book.foo is None
    assert persisted_book["foo"] is None
