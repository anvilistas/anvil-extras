# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.tables import app_tables

import marshmallow

anvil_to_marshmallow = {
    "bool": marshmallow.fields.Boolean,
    "date": marshmallow.fields.Date,
    "datetime": marshmallow.fields.DateTime,
    "number": marshmallow.fields.Number,
    "string": marshmallow.fields.Str,
}


def _exclusions_for_table(table_name, ignore_columns):
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


def schema_from_table(
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
    class
        A subclass of marshmallow.Schema
    """
    table = getattr(app_tables, table_name)
    exclusions = _exclusions_for_table(table_name, ignore_columns)
    if linked_tables is None:
        linked_tables = {}

    schema_definition = {
        column["name"]: anvil_to_marshmallow[column["type"]]()
        for column in table.list_columns()
        if column["type"] != "liveObject" and column["name"] not in exclusions
    }

    if table_name in linked_tables:
        linked_schema_definition = {
            column: schema_from_table(
                linked_table, ignore_columns, linked_tables, with_id
            )
            for column, linked_table in linked_tables[table_name].items()
        }
        schema_definition = {**schema_definition, **linked_schema_definition}

    if with_id:
        schema_definition["_id"] = marshmallow.fields.Function(lambda row: row.get_id())

    return marshmallow.Schema.from_dict(schema_definition)
