import os
import glob
import sqlite3
import pandas as pd

data_dir = os.path.join(os.path.dirname(__file__), 'Data')
db_path = os.path.join(os.path.dirname(__file__), 'olist.db')

conn = sqlite3.connect(db_path)
csv_files = glob.glob(os.path.join(data_dir, '*.csv'))

for file_path in csv_files:
    file_name = os.path.basename(file_path)
    table_name = file_name.replace('_dataset.csv', '').replace('.csv', '')
    
    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Loaded table: {table_name} ({len(df)} rows)")

conn.close()
print("Database olist.db created successfully!")
