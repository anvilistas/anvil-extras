# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.tables import app_tables

from . import lazy_module_loader as lazy

__version__ = "2.7.0"

LINKED_COLUMN_TYPES = ("liveObject", "liveObjectArray", "link_single", "link_multiple")
LO, LOA, LS, LM = LINKED_COLUMN_TYPES
FIELD_TYPES = None


def _get_field_types():
    global FIELD_TYPES
    if FIELD_TYPES is None:
        mm = lazy.marshmallow
        FIELD_TYPES = {
            "bool": mm.fields.Boolean,
            "date": mm.fields.Raw,
            "datetime": mm.fields.Raw,
            "number": mm.fields.Number,
            "string": mm.fields.Str,
            "simpleObject": mm.fields.Raw,
            "media": mm.fields.Raw,
        }
    return FIELD_TYPES


def _exclusions(table_name, ignore_columns):
    """Generate a list of columns to exclude from serialisation for a given table name

    Parameters
    ----------
    table_name : str
        The name of a data table within the app
    ignore_columns :  list, tuple, dict or str
        A list or tuple of column names to ignore, a dict mapping
        table names to such lists or tuples, or a string with a single column name

    Returns
    -------
    list
      of column names
    """
    if isinstance(ignore_columns, (list, tuple)):
        return ignore_columns
    elif isinstance(ignore_columns, dict):
        if table_name in ignore_columns.keys():
            return ignore_columns[table_name]
        else:
            return []
    elif isinstance(ignore_columns, str):
        return [ignore_columns]
    else:
        return []


def _link_columns(columns):
    """Generate a dict mapping linked column types to sets of column names

    Parameters
    ----------
    columns : list
        of the form return by table.list_columns()

    Returns
    -------
    dict

        e.g. For a table with two linked columns, 'link1' and link2' plus a multi-link
        column, 'multilink', this would return:

        {"liveObject": {"link1", "link2"}, "liveObjectArray": {"multilink"}}
    """
    rv = {
        field_type: {c["name"] for c in columns if c["type"] == field_type}
        for field_type in LINKED_COLUMN_TYPES
    }
    rv[LS] |= rv[LO]
    rv[LM] |= rv[LOA]
    return rv


def _basic_schema_definition(table_name, columns, ignore_columns, with_id):
    """
    Parameters
    ----------
    table_name : str
        The name of a data table within the app
    columns : dict
        mapping table names to column lists as generated by _columns
    ignore_columns :  list, tuple, dict or str
        A list or tuple of column names to ignore, a dict mapping
        table names to such lists or tuples, or a string with a single column name
    with_id : boolean
        whether the internal anvil id should be included in the serialised output
    """
    mm = lazy.marshmallow
    field_types = _get_field_types()
    exclusions = _exclusions(table_name, ignore_columns)
    try:
        result = {
            column["name"]: field_types[column["type"]]()
            for column in columns[table_name]
            if column["type"] not in LINKED_COLUMN_TYPES
            and column["name"] not in exclusions
        }
    except KeyError as e:
        raise ValueError(f"{e} columns are not supported")
    if with_id:
        result["_id"] = mm.fields.Function(lambda row: row.get_id())
    return result


def _schema_definition(table_name, columns, ignore_columns, linked_tables, with_id):
    """A recursive function to generate a dict for passing to mm.Schema.from_dict

    Parameters
    ----------
    table_name : str
        The name of a data table within the app
    columns : dict
        mapping table names to column lists as generated by _columns
    ignore_columns :  list, tuple, dict or str
        A list or tuple of column names to ignore, a dict mapping
        table names to such lists or tuples, or a string with a single column name
    linked_tables : dict
        mapping a table name to a dict which, in turn, maps a column name to a linked
        table name
    with_id : boolean
        whether the internal anvil id should be included in the serialised output

    Returns
    -------
    dict
    """
    mm = lazy.marshmallow
    result = _basic_schema_definition(table_name, columns, ignore_columns, with_id)
    if table_name in linked_tables:
        link_columns = _link_columns(columns[table_name])
        linked = {
            column: mm.fields.Nested(
                mm.Schema.from_dict(
                    _schema_definition(
                        linked_table, columns, ignore_columns, linked_tables, with_id
                    )
                )
            )
            for column, linked_table in linked_tables[table_name].items()
            if column in link_columns[LS]
        }
        multilinked = {
            column: mm.fields.List(
                mm.fields.Nested(
                    mm.Schema.from_dict(
                        _schema_definition(
                            linked_table,
                            columns,
                            ignore_columns,
                            linked_tables,
                            with_id,
                        )
                    )
                )
            )
            for column, linked_table in linked_tables[table_name].items()
            if column in link_columns[LM]
        }
        result = {
            **result,
            **linked,
            **multilinked,
        }
    return result


# The following functions hit the data tables service and thus have no tests.
def _columns(table_name, linked_tables):
    """Generate a dict mapping table names to column lists

    For the given table and each table found in the linked_tables dict.

    Parameters
    ----------
    table_name : str
        The name of a data table within the app
    linked_tables : dict
        mapping a table name to a dict which, in turn, maps a column name to a linked
        table name

    Returns
    -------
    dict
    """
    tables = {table_name}.union(
        {table for link in linked_tables.values() for table in link.values()}
    )
    return {table: getattr(app_tables, table).list_columns() for table in tables}


def datatable_schema(
    table_name, ignore_columns=None, linked_tables=None, with_id=False
):
    """Generate a marshmallow Schema dynamically from a table name

    Parameters
    ----------
    table_name : str
        The name of a data table within the app
    ignore_columns :  list, tuple, dict or str
        A list or tuple of column names to ignore, a dict mapping
        table names to such lists or tuples, or a string with a single column name
    linked_tables : dict
        mapping a table name to a dict which, in turn, maps a column name to a linked
        table name
    with_id : boolean
        whether the internal anvil id should be included in the serialised output

    Returns
    -------
    marshmallow.Schema
    """
    mm = lazy.marshmallow
    if linked_tables is None:
        linked_tables = {}
    columns = _columns(table_name, linked_tables)
    schema_definition = _schema_definition(
        table_name, columns, ignore_columns, linked_tables, with_id
    )
    return mm.Schema.from_dict(schema_definition)()
