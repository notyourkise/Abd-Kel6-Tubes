import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import get_db_connection

st.set_page_config(
    page_title="Student Details",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Student Details")

db = get_db_connection()

if db:
    # Get all students for selection
    students_df = db.execute_query("SELECT id_student, name, grade_level FROM student ORDER BY name")
    
    if students_df is not None and len(students_df) > 0:
        # Create selection dropdown
        student_options = {f"{row['name']} ({row['grade_level']})": row['id_student'] 
                          for _, row in students_df.iterrows()}
        
        selected_student = st.selectbox("Select a Student", list(student_options.keys()))
        student_id = student_options[selected_student]
        
        # Get student details
        student_info = db.execute_query(f"SELECT * FROM student WHERE id_student = {student_id}")
        study_habits = db.execute_query(f"SELECT * FROM study_habits WHERE id_student = {student_id}")
        exam_scores = db.execute_query(f"SELECT * FROM exam_scores WHERE id_student = {student_id}")
        parent_info = db.execute_query(f"SELECT * FROM parent_background WHERE id_student = {student_id}")
        services = db.execute_query(f"""
            SELECT s.service_name, ss.service_status
            FROM student_services ss
            JOIN services s ON ss.service_id = s.service_id
            WHERE ss.id_student = {student_id}
        """)
        activities = db.execute_query(f"""
            SELECT a.activity_type, sa.hours_per_week
            FROM student_activities sa
            JOIN activities a ON sa.activity_id = a.activity_id
            WHERE sa.id_student = {student_id}
        """)
        
        st.markdown("---")
        
        # Student Info Section
        st.subheader("📋 Personal Information")
        col1, col2, col3, col4 = st.columns(4)
        
        if student_info is not None and len(student_info) > 0:
            info = student_info.iloc[0]
            with col1:
                st.info(f"**Name:** {info['name']}")
            with col2:
                st.info(f"**Gender:** {info['gender']}")
            with col3:
                st.info(f"**Grade:** {info['grade_level']}")
            with col4:
                st.info(f"**Ethnicity:** {info['race_ethnicity']}")
            
            st.write(f"**Date of Birth:** {info['date_of_birth']}")
        
        st.markdown("---")
        
        # Study Habits Section
        st.subheader("📚 Study Habits")
        if study_habits is not None and len(study_habits) > 0:
            habits = study_habits.iloc[0]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Weekly Study Hours", habits['study_hours_per_week'])
            with col2:
                st.metric("Prefers Group Study", "Yes" if habits['prefers_group_study'] else "No")
            with col3:
                st.metric("Has Private Tutor", "Yes" if habits['has_private_tutor'] else "No")
        
        st.markdown("---")
        
        # Exam Scores Section
        st.subheader("📊 Exam Scores")
        if exam_scores is not None and len(exam_scores) > 0:
            scores = exam_scores.iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Math Score", scores['math_score'], "📐")
            with col2:
                st.metric("Reading Score", scores['reading_score'], "📖")
            with col3:
                st.metric("Writing Score", scores['writing_score'], "✍️")
            
            # Radar chart for exam scores
            avg_score = (scores['math_score'] + scores['reading_score'] + scores['writing_score']) / 3
            st.metric("Average Score", f"{avg_score:.1f}", 
                     "Excellent" if avg_score >= 80 else "Good" if avg_score >= 70 else "Satisfactory")
            
            # Visualization
            import plotly.graph_objects as go
            fig = go.Figure(data=[
                go.Scatterpolar(
                    r=[scores['math_score'], scores['reading_score'], scores['writing_score']],
                    theta=['Math', 'Reading', 'Writing'],
                    fill='toself'
                )
            ])
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title="Exam Score Performance",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Parent Background
        st.subheader("👨‍👩‍👧 Parent Information")
        if parent_info is not None and len(parent_info) > 0:
            st.dataframe(parent_info[['parent_type', 'parent_occupation', 'parental_level_of_education']], 
                        use_container_width=True)
        
        st.markdown("---")
        
        # Services
        st.subheader("🏫 Enrolled Services")
        if services is not None and len(services) > 0:
            st.dataframe(services, use_container_width=True)
        else:
            st.info("No services enrolled")
        
        st.markdown("---")
        
        # Activities
        st.subheader("🎭 Extracurricular Activities")
        if activities is not None and len(activities) > 0:
            st.dataframe(activities, use_container_width=True)
        else:
            st.info("No activities participated")
    else:
        st.error("No students found")
else:
    st.error("❌ Database connection failed!")
