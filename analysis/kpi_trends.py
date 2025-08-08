import pandas as pd

# Load full exported data (from ETL)
df = pd.read_csv("etl/exports/full_orders_data.csv")
df['order_date'] = pd.to_datetime(df['order_date'])

# Monthly Revenue
monthly_revenue = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum().reset_index()
monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()

# Average Order Value (AOV)
aov = df.groupby('order_id').agg({'sales': 'sum'}).sales.mean()

# Profit Margin
df['margin'] = df['profit'] / df['sales']
avg_margin = df['margin'].mean()

# Top Categories by Revenue
top_categories = df.groupby('category')['sales'].sum().sort_values(ascending=False).reset_index()

# Customer Order Frequency
customer_freq = df.groupby('customer_id')['order_id'].nunique().reset_index(name='orders')

# Show key results
print("📈 Monthly Revenue:\n", monthly_revenue.tail())
print(f"\n💵 Average Order Value: £{aov:.2f}")
print(f"💰 Average Profit Margin: {avg_margin:.2%}")
print("\n🛍️ Top Categories:\n", top_categories)
print("\n🧍‍♂️ Customer Order Frequency:\n", customer_freq.head())