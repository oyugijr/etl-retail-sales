import duckdb

con = duckdb.connect("salesdb.duckdb")
print(con.execute("SHOW TABLES").fetchall())