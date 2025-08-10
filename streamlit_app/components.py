import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet

# Load data
df = pd.read_csv("etl/exports/full_orders_data.csv")
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', infer_datetime_format=True)

# Sidebar filters
st.sidebar.header("Filters")
granularity = st.sidebar.radio("Time Granularity", ["Daily", "Monthly", "Yearly"])
target_revenue = st.sidebar.number_input("Target Revenue ($)", value=2500000, step=50000)

def show_kpis():
    total_revenue = df['sales'].sum()
    total_orders = df['order_id'].nunique()
    avg_order_value = total_revenue / total_orders
    returning_customer_rate = df[df.duplicated('customer_id', keep=False)]['customer_id'].nunique() / df['customer_id'].nunique()
    revenue_by_month = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum().pct_change().mean()

    yoy_growth = (
        df.groupby(df['order_date'].dt.year)['sales'].sum().pct_change().mean()
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}", delta=f"{((total_revenue-target_revenue)/target_revenue)*100:.2f}% vs Target")
    col2.metric("🛍️ Avg Order Value", f"${avg_order_value:,.2f}")
    col3.metric("🔁 Returning Customer Rate", f"{returning_customer_rate*100:.2f}%")
    col4.metric("📈 MoM Revenue Growth", f"{revenue_by_month*100:.2f}%")
    col5.metric("📊 YoY Growth", f"{yoy_growth*100:.2f}%")

def show_charts():
    # Adjust aggregation based on granularity
    if granularity == "Daily":
        df_grouped = df.groupby(df['order_date'].dt.date)['sales'].sum().reset_index()
        df_grouped.columns = ['date', 'Revenue ($)']
    elif granularity == "Monthly":
        df_grouped = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum().reset_index()
        df_grouped['order_date'] = df_grouped['order_date'].astype(str)
        df_grouped.columns = ['date', 'Revenue ($)']
    else:  # Yearly
        df_grouped = df.groupby(df['order_date'].dt.year)['sales'].sum().reset_index()
        df_grouped.columns = ['date', 'Revenue ($)']

    st.subheader("📆 Revenue Trend")
    fig1 = px.line(df_grouped, x='date', y='Revenue ($)', title=f"Revenue Over Time ({granularity})", markers=True)
    fig1.update_traces(line_color='#1f77b4')
    st.plotly_chart(fig1)

    # Category sales
    st.subheader("📦 Sales by Category")
    category_sales = df.groupby('category')['sales'].sum().reset_index()
    fig2 = px.bar(category_sales, x='category', y='sales', color='category', title='Sales by Category', text_auto=True)
    st.plotly_chart(fig2)

    # Region sales
    st.subheader("🌍 Sales by Region")
    region_sales = df.groupby('region')['sales'].sum().reset_index()
    fig3 = px.pie(region_sales, names='region', values='sales', title='Regional Sales Distribution', hole=0.3)
    st.plotly_chart(fig3)

def forecast():
    st.subheader("📈 30-Day Revenue Forecast with Confidence Interval")
    revenue_ts = df.groupby('order_date')['sales'].sum().reset_index()
    revenue_ts.columns = ['ds', 'y']
    model = Prophet(interval_width=0.90, yearly_seasonality=True)
    model.fit(revenue_ts)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    fig4 = px.line(forecast, x='ds', y='yhat', title='30-Day Revenue Forecast', labels={'yhat': 'Forecasted Revenue ($)'})
    fig4.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', line=dict(width=0), showlegend=False)
    fig4.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)', line=dict(width=0), showlegend=False)
    st.plotly_chart(fig4)
