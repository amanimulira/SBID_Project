import streamlit as st
from components import show_kpis, show_charts, forcast, filters
from query_ai import handle_query
from simulator import run_simulation

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("Superstore Performance Dashboard")

# KPIs
show_kpis()

# Charts
show_charts()

# Forecast
forcast()

# Filters
filters()

# Natural Laugage Q&A
st.subheader("Ask About the Data")
user_query = st.text_input("Ask a question like: 'What was Q2 revenue?' or 'Which category performed best?'")

if user_query:
    handle_query(user_query)

# Scenario Simulation
st.subheader("Business Scenario Simulator")
run_simulation()