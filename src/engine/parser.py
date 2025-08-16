
"""Tiny SQL-like parser with simple comparison operators."""
import re
from typing import Dict, List, Tuple, Optional

def parse_create(sql: str):
    m = re.match(r"\s*CREATE\s+TABLE\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.+)\)\s*(INDEX\s*\((.+)\))?\s*;?\s*$", sql, re.I)
    if not m:
        raise SyntaxError("invalid CREATE TABLE syntax")
    name = m.group(1)
    cols = m.group(2)
    indexed = m.group(4)
    parts = [p.strip() for p in cols.split(",")]
    schema = {}
    for p in parts:
        mm = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\s+(INT|TEXT)", p, re.I)
        if not mm:
            raise SyntaxError(f"invalid column definition: {p}")
        col = mm.group(1)
        typ = mm.group(2).upper()
        schema[col] = typ
    idx_cols = []
    if indexed:
        idx_cols = [c.strip() for c in indexed.split(",")]
    return name, schema, idx_cols

def parse_insert(sql: str):
    m = re.match(r'\s*INSERT\s+INTO\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+VALUES\s*\((.+)\)\s*;?\s*$', sql, re.I)
    if not m:
        raise SyntaxError("invalid INSERT syntax")
    name = m.group(1)
    vals = m.group(2)
    parts = [p.strip() for p in re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', vals)]
    parsed = []
    for p in parts:
        if p.startswith('"') and p.endswith('"'):
            parsed.append(p[1:-1])
        elif p.startswith("'") and p.endswith("'"):
            parsed.append(p[1:-1])
        elif p.isdigit() or (p.startswith('-') and p[1:].isdigit()):
            parsed.append(int(p))
        else:
            parsed.append(p)
    return name, parsed

def parse_select(sql: str):
    m = re.match(r'\s*SELECT\s+\*\s+FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(WHERE\s+(.+))?\s*;?\s*$', sql, re.I)
    if not m:
        raise SyntaxError("invalid SELECT syntax")
    name = m.group(1)
    where = m.group(3)
    if not where:
        return name, None
    # support operators =, !=, <, >, <=, >=
    mw = re.match(r'\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(=|!=|<=|>=|<|>)\s*(.+)\s*$', where)
    if not mw:
        raise SyntaxError("only simple WHERE col <op> literal supported")
    col = mw.group(1)
    op = mw.group(2)
    val = mw.group(3).strip()
    if val.startswith('"') and val.endswith('"'):
        val = val[1:-1]
    elif val.startswith("'") and val.endswith("'"):
        val = val[1:-1]
    elif val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
        val = int(val)
    else:
        val = val
    return name, (col, op, val)
