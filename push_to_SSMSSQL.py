import os
import json
import pyodbc
from glob import glob

def push_jsonl_to_ssms():
    # Step 1: Find the most recent JSONL file in the output directory
    output_dir = "output"
    json_files = glob(os.path.join(output_dir, "*.jsonl")) # Get all .jsonl files in the output dir
    if not json_files:
        raise FileNotFoundError("No JSON files found in the output directory.")

    latest_file = max(json_files, key=os.path.getctime) # Pick the most recently modified file
    print(f"Using latest file: {latest_file}")

    # Step 2: Setup SQL Server connection details
    server = 'LAPTOP-FLIH4Q2E' # Replace with your actual SQL Server name
    # name of the DB in SSMS
    database = 'JobInSaskatchewanCrawlerDB'
    table = 'JobListings'

    # Connection string to connect with SQL Server using Windows Authentication
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )

    # Establish the connection and create a cursor
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Clear the table and reset IDENTITY to 1
    # If your table ever has foreign key constraints, TRUNCATE won’t work — then you’d have to use DELETE + DBCC CHECKIDENT.
    cursor.execute(f"TRUNCATE TABLE {table}")

    # Step 3: Load and parse JSONL file (one JSON object per line)
    with open(latest_file, encoding='utf-8') as f:
        data = [json.loads(line) for line in f] # Read and decode each JSON line into a dictionary

    # Step 4: Insert each job record into the SQL Server table
    for record in data:
        cursor.execute(f"""
            INSERT INTO {table} (Company, JobTitle, Location, Link)
            VALUES (?, ?, ?, ?)
        """, record['Company'], record['Job_title'], record['Location'], record['Link'])

    # Commit changes and clean up
    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted into SSMS successfully.")
