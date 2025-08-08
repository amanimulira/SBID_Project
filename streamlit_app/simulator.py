import streamlit as st
import pandas as pd

def run_simulation():
    df = pd.read_csv("etl/exports/full_orders_data.csv")
    current_customers = df['customer_id'].nunique()
    retention_rate = st.slider("Increase Retention Rate by (%)", 0, 50, 10)

    estimated_returning_customers = current_customers * (1 + retention_rate / 100)
    avg_sales_per_customer = df['sales'].sum() / current_customers
    projected_sales = estimated_returning_customers * avg_sales_per_customer

    st.write(f"📈 Projected Sales with +{retention_rate}% Retention: **${projected_sales:,.0f}**")
