import os
import json
import pyodbc
from glob import glob

def push_jsonl_to_ssms():
    # Step 1: Find the most recent enriched JSONL file in the output directory
    output_dir = "output"
    # only pick enriched files
    json_files = [
        f for f in glob(os.path.join(output_dir, "*.jsonl"))
        if os.path.basename(f).startswith("Enriched_Result_")
    ]
    if not json_files:
        raise FileNotFoundError("No enriched JSONL files found in the output directory.")

    latest_file = max(json_files, key=os.path.getctime) # Pick the most recently modified file
    print(f"Using latest enriched file: {latest_file}")

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

        # Step 4: Insert each job record into the SQL Server table (normalized version)
        inserted, failed = 0, 0
        for record in data:
            try:
                # --- Company ---
                # Check if the company already exists in the Company table
                cursor.execute("SELECT Company_id FROM Company WHERE name = ?", record.get('Company', '').strip())
                row = cursor.fetchone()
                # If found, reuse its existing ID (avoid duplicates & wasted IDs)
                if row:
                    company_id = row[0]
                # If not found, insert it and get the new ID
                else:
                    cursor.execute("INSERT INTO Company (name) VALUES (?)", record.get('Company', '').strip())
                    # SCOPE_IDENTITY() returns the last identity value inserted in this session
                    cursor.execute("SELECT SCOPE_IDENTITY()")
                    company_id = cursor.fetchone()[0]

                # --- Category ---
                cursor.execute("SELECT Category_id FROM Category WHERE category = ?",
                               record.get('Category', '').strip())
                row = cursor.fetchone()
                if row:
                    category_id = row[0]
                else:
                    cursor.execute("INSERT INTO Category (category) VALUES (?)", record.get('Category', '').strip())
                    cursor.execute("SELECT SCOPE_IDENTITY()")
                    category_id = cursor.fetchone()[0]

                # --- citizenPR ---
                cursor.execute("SELECT CitizenPR_id FROM CitizenPR WHERE CitizenPR = ?",
                               record.get('CitizenPR', '').strip())
                row = cursor.fetchone()
                if row:
                    citizenPR_id = row[0]
                else:
                    cursor.execute("INSERT INTO citizenPR (citizenPR) VALUES (?)", record.get('CitizenPR', '').strip())
                    cursor.execute("SELECT SCOPE_IDENTITY()")
                    citizenPR_id = cursor.fetchone()[0]

                # --- Insert Job ---
                cursor.execute(f"""
                    INSERT INTO {table} (JobTitle, Location, Skills, Years, Link, Company_id, Category_id, CitizenPR_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                               record.get('Job_title', '').strip(),
                               record.get('Location', '').strip(),
                               record.get('Skills', '').strip(),
                               record.get('Years', '').strip(),
                               record.get('Link', '').strip(),
                               company_id,
                               category_id,
                               citizenPR_id
                               )
                inserted += 1
            except Exception as e:
                failed += 1
                print(f"Row insert failed for Job_title={record.get('Job_title')}: {e}")
        # Commit changes
        conn.commit()
        print(f"Inserted {inserted} rows into SSMS successfully. Failed: {failed}")
    except Exception as e:
        print(f"---Enriched data was not inserted into SSMS successfully---. {e}")
    # Clean up safely
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
                conn.close()

if __name__ == "__main__":
    push_jsonl_to_ssms()