import duckdb

# Connect to (or create) the DuckDB database file
con = duckdb.connect("ipl_data.duckdb")

# Load the CSV files into DuckDB tables
con.execute("CREATE TABLE deliveries AS SELECT * FROM read_csv_auto('deliveries.csv')")
con.execute("CREATE TABLE matches AS SELECT * FROM read_csv_auto('matches.csv')")

# Optionally, verify the tables by querying a few rows from each
print("Deliveries table preview:")
print(con.execute("SELECT * FROM deliveries LIMIT 5").fetchall())

print("\nMatches table preview:")
print(con.execute("SELECT * FROM matches LIMIT 5").fetchall())

# Close the connection
con.close()
