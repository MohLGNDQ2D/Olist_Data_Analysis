import os
import sqlite3
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'olist.db')
sql_path = os.path.join(base_dir, 'sql', 'delivery_analysis.sql')
output_csv = os.path.join(base_dir, 'Data', 'cleaned_delivery_analysis.csv')

conn = sqlite3.connect(db_path)
with open(sql_path, 'r') as f:
    query = f.read()

df = pd.read_sql_query(query, conn)
conn.close()

df = df[df['actual_delivery_days'] >= 0].copy()

print("=== Delivery Summary ===")
print(f"Total delivered orders: {len(df)}")
print(f"Delayed orders percentage: {(df['delivery_status'] == 'Delayed').mean() * 100:.2f}%\n")

print("=== Review Score by Delivery Status ===")
summary = df.groupby('delivery_status').agg(
    avg_score=('review_score', 'mean'),
    order_count=('order_id', 'count')
).reset_index()
print(summary)

df.to_csv(output_csv, index=False)
print(f"\nCleaned dataset saved to: {output_csv}")