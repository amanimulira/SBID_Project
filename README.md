# SBID_Project


## Project Overview

Design and deploy an AI-pwered BI dashboard that automatically pulls raw business data (sales, customer behaviour, etc.), processes it via ETL pipelines, summarizes key trends usign LLMs, and presents actionable insights via an interactive Streamlit/Power BI dashboard. Automate reports via Power Automate, and enable stakeholders to ask natural lanugage questions about the data.

## Project Structure

1. Data Pipeline & Engineering 

* Use Python and SQL to extract data from simulated relational database (e.g., PostgreSQL).
* Build an ETL pipeline to clean, transform, and load the data for analysis.

2. Analysis & ML insights

* Use pandas, Numpy, and scikit-learn to perform:
	* descriptive analytics (e.g. KPI trends)
	* Predictive modeling (e.g. forecasting next month's revenue or churn rate)

3. AI Summarisation 

* Use an LLM (OpenAI API) to generate business summaries like:
"Revenue dropped by 12% in Q2 due to decreased returning customer rate. Recommend 
reactivation email campaign."
* Fine-tune prompt engineering for insightful, concise summaries.

4. Interactive Dashboard

* Build with Streamlit/Power BI, including:
	* KPI tiles
	* Dynamic charts with Plotly
	* Natural language query interface via LLM
	* Business scenario simulator (e.g. "What if we increase retention by 10%?)

5. Automation Layer

* Use Power Automate to:
	* Email weekly insights to stakeholders
	* Trigger alerts for abnormal data (e.g., sales dip)

6. Deployment & Git

* Host the app with Streamlit Cloud or Azure
* Maintain ful version control and documentaiton on GitHub
