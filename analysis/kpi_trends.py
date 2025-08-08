import pandas as pd
import json
from pathlib import Path

# Load data
df = pd.read_csv("etl/exports/full_orders_data.csv")
df['order_date'] = pd.to_datetime(df['order_date'])

# 1. Monthly Revenue
monthly_revenue = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum().reset_index()
monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()

# 2. Average Order Value (AOV)
aov = df.groupby('order_id').agg({'sales': 'sum'}).sales.mean()

# 3. Profit Margin
df['margin'] = df['profit'] / df['sales']
avg_margin = df['margin'].mean()

# 4. Top Categories by Revenue
top_categories = df.groupby('category')['sales'].sum().sort_values(ascending=False).reset_index()

# 5. Customer Order Frequency
customer_freq = df.groupby('customer_id')['order_id'].nunique().reset_index(name='orders')

# 6. Quarterly Metrics
df['quarter'] = df['order_date'].dt.quarter
df['year'] = df['order_date'].dt.year

# Assuming current year analysis
current_year = df['year'].max()
q1_sales = df[(df['quarter'] == 1) & (df['year'] == current_year)]['sales'].sum()
q2_sales = df[(df['quarter'] == 2) & (df['year'] == current_year)]['sales'].sum()

# Returning customers (placed >1 order)
returning_q1 = customer_freq[(customer_freq['orders'] > 1)].shape[0]
returning_q2 = customer_freq[(customer_freq['orders'] > 1)].shape[0]  # Adjust logic as needed

# Average discount in Q2
avg_discount_q2 = df[(df['quarter'] == 2) & (df['year'] == current_year)]['discount'].mean()

# Top declining category (example logic - adjust based on your trend analysis)
category_growth = df.groupby(['category', 'quarter'])['sales'].sum().unstack().pct_change(axis=1)
top_declining = category_growth.iloc[:,-1].idxmin()  # Gets category with worst Q2 performance

# Prepare JSON output
metrics = {
    "total_sales_q1": round(q1_sales, 2),
    "total_sales_q2": round(q2_sales, 2),
    "returning_customers_q1": returning_q1,
    "returning_customers_q2": returning_q2,
    "avg_discount_q2": round(avg_discount_q2, 2),
    "top_declining_category": top_declining,
    "average_order_value": round(aov, 2),
    "average_profit_margin": round(avg_margin, 4)
}

# Save to JSON
output_path = Path("etl/exports/metrics_summary.json")
output_path.parent.mkdir(exist_ok=True, parents=True)

with open(output_path, 'w') as f:
    json.dump(metrics, f, indent=2)

print("✅ Metrics saved to etl/exports/metrics_summary.json")
print(json.dumps(metrics, indent=2))

# Show key results (original outputs)
print("\n📈 Monthly Revenue:\n", monthly_revenue.tail())
print(f"\n💵 Average Order Value: £{aov:.2f}")
print(f"💰 Average Profit Margin: {avg_margin:.2%}")
print("\n🛍️ Top Categories:\n", top_categories)
print("\n🧍‍♂️ Customer Order Frequency:\n", customer_freq.head())