import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet

df = pd.read_csv("etl/exports/full_orders_data.csv")

def show_kpis():
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', infer_datetime_format=True)
    # KPI calculations
    total_revenue = df['sales'].sum()
    total_orders = df['order_id'].nunique()
    avg_order_value = total_revenue / total_orders
    returning_customer_rate = df[df.duplicated('customer_id', keep=False)]['customer_id'].nunique() / df['customer_id'].nunique()
    revenue_by_month = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum().pct_change().mean()

    # KPI display
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("🛍️ Avg Order Value", f"${avg_order_value:,.2f}")
    col3.metric("🔁 Returning Customer Rate", f"{returning_customer_rate*100:.2f}%")
    col4.metric("📈 MoM Revenue Growth", f"{revenue_by_month*100:.2f}%")

def show_charts():
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', infer_datetime_format=True)

    
    st.subheader("📆 Monthly Revenue Trend")
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    monthly_sales = df.groupby('month')['sales'].sum().reset_index()
    fig1 = px.line(monthly_sales, x='month', y='sales', title='Revenue Over Time')
    st.plotly_chart(fig1)

    st.subheader("📦 Sales by Category")
    category_sales = df.groupby('category')['sales'].sum().reset_index()
    fig2 = px.bar(category_sales, x='category', y='sales', color='category', title='Sales by Category')
    st.plotly_chart(fig2)

    st.subheader("🌍 Sales by Region")
    region_sales = df.groupby('region')['sales'].sum().reset_index()
    fig3 = px.pie(region_sales, names='region', values='sales', title='Regional Sales Distribution')
    st.plotly_chart(fig3)

def forcast():
    st.subheader("Revenue Forecast")
    revenue_ts = df.groupby('order_date')['sales'].sum().reset_index()
    revenue_ts.columns = ['ds', 'y']
    model = Prophet()
    model.fit(revenue_ts)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    fig4 = px.line(forecast, x='ds', y='yhat', title='30-Day Revenue Forecast')
    st.plotly_chart(fig4)

def filters():
    st.sidebar.header("Filters")
    segment_filter = st.sidebar.selectbox("Segment", df['segment'].unique())
    category_filter = st.sidebar.selectbox("Category", df['category'].unique())

    filtered_df = df[(df['segment'] == segment_filter) & (df['category'] == category_filter)]
    st.sidebar.markdown(f"Filtered Rows: {len(filtered_df)}")
