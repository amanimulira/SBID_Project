from sqlalchemy import create_engine
import pandas as pd
import os
from db_config import DB_CONFIG

def get_engine():
    uri = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(uri)

def load_sales_data(engine):
    with open("sql/sales_query.sql", "r") as f:
        query = f.read()
    return pd.read_sql(query, engine)

def transform_data(df):
    df.columns = df.columns.str.lower().str.replace(" ","_")
    df['total_sale'] = df['quantity'] * df['price']

    product = df.groupby('product_name').agg({'quantity': 'sum', 'total_sale': 'sum'}).reset_index()
    customer = df.groupby('customer_name').agg({'quantity': 'sum', 'total_sale': 'sum'}).reset_index()
    daily = df.groupby('sale_date').agg({'quantity': 'sum', 'total_sale': 'sum'}).reset_index()

    return df, product, customer, daily

def export_csv(dataframes, filenames):
    os.makedirs("exports", exist_ok=True)
    for df, fname in zip(dataframes, filenames):
        df.to_csv(f"exports/{fname}", inde=False)

if __name__ == "__main__":
    engine = get_engine()
    raw_df = load_sales_data(engine)
    full_df, product_df, customer_df, daily_df = transform_data(raw_df)

    export_csv(
        [full_df, product_df, customer_df, daily_df],
        ['full_sales_data.csv', 'product_sales_summary.csv', 'customer_sales_summary.csv', 'daily_sales_summary.csv']
    )
    print("✅ ETL completed and data exported to /exports")