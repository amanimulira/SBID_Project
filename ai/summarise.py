import json 
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=api_key)

# Load KPIs
with open("etl/exports/metrics_summary.json", "r") as f:
    metrics = json.load(f)

# Format prompt
prompt = f"""
You are a data analyst summarising quarterly business performance.
Use the following metrics to create an executive summary and action recommendation.

Metrics:
{json.dumps(metrics, indent=2)}

Write a short paragraph summarising the key trends and a suggestion for action.
"""

# Call GPT
response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": "You are a helpful business analyst."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7
)


summary = response.choices[0].message.content.strip()

# Save to file
with open("exports/ai_summary.txt", "w") as f:
    f.write(summary)

print("✅ AI summary saved to 'exports/ai_summary.txt'")