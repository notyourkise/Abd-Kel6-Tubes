import streamlit as st
import pandas as pd
from modules.database import DatabaseConnection
from modules.styles import get_custom_css

st.set_page_config(page_title="Top Performance", page_icon="🏆", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

db = DatabaseConnection()
db.connect()

st.title("High Achievers")

# Filters
col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("Select Subject", ["Math", "Reading", "Writing", "Overall Average"])
with col2:
    limit = st.slider("Number of Students", 5, 50, 10)

# Query Logic
order_by = "math_score"
if subject == "Reading":
    order_by = "reading_score"
elif subject == "Writing":
    order_by = "writing_score"
elif subject == "Overall Average":
    order_by = "(math_score + reading_score + writing_score) / 3"

query = f"""
    SELECT name, gender, ethnicity, math_score, reading_score, writing_score,
           ROUND((math_score + reading_score + writing_score) / 3.0, 1) as average
    FROM student 
    ORDER BY {order_by} DESC 
    LIMIT {limit}
"""

top_students = db.execute_query(query)

if not top_students.empty:
    # Render table without relying on pyarrow (HTML fallback)
    table_html = top_students.to_html(index=False, classes="lux-table")
    st.markdown(f"<div class='lux-table-wrapper'>{table_html}</div>", unsafe_allow_html=True)
    
    # Hall of Fame Cards
    st.subheader("Hall of Fame")
    cols = st.columns(3)
    for idx, row in top_students.head(3).iterrows():
        with cols[idx]:
            st.markdown(f"""
            <div style="background-color: #141414; border: 1px solid #D4AF37; padding: 20px; text-align: center;">
                <h3 style="margin:0; color: #D4AF37;">#{idx+1}</h3>
                <h2 style="margin:10px 0; color: #FFF;">{row['name']}</h2>
                <p style="color: #AAA;">{row['ethnicity']}</p>
                <h1 style="margin:0; font-size: 3rem;">{row['average'] if subject == 'Overall Average' else row[order_by.lower()]}</h1>
                <p style="color: #D4AF37;">{subject} Score</p>
            </div>
            """, unsafe_allow_html=True)

