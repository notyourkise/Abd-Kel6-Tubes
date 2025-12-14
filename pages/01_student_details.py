import streamlit as st
import pandas as pd
from modules.database import DatabaseConnection
from modules.styles import get_custom_css

# Page Configuration
st.set_page_config(page_title="Student Details", page_icon="👤", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Connect to Database
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

# --- SEARCH BAR ---
col1, col2 = st.columns([3, 1])
with col1:
    search_term = st.text_input("Search Student by Name", placeholder="Enter student name...")

# --- FETCH STUDENTS LIST ---
# Update: student_id -> id_student, ethnicity -> race_ethnicity
query = "SELECT id_student, name, gender, race_ethnicity FROM student"
if search_term:
    query += f" WHERE name ILIKE '%{search_term}%'"
query += " ORDER BY id_student LIMIT 100"

students = db.execute_query(query)

if not students.empty:
    # --- SELECTION ---
    selected_student_name = st.selectbox("Select Student", students['name'].tolist())
    
    if selected_student_name:
        # Get ID (Update: id_student)
        student_id = students[students['name'] == selected_student_name]['id_student'].values[0]
        
        # --- FETCH FULL DETAILS (MULTI-TABLE QUERIES) ---
        
        # 1. Basic Info
        details = db.execute_query("SELECT * FROM student WHERE id_student = %s", (int(student_id),))
        
        # 2. Exam Scores (New Table)
        scores = db.execute_query("SELECT * FROM exam_scores WHERE id_student = %s", (int(student_id),))
        
        # 3. Study Habits (New Columns)
        habits = db.execute_query("SELECT * FROM study_habits WHERE id_student = %s", (int(student_id),))
        
        # 4. Lunch Status (Complex JOIN)
        # Mencari status layanan di mana nama servicenya adalah 'Lunch Program'
        lunch_query = """
            SELECT ss.service_status
            FROM student_services ss
            JOIN services srv ON ss.service_id = srv.service_id
            WHERE ss.id_student = %s AND srv.service_name = 'Lunch Program'
        """
        lunch_data = db.execute_query(lunch_query, (int(student_id),))
        lunch_status = lunch_data.iloc[0]['service_status'] if not lunch_data.empty else "Standard"

        # --- DISPLAY LOGIC ---
        if not details.empty:
            s = details.iloc[0]
            
            st.markdown("---")
            st.subheader(f"Profile: {s['name']}")
            
            # Personal Info Grid
            col1, col2, col3, col4 = st.columns(4)
            render_info_card(col1, "ID", s['id_student'])
            render_info_card(col2, "Gender", s['gender'])
            render_info_card(col3, "Race/Ethnicity", s['race_ethnicity']) # Update key
            render_info_card(col4, "Lunch Plan", lunch_status) # Value from Join
            
            # Academic Card
            st.markdown("### Academic Performance")
            col1, col2, col3 = st.columns(3)
            
            if not scores.empty:
                sc = scores.iloc[0]
                with col1: st.metric("Math Score", sc['math_score'])
                with col2: st.metric("Reading Score", sc['reading_score'])
                with col3: st.metric("Writing Score", sc['writing_score'])
            else:
                st.warning("No exam scores found for this student.")
                
            # Study Habits
            if not habits.empty:
                h = habits.iloc[0]
                st.markdown("### Study Habits")
                col1, col2, col3 = st.columns(3)
                
                # Update Metrics sesuai kolom baru database
                col1.metric("Weekly Study", f"{h['study_hours_per_week']}h")
                col2.metric("Group Study?", h['prefers_group_study'])
                col3.metric("Private Tutor?", h['has_private_tutor'])
            else:
                st.info("No study habit data available.")
else:
    st.info("No students found matching your search.")