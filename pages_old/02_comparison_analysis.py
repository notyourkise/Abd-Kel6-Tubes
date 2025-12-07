import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.database import get_db_connection

st.set_page_config(
    page_title="Comparison Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Comparison Analysis")

db = get_db_connection()

if db:
    tab1, tab2, tab3 = st.tabs(["Grade Comparison", "Gender Comparison", "Tutor Impact"])
    
    with tab1:
        st.subheader("Performance by Grade Level")
        
        performance_df = db.execute_query("""
            SELECT 
                s.grade_level,
                es.math_score,
                es.reading_score,
                es.writing_score
            FROM student s
            JOIN exam_scores es ON s.id_student = es.id_student
        """)
        
        if performance_df is not None and len(performance_df) > 0:
            # Calculate stats by grade
            grade_stats = performance_df.groupby('grade_level').agg({
                'math_score': ['mean', 'std'],
                'reading_score': ['mean', 'std'],
                'writing_score': ['mean', 'std']
            }).round(2)
            
            # Visualization
            col1, col2 = st.columns(2)
            
            with col1:
                avg_by_grade = performance_df.groupby('grade_level')[['math_score', 'reading_score', 'writing_score']].mean()
                fig = px.bar(
                    avg_by_grade.reset_index(),
                    x='grade_level',
                    y=['math_score', 'reading_score', 'writing_score'],
                    title="Average Scores by Grade Level",
                    labels={'grade_level': 'Grade Level', 'value': 'Score'},
                    barmode='group'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig_box = px.box(
                    performance_df,
                    x='grade_level',
                    y='math_score',
                    title="Math Score Distribution by Grade",
                    labels={'grade_level': 'Grade Level', 'math_score': 'Math Score'}
                )
                fig_box.update_layout(height=400)
                st.plotly_chart(fig_box, use_container_width=True)
            
            st.subheader("Detailed Statistics")
            st.dataframe(grade_stats, use_container_width=True)
    
    with tab2:
        st.subheader("Performance by Gender")
        
        gender_df = db.execute_query("""
            SELECT 
                s.gender,
                es.math_score,
                es.reading_score,
                es.writing_score
            FROM student s
            JOIN exam_scores es ON s.id_student = es.id_student
        """)
        
        if gender_df is not None and len(gender_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                avg_gender = gender_df.groupby('gender')[['math_score', 'reading_score', 'writing_score']].mean()
                fig = px.bar(
                    avg_gender.reset_index(),
                    x='gender',
                    y=['math_score', 'reading_score', 'writing_score'],
                    title="Average Scores by Gender",
                    barmode='group'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig_violin = px.violin(
                    gender_df,
                    x='gender',
                    y='reading_score',
                    title="Reading Score Distribution by Gender",
                    box=True,
                    points='all'
                )
                fig_violin.update_layout(height=400)
                st.plotly_chart(fig_violin, use_container_width=True)
    
    with tab3:
        st.subheader("Impact of Private Tutor on Performance")
        
        tutor_df = db.execute_query("""
            SELECT 
                sh.has_private_tutor,
                es.math_score,
                es.reading_score,
                es.writing_score
            FROM student s
            JOIN study_habits sh ON s.id_student = sh.id_student
            JOIN exam_scores es ON s.id_student = es.id_student
        """)
        
        if tutor_df is not None and len(tutor_df) > 0:
            tutor_df['tutor_status'] = tutor_df['has_private_tutor'].apply(
                lambda x: 'With Tutor' if x else 'No Tutor'
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                avg_tutor = tutor_df.groupby('tutor_status')[['math_score', 'reading_score', 'writing_score']].mean()
                fig = px.bar(
                    avg_tutor.reset_index(),
                    x='tutor_status',
                    y=['math_score', 'reading_score', 'writing_score'],
                    title="Average Scores with/without Private Tutor",
                    barmode='group'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Calculate difference
                with_tutor = tutor_df[tutor_df['has_private_tutor']]['writing_score'].mean()
                without_tutor = tutor_df[~tutor_df['has_private_tutor']]['writing_score'].mean()
                diff = with_tutor - without_tutor
                
                st.metric(
                    "Average Writing Score - With Tutor",
                    f"{with_tutor:.1f}",
                    f"{diff:+.1f}"
                )
                
                fig_box = px.box(
                    tutor_df,
                    x='tutor_status',
                    y='writing_score',
                    title="Writing Score Distribution",
                    color='tutor_status'
                )
                fig_box.update_layout(height=300)
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Summary statistics
            st.subheader("Summary Statistics")
            summary = tutor_df.groupby('tutor_status')[['math_score', 'reading_score', 'writing_score']].agg(['mean', 'std', 'count']).round(2)
            st.dataframe(summary, use_container_width=True)
else:
    st.error("❌ Database connection failed!")
