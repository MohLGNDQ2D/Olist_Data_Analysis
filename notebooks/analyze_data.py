import os
import sqlite3
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'olist.db')
sql_path = os.path.join(base_dir, 'sql', 'delivery_analysis.sql')
output_csv = os.path.join(base_dir, 'Data', 'cleaned_delivery_analysis.csv')

# 1. Read data from database using SQL query
conn = sqlite3.connect(db_path)
with open(sql_path, 'r') as f:
    query = f.read()
df = pd.read_sql_query(query, conn)
conn.close()

# 2. Clean data: remove invalid negative days
df = df[df['actual_delivery_days'] >= 0].copy()

# 3. Calculate average review score
print("Average review score by delivery status:")
print(df.groupby('delivery_status')['review_score'].mean())

# 4. Save clean data for Power BI
df.to_csv(output_csv, index=False)
print("\nClean data saved successfully!")