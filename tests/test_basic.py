
import os, shutil
from src.engine import storage, executor

def setup_function(fn):
    d = os.path.join(os.getcwd(), "data")
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d, exist_ok=True)

def test_create_insert_select_and_ops():
    executor.create_table('CREATE TABLE users (id INT, name TEXT) INDEX(id);')
    executor.insert('INSERT INTO users VALUES (1, "Alice");')
    executor.insert('INSERT INTO users VALUES (2, "Bob");')
    executor.insert("INSERT INTO users VALUES (3, 'Carol');")
    res = executor.select('SELECT * FROM users WHERE id = 2;')
    assert len(res) == 1 and res[0]["name"] == "Bob"
    res2 = executor.select('SELECT * FROM users WHERE id > 1;')
    assert len(res2) == 2
    res3 = executor.select('SELECT * FROM users WHERE name != "Bob";')
    assert len(res3) == 2
