import sqlite3

connect = sqlite3.connect("database.db")
c = connect.cursor()

c.execute("""

    DROP TABLE IF EXISTS tasks
          
""")

c.execute("""
          
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        completed BOOLEAN DEFAULT 0
    )
""")

connect.commit()
connect.close()
