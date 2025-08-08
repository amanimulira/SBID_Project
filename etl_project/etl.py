from sqlalchemy import create_engine
import pandas as pd
import os
from db_config import DB_CONFIG


# --------------------
# 1. Setup
# --------------------

def get_engine():
    uri = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(uri)

def load_sql_query(filepath):
    with open(filepath, "r") as file:
        return file.read()

# --------------------
# 2. Data Extraction
# --------------------

def extract_data(engine, sql_path):
    query = load_sql_query(sql_path)
    df = pd.read_sql(query, engine)
    return df

# --------------------
# 3. Data Transformation
# --------------------

def transform_data(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df['discounted_sales'] = df['sales'] * (1 - df['discount'])
    df['order_date'] = pd.to_datetime(df['order_date'])

    product = df.groupby('product_name').agg({
        'sales': 'sum',
        'discounted_sales': 'sum',
        'profit': 'sum',
        'quantity': 'sum'
    }).reset_index().sort_values(by='sales', ascending=False)

    customer = df.groupby('customer_name').agg({
        'sales': 'sum',
        'profit': 'sum',
        'quantity': 'sum'
    }).reset_index().sort_values(by='sales', ascending=False)

    daily = df.groupby('order_date').agg({
        'sales': 'sum',
        'profit': 'sum'
    }).reset_index().sort_values(by='order_date')

    region = df.groupby('region').agg({
        'sales': 'sum',
        'profit': 'sum'
    }).reset_index()

    return df, product, customer, daily, region

# --------------------
# 4. Data Export
# --------------------

def export_data(dataframes, filenames, output_dir="etl_project/exports"):
    os.makedirs(output_dir, exist_ok=True)
    for df, name in zip(dataframes, filenames):
        df.to_csv(os.path.join(output_dir, name), index=False)
    print(f"✅ Exported to: {output_dir}")


# --------------------
# 5. Main Pipeline
# --------------------

def run_etl():
    engine = get_engine()
    raw_df = extract_data(engine, 'etl_project/sql/load_orders.sql')
    full_df, product_df, customer_df, daily_df, region_df = transform_data(raw_df)

    export_data(
        [full_df, product_df, customer_df, daily_df, region_df],
        ['full_orders_data.csv', 'product_sales.csv', 'customer_sales.csv', 'daily_sales.csv', 'region_sales.csv']
    )

if __name__ == "__main__":
    run_etl()