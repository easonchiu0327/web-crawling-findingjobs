import os
import json
import pyodbc
from glob import glob

def push_jsonl_to_ssms():
    # Step 1: Find the most recent JSONL file in the output directory
    output_dir = "output"
    json_files = glob(os.path.join(output_dir, "*.jsonl")) # Get all .jsonl files in the output dir
    if not json_files:
        raise FileNotFoundError("No JSONL files found in the output directory.")

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
    conn = None
    cursor = None

    try:
        # Establish the connection and create a cursor
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.fast_executemany = True  # small perf boost for executemany

        # Clear the table and reset IDENTITY to 1
        # If your table ever has foreign key constraints, TRUNCATE won’t work — then you’d have to use DELETE + DBCC CHECKIDENT.
        try:
            cursor.execute(f"TRUNCATE TABLE {table}")
        except pyodbc.Error as e:
            print(f"TRUNCATE failed ({e}); falling back to DELETE + reseed.")
            cursor.execute(f"DELETE FROM {table}")
            # Reseed identity to 1 (only if table has IDENTITY)
            try:
                cursor.execute(f"DBCC CHECKIDENT ('{table}', RESEED, 0)")
            except pyodbc.Error:
                # Ignore if table has no identity column
                pass

        # Step 3: Load and parse JSONL file (one JSON object per line)
        with open(latest_file, encoding='utf-8') as f:
            data = [json.loads(line) for line in f if line.strip()] # Read and decode each JSON line into a dictionary

        # Step 4: Insert each job record into the SQL Server table
        for record in data:
            cursor.execute(f"""
                INSERT INTO {table} (Company, JobTitle, Location, Link, Category, Skills, Years, CitizenPR)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            record.get('Company'),
                    record.get('Job_title'),
                    record.get('Location'),
                    record.get('Link'),
                    record.get('Category'),
                    record.get('Skills'),
                    record.get('Years'),
                    record.get('CitizenPR')
            )
        # Commit changes
        conn.commit()
        print("Enriched data has been inserted into SSMS successfully.")
    except Exception as e:
        print(f"Enriched data was not inserted into SSMS successfully. {e}")
    # Clean up safely
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
                conn.close()

