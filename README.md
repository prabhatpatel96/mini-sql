# Mini-SQL Database Engine  

A lightweight, custom-built **SQL engine** developed in Python to mimic the core functionality of relational database systems.  
This project demonstrates database internals such as parsing, query execution, and indexing — built completely from scratch without external database libraries.  

---

## 🚀 Features  
- 🛠 **Custom SQL Parser** – Supports basic SQL commands (`CREATE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`).  
- 📂 **Table Management** – Create and store tables with schema definitions.  
- ⚡ **Query Execution Engine** – Handles simple queries on structured data.  
- 📑 **Indexing Support** – Implements indexing for faster query lookups.  
- 🧪 **Lightweight & Educational** – Designed to understand DBMS fundamentals without heavy dependencies.  

---

## 📖 Example Usage  

```python
from mini_sql import MiniSQL

# Initialize database engine
db = MiniSQL()

# Create table
db.execute("CREATE TABLE students (id INT, name TEXT, grade FLOAT);")

# Insert data
db.execute("INSERT INTO students VALUES (1, 'Alice', 9.1);")
db.execute("INSERT INTO students VALUES (2, 'Bob', 8.7);")

# Query data
results = db.execute("SELECT * FROM students;")
print(results)
# Output: [(1, 'Alice', 9.1), (2, 'Bob', 8.7)]



#project structure
mini_sql/
│── mini_sql/          # Core implementation files
│   ├── parser.py      # SQL command parser
│   ├── engine.py      # Query execution logic
│   ├── storage.py     # Table/data storage management
│   └── __init__.py
│
│── examples/          # Example usage scripts
│── tests/             # Unit tests
│── README.md          # Project documentation
│── requirements.txt   # Dependencies (if any)



# make clone in your PC
git clone https://github.com/<your-username>/mini-sql.git
cd mini-sql


