Pivot
=====
A pivot table component based on https://github.com/nicolaskruchten/pivottable

Properties
----------

:items: list of dicts

    The dataset to be pivoted

:rows: list of strings

    attribute names to prepopulate in rows area

:columns: list of strings

    attribute names to prepopulate in columns area

:values: list of strings

    attribute names to prepopulate in vals area (gets passed to aggregator generating function)

:aggregator: string

    aggregator to prepopulate in dropdown (e.g. "Count" or "Sum")
