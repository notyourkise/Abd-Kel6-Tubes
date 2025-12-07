import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.database import DatabaseConnection
from config.settings import DB_CONFIG

# Page configuration
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database connection
@st.cache_resource
def get_db_connection():
    db = DatabaseConnection()
    db.connect()
    return db

db = get_db_connection()

# Sidebar navigation
st.sidebar.title("📚 Student Analytics")
page = st.sidebar.radio("Select Page", 
    ["🏠 Home", "👤 Student Details", "📊 Analytics", "🎯 Performance", "⚙️ Settings"]
)

# ============================================================================
# PAGE 1: HOME
# ============================================================================
if page == "🏠 Home":
    st.title("📊 Student Performance Analytics Dashboard")
    st.markdown("Modern analytics for student success")
    
    # Get data
    students_df = db.execute_query("SELECT * FROM student")
    exam_scores_df = db.execute_query("SELECT * FROM exam_scores")
    study_habits_df = db.execute_query("SELECT * FROM study_habits")
    
    if students_df is not None and len(students_df) > 0:
        # KPI Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("👨‍🎓 Total Students", len(students_df))
        
        with col2:
            if exam_scores_df is not None and len(exam_scores_df) > 0:
                avg_math = exam_scores_df['math_score'].mean()
                st.metric("📐 Avg Math Score", f"{avg_math:.1f}", delta="Good")
        
        with col3:
            if exam_scores_df is not None and len(exam_scores_df) > 0:
                avg_reading = exam_scores_df['reading_score'].mean()
                st.metric("📖 Avg Reading Score", f"{avg_reading:.1f}", delta="Good")
        
        with col4:
            if exam_scores_df is not None and len(exam_scores_df) > 0:
                avg_writing = exam_scores_df['writing_score'].mean()
                st.metric("✏️ Avg Writing Score", f"{avg_writing:.1f}", delta="Good")
        
        with col5:
            if study_habits_df is not None and len(study_habits_df) > 0:
                avg_study = study_habits_df['study_hours_per_week'].mean()
                st.metric("⏰ Avg Study Hours", f"{avg_study:.1f}h/week", delta="Good")
        
        st.markdown("---")
        
        # Gender Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            if 'gender' in students_df.columns:
                gender_dist = students_df['gender'].value_counts()
                fig_gender = px.bar(
                    x=gender_dist.index,
                    y=gender_dist.values,
                    labels={'x': 'Gender', 'y': 'Count'},
                    title="Students by Gender",
                    color=gender_dist.index,
                    color_discrete_sequence=["#1f77b4", "#ff7f0e"]
                )
                fig_gender.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_gender, width='stretch')
        
        with col2:
            if 'ethnicity' in students_df.columns:
                ethnicity_dist = students_df['ethnicity'].value_counts()
                fig_ethnicity = px.pie(
                    values=ethnicity_dist.values,
                    names=ethnicity_dist.index,
                    title="Distribution by Ethnicity",
                    hole=0.4
                )
                fig_ethnicity.update_layout(height=400)
                st.plotly_chart(fig_ethnicity, width='stretch')
        
        st.markdown("---")
        
        # Score Distributions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if exam_scores_df is not None and 'math_score' in exam_scores_df.columns:
                fig_math = px.histogram(
                    exam_scores_df,
                    x='math_score',
                    nbins=15,
                    title="Math Score Distribution",
                    color_discrete_sequence=["#1f77b4"]
                )
                fig_math.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_math, width='stretch')
        
        with col2:
            if exam_scores_df is not None and 'reading_score' in exam_scores_df.columns:
                fig_reading = px.histogram(
                    exam_scores_df,
                    x='reading_score',
                    nbins=15,
                    title="Reading Score Distribution",
                    color_discrete_sequence=["#ff7f0e"]
                )
                fig_reading.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_reading, width='stretch')
        
        with col3:
            if exam_scores_df is not None and 'writing_score' in exam_scores_df.columns:
                fig_writing = px.histogram(
                    exam_scores_df,
                    x='writing_score',
                    nbins=15,
                    title="Writing Score Distribution",
                    color_discrete_sequence=["#2ca02c"]
                )
                fig_writing.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_writing, width='stretch')
        
        st.markdown("---")
        st.caption("📈 Student Performance Analytics Dashboard | © 2024 | Built with Streamlit & PostgreSQL")

# ============================================================================
# PAGE 2: STUDENT DETAILS
# ============================================================================
elif page == "👤 Student Details":
    st.title("👤 Student Profile Details")
    
    students_df = db.execute_query("SELECT * FROM student ORDER BY name")
    
    if students_df is not None and len(students_df) > 0:
        selected_student = st.selectbox(
            "Select Student",
            options=students_df['name'].tolist(),
            key="student_select"
        )
        
        student_id = students_df[students_df['name'] == selected_student]['student_id'].values[0]
        
        # Get detailed info
        student_details = db.execute_query(
            "SELECT * FROM student WHERE student_id = %s",
            (student_id,)
        )
        
        exam_scores = db.execute_query(
            "SELECT * FROM exam_scores WHERE student_id = %s",
            (student_id,)
        )
        
        study_habits = db.execute_query(
            "SELECT * FROM study_habits WHERE student_id = %s",
            (student_id,)
        )
        
        parent_bg = db.execute_query(
            "SELECT * FROM parent_background WHERE student_id = %s",
            (student_id,)
        )
        
        student_services = db.execute_query(
            "SELECT s.service_name, s.service_type FROM student_services ss JOIN services s ON ss.service_id = s.service_id WHERE ss.student_id = %s",
            (student_id,)
        )
        
        student_activities = db.execute_query(
            "SELECT a.activity_name, a.activity_type FROM student_activities sa JOIN activities a ON sa.activity_id = a.activity_id WHERE sa.student_id = %s",
            (student_id,)
        )
        
        if student_details is not None and len(student_details) > 0:
            student_data = student_details.iloc[0]
            
            # Personal Info
            st.subheader("📋 Personal Information")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.info(f"**Name:** {student_data['name']}")
            with col2:
                st.info(f"**Gender:** {student_data['gender']}")
            with col3:
                st.info(f"**Ethnicity:** {student_data['ethnicity']}")
            with col4:
                st.info(f"**Lunch:** {student_data['lunch']}")
            
            st.markdown("---")
            
            # Academic Scores
            st.subheader("📊 Academic Scores")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Math Score", student_data['math_score'])
            with col2:
                st.metric("Reading Score", student_data['reading_score'])
            with col3:
                st.metric("Writing Score", student_data['writing_score'])
            with col4:
                avg = (student_data['math_score'] + student_data['reading_score'] + student_data['writing_score']) / 3
                st.metric("Average Score", f"{avg:.1f}")
            
            st.markdown("---")
            
            # Study Habits
            if study_habits is not None and len(study_habits) > 0:
                st.subheader("📚 Study Habits")
                habit_data = study_habits.iloc[0]
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Study Hours/Week", f"{habit_data['study_hours_per_week']:.1f}h")
                with col2:
                    st.metric("Internet Hours", f"{habit_data['hours_internet']:.1f}h")
                with col3:
                    st.metric("Family Study Hours", f"{habit_data['hours_family_study']:.1f}h")
                
                st.markdown("---")
            
            # Parent Background
            if parent_bg is not None and len(parent_bg) > 0:
                st.subheader("👨‍👩‍👧 Parent Background")
                st.dataframe(parent_bg[['parent_education', 'parent_occupation', 'parent_income_level']], width='stretch')
                st.markdown("---")
            
            # Services
            if student_services is not None and len(student_services) > 0:
                st.subheader("🎓 Services Enrolled")
                col1, col2 = st.columns(2)
                with col1:
                    for idx, row in student_services.iterrows():
                        st.success(f"✓ {row['service_name']} ({row['service_type']})")
            
            # Activities
            if student_activities is not None and len(student_activities) > 0:
                st.subheader("🏆 Activities Participation")
                col1, col2 = st.columns(2)
                with col1:
                    for idx, row in student_activities.iterrows():
                        st.info(f"★ {row['activity_name']} ({row['activity_type']})")

# ============================================================================
# PAGE 3: ANALYTICS
# ============================================================================
elif page == "📊 Analytics":
    st.title("📊 Analytics & Reports")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Study Habits", "Score Analysis", "Lunch Impact", "Exam Prep"])
    
    with tab1:
        st.subheader("📚 Study Habits Analysis")
        study_habits_df = db.execute_query(
            """
            SELECT sh.study_hours_per_week, sh.hours_internet, sh.hours_family_study, s.gender, s.ethnicity
            FROM study_habits sh
            JOIN student s ON sh.student_id = s.student_id
            """
        )
        
        if study_habits_df is not None and len(study_habits_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(
                    study_habits_df,
                    x='study_hours_per_week',
                    nbins=20,
                    title="Study Hours Distribution",
                    color_discrete_sequence=["#1f77b4"]
                )
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                avg_data = study_habits_df[['study_hours_per_week', 'hours_internet', 'hours_family_study']].mean()
                fig = px.bar(
                    x=['Study Hours', 'Internet Hours', 'Family Study'],
                    y=avg_data.values,
                    title="Average Time Spent",
                    color=['#1f77b4', '#ff7f0e', '#2ca02c']
                )
                st.plotly_chart(fig, width='stretch')
    
    with tab2:
        st.subheader("📈 Exam Score Analysis")
        exam_df = db.execute_query("SELECT * FROM exam_scores")
        
        if exam_df is not None and len(exam_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(
                    exam_df,
                    x='math_score',
                    y='reading_score',
                    size='writing_score',
                    color='average_score',
                    title="Math vs Reading (size=Writing)",
                    color_continuous_scale="Viridis"
                )
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                fig = px.box(
                    exam_df,
                    y=['math_score', 'reading_score', 'writing_score'],
                    title="Score Distribution by Subject",
                    labels={'value': 'Score', 'variable': 'Subject'}
                )
                st.plotly_chart(fig, width='stretch')
    
    with tab3:
        st.subheader("🍴 Lunch Type Impact on Scores")
        lunch_analysis = db.execute_query(
            """
            SELECT s.lunch, AVG(es.average_score) as avg_score, COUNT(*) as student_count
            FROM exam_scores es
            JOIN student s ON es.student_id = s.student_id
            GROUP BY s.lunch
            """
        )
        
        if lunch_analysis is not None and len(lunch_analysis) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    lunch_analysis,
                    x='lunch',
                    y='avg_score',
                    title="Average Score by Lunch Type",
                    color='avg_score',
                    color_continuous_scale="RdYlGn"
                )
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                fig = px.pie(
                    lunch_analysis,
                    values='student_count',
                    names='lunch',
                    title="Student Distribution by Lunch Type",
                    hole=0.4
                )
                st.plotly_chart(fig, width='stretch')
    
    with tab4:
        st.subheader("📝 Test Preparation Course Impact")
        prep_analysis = db.execute_query(
            """
            SELECT s.test_preparation_course, AVG(es.math_score) as avg_math, 
                   AVG(es.reading_score) as avg_reading, AVG(es.writing_score) as avg_writing,
                   COUNT(*) as student_count
            FROM exam_scores es
            JOIN student s ON es.student_id = s.student_id
            GROUP BY s.test_preparation_course
            """
        )
        
        if prep_analysis is not None and len(prep_analysis) > 0:
            fig = px.bar(
                prep_analysis,
                x='test_preparation_course',
                y=['avg_math', 'avg_reading', 'avg_writing'],
                title="Average Scores by Test Prep Course",
                barmode='group',
                labels={'value': 'Average Score', 'variable': 'Subject'}
            )
            st.plotly_chart(fig, width='stretch')

# ============================================================================
# PAGE 4: PERFORMANCE
# ============================================================================
elif page == "🎯 Performance":
    st.title("🎯 Performance Dashboard")
    
    exam_df = db.execute_query(
        """
        SELECT es.*, s.name, s.gender, s.lunch
        FROM exam_scores es
        JOIN student s ON es.student_id = s.student_id
        ORDER BY es.average_score DESC
        """
    )
    
    if exam_df is not None and len(exam_df) > 0:
        tab1, tab2, tab3 = st.tabs(["Top Performers", "Score Violin Plot", "Gender Comparison"])
        
        with tab1:
            st.subheader("🌟 Top 15 Performers")
            top_students = exam_df.head(15)[['name', 'gender', 'math_score', 'reading_score', 'writing_score', 'average_score']]
            st.dataframe(top_students, width='stretch')
        
        with tab2:
            st.subheader("🎻 Score Distribution by Gender")
            if 'gender' in exam_df.columns:
                fig = px.violin(
                    exam_df,
                    y=['math_score', 'reading_score', 'writing_score'],
                    x='gender',
                    box=True,
                    title="Score Distribution by Gender"
                )
                st.plotly_chart(fig, width='stretch')
        
        with tab3:
            st.subheader("👥 Gender Performance Metrics")
            gender_stats = exam_df.groupby('gender').agg({
                'math_score': ['mean', 'std'],
                'reading_score': ['mean', 'std'],
                'writing_score': ['mean', 'std'],
                'average_score': 'mean'
            }).round(2)
            st.dataframe(gender_stats, width='stretch')

# ============================================================================
# PAGE 5: SETTINGS
# ============================================================================
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    st.subheader("🗄️ Database Configuration")
    
    config_display = {
        "Host": DB_CONFIG['host'],
        "Port": DB_CONFIG['port'],
        "Database": DB_CONFIG['database'],
        "User": DB_CONFIG['user'],
        "Status": "✅ Connected" if db.conn else "❌ Disconnected"
    }
    
    for key, value in config_display.items():
        st.write(f"**{key}:** {value}")
    
    st.markdown("---")
    
    st.subheader("📊 Data Summary")
    
    students_count = db.execute_query("SELECT COUNT(*) as count FROM student").iloc[0]['count'] if db.execute_query("SELECT COUNT(*) as count FROM student") is not None else 0
    exams_count = db.execute_query("SELECT COUNT(*) as count FROM exam_scores").iloc[0]['count'] if db.execute_query("SELECT COUNT(*) as count FROM exam_scores") is not None else 0
    services_count = db.execute_query("SELECT COUNT(*) as count FROM student_services").iloc[0]['count'] if db.execute_query("SELECT COUNT(*) as count FROM student_services") is not None else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", students_count)
    with col2:
        st.metric("Exam Records", exams_count)
    with col3:
        st.metric("Service Enrollments", services_count)
    
    st.markdown("---")
    st.caption("Student Performance Analytics Dashboard | © 2024 | Built with Streamlit & PostgreSQL")
