from openai import OpenAI
import os
import streamlit as st

# client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
client = OpenAI(api_key="")

def handle_query(user_input):
    df = open("exports/metrics_summary.json").read()

    prompt = f"""
    You are a business data analyst. Given the dataset summary below and user question, respond with an insight:
    
    Metrics:
    {df}

    Question:
    {user_input}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful data analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    st.write(response.choices[0].message.content.strip())
