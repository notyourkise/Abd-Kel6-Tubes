import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import DatabaseConnection
from modules.styles import get_custom_css

# Page Config
st.set_page_config(
    page_title="Student Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Database Connection
@st.cache_resource
def get_db():
    db = DatabaseConnection()
    db.connect()
    return db

db = get_db()

# Helper for charts
def apply_gold_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0', family="Lato"),
        title_font=dict(color='#D4AF37', family="Cinzel"),
        xaxis=dict(gridcolor='#333333', showgrid=True),
        yaxis=dict(gridcolor='#333333', showgrid=True),
        colorway=['#D4AF37', '#C5A028', '#8A7120', '#E5C15D', '#F0D585']
    )
    return fig

# Main Content
st.title("Executive Dashboard")
st.markdown("Overview of student performance metrics and key indicators.")

# Top Metrics
col1, col2, col3, col4 = st.columns(4)

# Fetch Data (UPDATED QUERIES)
# 1. Total Students (Tetap di tabel student)
students_count = db.execute_query("SELECT COUNT(*) as count FROM student")

# 2. Avg Scores (Sekarang ambil dari exam_scores)
avg_scores = db.execute_query("""
    SELECT AVG(math_score) as math, 
           AVG(reading_score) as reading, 
           AVG(writing_score) as writing 
    FROM exam_scores
""")

# 3. Study Stats (Sekarang study_hours_per_week ada di study_habits)
study_stats = db.execute_query("SELECT AVG(study_hours_per_week) as hours FROM study_habits")

with col1:
    count = students_count.iloc[0]['count'] if not students_count.empty else 0
    st.metric("Total Students", f"{count:,}")

with col2:
    math = avg_scores.iloc[0]['math'] if not avg_scores.empty and avg_scores.iloc[0]['math'] is not None else 0
    st.metric("Avg Math Score", f"{math:.1f}")

with col3:
    reading = avg_scores.iloc[0]['reading'] if not avg_scores.empty and avg_scores.iloc[0]['reading'] is not None else 0
    st.metric("Avg Reading Score", f"{reading:.1f}")

with col4:
    hours = study_stats.iloc[0]['hours'] if not study_stats.empty and study_stats.iloc[0]['hours'] is not None else 0
    st.metric("Avg Study Hours", f"{hours:.1f}h")

st.markdown("---")

# Charts Row 1
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Score Distribution")
    # UPDATE: Mengambil dari exam_scores
    scores_df = db.execute_query("SELECT math_score, reading_score, writing_score FROM exam_scores")
    
    if not scores_df.empty:
        fig = px.histogram(scores_df, x=['math_score', 'reading_score', 'writing_score'], 
                           barmode='overlay', opacity=0.7,
                           labels={'value': 'Score', 'variable': 'Subject'})
        fig = apply_gold_theme(fig)
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No score data available.")

with col_right:
    st.subheader("Gender Ratio")
    # UPDATE: Gender masih ada di tabel student, jadi ini aman
    gender_df = db.execute_query("SELECT gender, COUNT(*) as count FROM student GROUP BY gender")
    
    if not gender_df.empty:
        fig = px.pie(gender_df, values='count', names='gender', hole=0.6)
        fig = apply_gold_theme(fig)
        fig.update_traces(textposition='outside', textinfo='percent+label')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No gender data available.")

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Parental Education Impact")
    # UPDATE: Melakukan JOIN antara parent_background dan exam_scores
    parent_df = db.execute_query("""
        SELECT p.parental_level_of_education, 
               AVG(e.math_score) as math, 
               AVG(e.reading_score) as reading, 
               AVG(e.writing_score) as writing 
        FROM parent_background p
        JOIN exam_scores e ON p.id_student = e.id_student
        GROUP BY p.parental_level_of_education
    """)
    
    if not parent_df.empty:
        fig = px.bar(parent_df, x='parental_level_of_education', y=['math', 'reading', 'writing'],
                     barmode='group')
        fig = apply_gold_theme(fig)
        fig.update_layout(xaxis_title=None, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No parental data available.")

with col2:
    st.subheader("Study Habits vs Performance")
    # UPDATE: JOIN antara exam_scores dan study_habits menggunakan id_student
    correlation_df = db.execute_query("""
        SELECT e.math_score, s.study_hours_per_week 
        FROM exam_scores e 
        JOIN study_habits s ON e.id_student = s.id_student
    """)
    
    if not correlation_df.empty:
        fig = px.scatter(correlation_df, x='study_hours_per_week', y='math_score', opacity=0.6,
                         labels={'study_hours_per_week': 'Hours/Week', 'math_score': 'Math Score'})
        fig = apply_gold_theme(fig)
        fig.update_traces(marker=dict(size=8, line=dict(width=1, color='#000')))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No study data available.")