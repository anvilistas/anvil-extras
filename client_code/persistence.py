# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import anvil.server

__version__ = "2.2.3"


def _snakify(text):
    return "".join("_" + c.lower() if c.isupper() else c for c in text).lstrip("_")


class LinkedAttribute:
    """A descriptor class for adding linked table items as attributes

    For a class backed by a data tables row, this class is used to dyamically add
    linked table items as attributes to the parent object.
    """

    def __init__(self, linked_column, linked_attr):
        """
        Parameters
        ----------
        linked_column: str
            The name of the column in the row object which links to another table
        linked_attr: str
            The name of the column in the linked table which contains the required
            value
        """
        self._linked_column = linked_column
        self._linked_attr = linked_attr

    def __set_name__(self, owner, name):
        if name == self._linked_column:
            raise ValueError(
                "Attribute name cannot be the same as the linked column name"
            )
        self._name = name

    def __get__(self, instance, objtype=None):
        if instance is None:
            return self

        if instance._delta:
            return instance._delta[self._name]

        if not instance._store:
            return None

        return instance._store[self._linked_column][self._linked_attr]

    def __set__(self, instance, value):
        instance._delta[self._name] = value


class LinkedClass:
    "A descriptor class for adding objects based on linked tables as attributes"

    def __init__(self, cls, *args, linked_column=None, **kwargs):
        self._linked_column = linked_column
        self._cls = cls
        self._args = args or []
        self._kwargs = kwargs or {}

    def __get__(self, instance, objtype=None):
        if instance is None:
            return self

        return self._cls(
            instance._store[self._linked_column], *self._args, **self._kwargs
        )

    def __set__(self, instance, value):
        raise AttributeError(
            "Linked Class instance is already set and cannot be changed"
        )


class PersistedClass:
    key = None

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._snake_name = _snakify(cls.__name__)
        cls._cache = {}
        for attr, value in cls.__dict__.items():
            try:
                is_persisted_class = issubclass(value, PersistedClass)
            except TypeError:
                is_persisted_class = False

            if is_persisted_class:
                setattr(cls, attr, LinkedClass(cls=value, linked_column=attr))

    @classmethod
    def search(cls, lazy=False, *args, **kwargs):
        rows = anvil.server.call(f"search_{cls._snake_name}", *args, **kwargs)
        if lazy:
            return (cls(store=row) for row in rows)

        result = [cls(store=row) for row in rows]
        cls._cache.clear()
        for obj in result:
            cls._cache[getattr(obj, cls.key)] = obj
        return result

    @classmethod
    def get(cls, key):
        try:
            return cls._cache[key]
        except KeyError:
            row = anvil.server.call(f"get_{cls._snake_name}", {cls.key: key})
            obj = cls(store=row)
            cls._cache[key] = obj
            return obj

    def __init__(self, store=None, *args, **kwargs):
        self._store = store or {}
        self._delta = {}

    def __getattr__(self, key):
        if self._delta and key in self._delta:
            return self._delta[key]

        # if the _store raises a KeyError
        # we aren't yet backed by a row object
        # so return None
        try:
            return self._store[key]
        except KeyError:
            return None

    def __getitem__(self, key):
        return getattr(self, key)

    def __setattr__(self, key, value):
        is_private = key.startswith("_")
        is_descriptor = hasattr(self.__class__, key) and hasattr(
            getattr(self.__class__, key), "__set__"
        )
        if is_private or is_descriptor:
            object.__setattr__(self, key, value)
        else:
            self._delta[key] = value

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def add(self, *args, **kwargs):
        self._store = anvil.server.call(
            f"add_{self._snake_name}", self._delta, *args, **kwargs
        )
        self._delta.clear()

    def update(self, *args, **kwargs):
        anvil.server.call(
            f"update_{self._snake_name}", self._store, self._delta, *args, **kwargs
        )
        self._delta.clear()

    def delete(self, *args, **kwargs):
        anvil.server.call(f"delete_{self._snake_name}", self._store, *args, **kwargs)
        self._delta.clear()


def persisted_class(cls):
    """A decorator for a class with a persistence mechanism"""
    return type(cls.__name__, (PersistedClass,), cls.__dict__.copy())
