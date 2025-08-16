
"""Storage manager for mini-sql."""
import os, json
from typing import Dict, List, Optional

DB_DIR = os.path.join(os.getcwd(), "data")  # defaults to ./data

def ensure_db_dir():
    os.makedirs(DB_DIR, exist_ok=True)

def meta_path(table: str) -> str:
    return os.path.join(DB_DIR, f"{table}.meta.json")

def data_path(table: str) -> str:
    return os.path.join(DB_DIR, f"{table}.data.jsonl")

def index_path(table: str, col: str) -> str:
    return os.path.join(DB_DIR, f"{table}.{col}.index.json")

def create_table(table: str, schema: Dict[str, str], indexed: Optional[List[str]]=None):
    ensure_db_dir()
    if indexed is None:
        indexed = []
    meta = {"table": table, "schema": schema, "indexed": indexed, "rows": 0}
    with open(meta_path(table), "w", encoding="utf-8") as f:
        json.dump(meta, f)
    open(data_path(table), "a").close()
    for col in indexed:
        with open(index_path(table, col), "w", encoding="utf-8") as f:
            json.dump({}, f)

def load_meta(table: str):
    with open(meta_path(table), "r", encoding="utf-8") as f:
        return json.load(f)

def append_row(table: str, row: Dict[str, object]):
    ensure_db_dir()
    dp = data_path(table)
    with open(dp, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, separators=(",", ":")) + "\n")
    meta = load_meta(table)
    meta["rows"] += 1
    with open(meta_path(table), "w", encoding="utf-8") as f:
        json.dump(meta, f)
    return meta["rows"] - 1

def read_row_at(table: str, lineno: int):
    dp = data_path(table)
    with open(dp, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == lineno:
                return json.loads(line.strip())
    raise IndexError("line number out of range")

def full_scan(table: str):
    dp = data_path(table)
    if not os.path.exists(dp):
        return
    with open(dp, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line.strip():
                yield i, json.loads(line.strip())

def ensure_index(table: str, col: str):
    ensure_db_dir()
    ip = index_path(table, col)
    if os.path.exists(ip):
        return
    index = {}
    for lineno, row in full_scan(table):
        key = row.get(col)
        if key is None:
            continue
        index.setdefault(str(key), []).append(lineno)
    with open(ip, "w", encoding="utf-8") as f:
        json.dump(index, f)

def update_index_on_insert(table: str, col: str, value, lineno: int):
    ip = index_path(table, col)
    if not os.path.exists(ip):
        ensure_index(table, col)
    with open(ip, "r", encoding="utf-8") as f:
        index = json.load(f)
    index.setdefault(str(value), []).append(lineno)
    with open(ip, "w", encoding="utf-8") as f:
        json.dump(index, f)

def lookup_index(table: str, col: str, value):
    ip = index_path(table, col)
    if not os.path.exists(ip):
        return []
    with open(ip, "r", encoding="utf-8") as f:
        index = json.load(f)
    return index.get(str(value), [])
