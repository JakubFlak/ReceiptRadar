import duckdb

con = duckdb.connect("data/warehouse.duckdb")

result = con.execute("SELECT 1").fetchall()
print(result)