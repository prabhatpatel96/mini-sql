
"""Executor connecting parser and storage with operator support."""
from . import storage, parser
from typing import Any, Dict, List

def create_table(sql: str):
    name, schema, idx_cols = parser.parse_create(sql)
    storage.create_table(name, schema, idx_cols)
    return f"Table `{name}` created with columns {list(schema.keys())} and indexes {idx_cols}"

def insert(sql: str):
    name, values = parser.parse_insert(sql)
    meta = storage.load_meta(name)
    schema = meta["schema"]
    cols = list(schema.keys())
    if len(values) != len(cols):
        raise ValueError("column count mismatch")
    row = {}
    for c, v in zip(cols, values):
        typ = schema[c]
        if typ == "INT":
            if isinstance(v, int):
                row[c] = v
            else:
                try:
                    row[c] = int(v)
                except:
                    raise ValueError(f"cannot cast {v} to INT for column {c}")
        else:
            row[c] = str(v)
    lineno = storage.append_row(name, row)
    for col in meta.get("indexed", []):
        if col in row:
            storage.update_index_on_insert(name, col, row[col], lineno)
    return f"1 row inserted into `{name}` (line {lineno})"

def _compare(a, op, b):
    if a is None:
        return False
    try:
        if op == "=":
            return a == b
        if op == "!=":
            return a != b
        if op == "<":
            return a < b
        if op == ">":
            return a > b
        if op == "<=":
            return a <= b
        if op == ">=":
            return a >= b
    except TypeError:
        return False
    return False

def select(sql: str):
    name, where = parser.parse_select(sql)
    meta = storage.load_meta(name)
    if where is None:
        results = [row for _, row in storage.full_scan(name)]
        return results
    col, op, val = where
    # if equality and index exists, use it
    if op == "=" and col in meta.get("indexed", []):
        linenos = storage.lookup_index(name, col, val)
        return [storage.read_row_at(name, ln) for ln in linenos]
    # otherwise scan and filter using _compare
    res = []
    for _, row in storage.full_scan(name):
        if _compare(row.get(col), op, val):
            res.append(row)
    return res
