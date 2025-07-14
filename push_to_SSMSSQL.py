import os
import json
import pyodbc
from glob import glob

def push_json_to_ssms():
    # Step 1: Find the most recent JSON file
    output_dir = "output"
    json_files = glob(os.path.join(output_dir, "*.jsonl"))
    if not json_files:
        raise FileNotFoundError("No JSON files found in the output directory.")

    latest_file = max(json_files, key=os.path.getctime)
    print(f"Using latest file: {latest_file}")

    # Step 2: Setup SQL Server connection
    server = 'LAPTOP-FLIH4Q2E'
    database = 'JobInSaskatchewanCrawlerDB'
    table = 'JobListings'

    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    # Clear the table and reset IDENTITY to 1
    # If your table ever has foreign key constraints, TRUNCATE won’t work — then you’d have to use DELETE + DBCC CHECKIDENT.
    cursor.execute(f"TRUNCATE TABLE {table}")

    # Step 3: Load and insert JSON data
    with open(latest_file, encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    for record in data:
        cursor.execute(f"""
            INSERT INTO {table} (Company, JobTitle, Location, Link)
            VALUES (?, ?, ?, ?)
        """, record['Company'], record['Job_title'], record['Location'], record['Link'])

    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted into SSMS successfully.")
