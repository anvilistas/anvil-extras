# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.tables import app_tables

import marshmallow

__version__ = "1.8.1"

anvil_to_marshmallow = {
    "bool": marshmallow.fields.Boolean,
    "date": marshmallow.fields.Raw,
    "datetime": marshmallow.fields.Raw,
    "number": marshmallow.fields.Number,
    "string": marshmallow.fields.Str,
    "simpleObject": marshmallow.fields.Raw,
    "media": marshmallow.fields.Raw,
}


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
        return ignore_columns[table_name]
    elif isinstance(ignore_columns, str):
        return [ignore_columns]
    else:
        return []


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
    table = getattr(app_tables, table_name)
    columns = table.list_columns()
    exclusions = _exclusions(table_name, ignore_columns)
    if linked_tables is None:
        linked_tables = {}

    try:
        schema_definition = {
            column["name"]: anvil_to_marshmallow[column["type"]]()
            for column in columns
            if column["type"] not in ("liveObject", "liveObjectArray")
            and column["name"] not in exclusions
        }
    except KeyError as e:
        raise ValueError(f"{e} columns are not supported")

    if table_name in linked_tables:
        link_columns = [c["name"] for c in columns if c["type"] == "liveObject"]
        linked_schema_definition = {
            column: marshmallow.fields.Nested(
                datatable_schema(linked_table, ignore_columns, linked_tables, with_id)
            )
            for column, linked_table in linked_tables[table_name].items()
            if column in link_columns
        }
        multilink_columns = [
            c["name"] for c in columns if c["type"] == "liveObjectArray"
        ]
        multilink_schema_definition = {
            column: marshmallow.fields.List(
                marshmallow.fields.Nested(
                    datatable_schema(
                        linked_table, ignore_columns, linked_tables, with_id
                    )
                )
            )
            for column, linked_table in linked_tables[table_name].items()
            if column in multilink_columns
        }
        schema_definition = {
            **schema_definition,
            **linked_schema_definition,
            **multilink_schema_definition,
        }

    if with_id:
        schema_definition["_id"] = marshmallow.fields.Function(lambda row: row.get_id())

    return marshmallow.Schema.from_dict(schema_definition)()
