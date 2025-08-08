import pandas as pd
from sqlalchemy import create_engine

# Load Excel file
df = pd.read_csv("Sample - Superstore.csv", engine='python', encoding='latin1')

# Clean column names
df.columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]

# Rename to match SQL table
df.rename(columns={'order_id': 'order_id',
                   'order_date': 'order_date',
                   'ship_date': 'ship_date',
                   'ship_mode': 'ship_mode',
                   'customer_id': 'customer_id',
                   'customer_name': 'customer_name',
                   'segment': 'segment',
                   'country': 'country',
                   'city': 'city',
                   'state': 'state',
                   'postal_code': 'postal_code',
                   'region': 'region',
                   'product_id': 'product_id',
                   'category': 'category',
                   'sub_category': 'sub_category',
                   'product_name': 'product_name',
                   'sales': 'sales',
                   'quantity': 'quantity',
                   'discount': 'discount',
                   'profit': 'profit'}, inplace=True)

# Connect to PostgreSQL
engine = create_engine("postgresql+psycopg2://amani:April1972@localhost:5432/superstore")

# Load into PostgreSQL table
df.to_sql('orders', engine, if_exists='replace', index=False)

print("✅ Data loaded successfully into PostgreSQL!")
