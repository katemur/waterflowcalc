import sqlite3
n = input("N:")
db= sqlite3.connect("tables.db")
results = db.execute("SELECT alpha FROM b2 ORDER BY ABS(793 - np) LIMIT 2;")
print(results)
