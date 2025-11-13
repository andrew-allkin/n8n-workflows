import psycopg2
import openpyxl

# Database connection details
conn = psycopg2.connect(
    host="localhost",
    database="n8n_workflows_data",
    user="admin",
    password="adminpassword",
    port="5432"
)

cur = conn.cursor()

# Drop and recreate table
print("Dropping existing table if exists...")
cur.execute("DROP TABLE IF EXISTS sender_label_mapping")

print("Creating sender_label_mapping table...")
cur.execute("""
    CREATE TABLE sender_label_mapping (
        id SERIAL PRIMARY KEY,
        pattern VARCHAR(255) NOT NULL,
        gmail_label VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Read Excel file and insert data
print("Reading email_labels.xlsx...")
wb = openpyxl.load_workbook('email_labels.xlsx')
ws = wb.active

print("Inserting sender-label mappings...")
row_count = 0
for row in ws.iter_rows(min_row=2, values_only=True):  # Skip header row
    label = row[0]
    pattern = row[1]
    
    if label and pattern:  # Only insert if both values exist
        cur.execute(
            "INSERT INTO sender_label_mapping (pattern, gmail_label) VALUES (%s, %s)",
            (pattern, label)
        )
        row_count += 1
        print(f"  Added: '{pattern}' -> '{label}'")

conn.commit()
print(f"\nSetup complete! {row_count} mappings inserted.")

cur.close()
conn.close()


