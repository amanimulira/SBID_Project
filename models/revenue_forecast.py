import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from pathlib import Path

# Load your cleaned data
df = pd.read_csv("etl/exports/full_orders_data.csv")

# Prepare tiem series data: monthly revenue
df['order_date'] = pd.to_datetime(df['order_date'])
monthly_sales = df.groupby(pd.Grouper(key='order_date', freq='MS'))['sales'].sum().reset_index()


# Rename for Prophet
prophet_df = monthly_sales.rename(columns={
    'order_date': 'ds',
    'sales': 'y'
})

# Initialize and fit Prophet model
model = Prophet()
model.fit(prophet_df)

# Forecast next 6 months
future = model.make_future_dataframe(periods=6, freq='MS')
forecast = model.predict(future)

# Plot the forecast
fig1 = model.plot(forecast)
plt.title("Sales Forecast (Prophet)")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# Optional: Save forecast to CSV
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv("/Users/amani/Desktop/CV Projects Data Science/SBID_Project/etl/etl.py", index=False)

print("✅ Forecast complete and saved to 'exports/sales_forecast.csv'")