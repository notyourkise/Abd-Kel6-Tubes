import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import DatabaseConnection
from modules.styles import get_custom_css

st.set_page_config(page_title="Student Details", page_icon="👤", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

db = DatabaseConnection()
db.connect()

st.title("Student Profiles")

def render_info_card(column, label, value):
    display_value = value if value not in (None, "") else "-"
    column.markdown(
        f"""
        <div class="profile-card">
            <span class="profile-label">{label}</span>
            <span class="profile-value">{display_value}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# Search Bar
col1, col2 = st.columns([3, 1])
with col1:
    search_term = st.text_input("Search Student by Name", placeholder="Enter student name...")

# Fetch Students
query = "SELECT student_id, name, gender, ethnicity FROM student"
if search_term:
    query += f" WHERE name ILIKE '%{search_term}%'"
query += " ORDER BY student_id LIMIT 100"

students = db.execute_query(query)

if not students.empty:
    # Selection
    selected_student_name = st.selectbox("Select Student", students['name'].tolist())
    
    if selected_student_name:
        student_id = students[students['name'] == selected_student_name]['student_id'].values[0]
        
        # Fetch Full Details
        details = db.execute_query("SELECT * FROM student WHERE student_id = %s", (int(student_id),))
        habits = db.execute_query("SELECT * FROM study_habits WHERE student_id = %s", (int(student_id),))
        
        if not details.empty:
            s = details.iloc[0]
            
            st.markdown("---")
            st.subheader(f"Profile: {s['name']}")
            
            # Personal Info Grid
            col1, col2, col3, col4 = st.columns(4)
            render_info_card(col1, "ID", s['student_id'])
            render_info_card(col2, "Gender", s['gender'])
            render_info_card(col3, "Ethnicity", s['ethnicity'])
            render_info_card(col4, "Lunch", s['lunch'])
            
            # Academic Card
            st.markdown("### Academic Performance")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Math Score", s['math_score'])
            with col2:
                st.metric("Reading Score", s['reading_score'])
            with col3:
                st.metric("Writing Score", s['writing_score'])
                
            # Study Habits
            if not habits.empty:
                h = habits.iloc[0]
                st.markdown("### Study Habits")
                col1, col2, col3 = st.columns(3)
                col1.metric("Weekly Study", f"{h['study_hours_per_week']}h")
                col2.metric("Internet Usage", f"{h['hours_internet']}h")
                col3.metric("Family Study", f"{h['hours_family_study']}h")
else:
    st.info("No students found matching your search.")
