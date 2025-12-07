import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import get_db_connection

st.set_page_config(
    page_title="Insights & Recommendations",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Insights & Recommendations")

db = get_db_connection()

if db:
    tab1, tab2, tab3, tab4 = st.tabs(["Key Insights", "At Risk Students", "Top Performers", "Recommendations"])
    
    with tab1:
        st.subheader("📊 Key Insights from Data")
        
        # Get overview stats
        overall_stats = db.execute_query("""
            SELECT 
                COUNT(DISTINCT s.id_student) as total_students,
                ROUND(AVG(es.math_score)::numeric, 1) as avg_math,
                ROUND(AVG(es.reading_score)::numeric, 1) as avg_reading,
                ROUND(AVG(es.writing_score)::numeric, 1) as avg_writing,
                ROUND(AVG(sh.study_hours_per_week)::numeric, 1) as avg_study_hours
            FROM student s
            LEFT JOIN exam_scores es ON s.id_student = es.id_student
            LEFT JOIN study_habits sh ON s.id_student = sh.id_student
        """)
        
        if overall_stats is not None and len(overall_stats) > 0:
            stats = overall_stats.iloc[0]
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total Students", int(stats['total_students']))
            with col2:
                st.metric("Avg Math Score", float(stats['avg_math']))
            with col3:
                st.metric("Avg Reading Score", float(stats['avg_reading']))
            with col4:
                st.metric("Avg Writing Score", float(stats['avg_writing']))
            with col5:
                st.metric("Avg Study Hours/Week", float(stats['avg_study_hours']))
        
        st.markdown("---")
        
        # Detailed insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("✅ **Strengths**")
            st.markdown("""
            - Consistent performance across different score types
            - Good participation in extracurricular activities
            - Diverse service enrollment
            """)
        
        with col2:
            st.warning("⚠️ **Areas for Improvement**")
            st.markdown("""
            - Some students show significant score variation
            - Lower participation in certain activities
            - Need more targeted tutoring support
            """)
    
    with tab2:
        st.subheader("🚨 Students At Risk")
        
        # Identify at-risk students
        at_risk = db.execute_query("""
            SELECT 
                s.id_student,
                s.name,
                s.grade_level,
                es.math_score,
                es.reading_score,
                es.writing_score,
                ROUND(((es.math_score + es.reading_score + es.writing_score) / 3)::numeric, 1) as avg_score,
                sh.study_hours_per_week,
                sh.has_private_tutor
            FROM student s
            LEFT JOIN exam_scores es ON s.id_student = es.id_student
            LEFT JOIN study_habits sh ON s.id_student = sh.id_student
            WHERE (es.math_score < 60 OR es.reading_score < 60 OR es.writing_score < 60)
               OR ROUND(((es.math_score + es.reading_score + es.writing_score) / 3), 1) < 60
            ORDER BY avg_score ASC
        """)
        
        if at_risk is not None and len(at_risk) > 0:
            st.warning(f"⚠️ Found {len(at_risk)} students at risk")
            
            # Filter by threshold
            threshold = st.slider("Score Threshold", 0, 100, 60)
            filtered_at_risk = at_risk[at_risk['avg_score'] < threshold]
            
            if len(filtered_at_risk) > 0:
                st.dataframe(filtered_at_risk[['name', 'grade_level', 'math_score', 'reading_score', 'writing_score', 'avg_score', 'has_private_tutor']], 
                           use_container_width=True)
                
                # Visualization
                fig = px.scatter(
                    filtered_at_risk,
                    x='study_hours_per_week',
                    y='avg_score',
                    size='avg_score',
                    color='grade_level',
                    hover_data=['name'],
                    title="At-Risk Students: Study Hours vs Performance"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No students below selected threshold!")
        else:
            st.success("✅ All students performing above minimum threshold!")
    
    with tab3:
        st.subheader("⭐ Top Performing Students")
        
        top_students = db.execute_query("""
            SELECT 
                s.id_student,
                s.name,
                s.grade_level,
                es.math_score,
                es.reading_score,
                es.writing_score,
                ROUND(((es.math_score + es.reading_score + es.writing_score) / 3)::numeric, 1) as avg_score,
                sh.study_hours_per_week
            FROM student s
            LEFT JOIN exam_scores es ON s.id_student = es.id_student
            LEFT JOIN study_habits sh ON s.id_student = sh.id_student
            ORDER BY avg_score DESC
            LIMIT 20
        """)
        
        if top_students is not None and len(top_students) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(top_students[['name', 'grade_level', 'math_score', 'reading_score', 'writing_score', 'avg_score']], 
                           use_container_width=True)
            
            with col2:
                fig = px.bar(
                    top_students.head(10),
                    x='avg_score',
                    y='name',
                    title="Top 10 Highest Performing Students",
                    color='avg_score',
                    color_continuous_scale="Greens"
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("💼 Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📌 **For Educators**")
            st.markdown("""
            1. **Personalized Support**: Provide extra support to at-risk students
            2. **Study Patterns**: Encourage longer study hours for low performers
            3. **Tutor Programs**: Expand private tutoring for struggling students
            4. **Grade-Specific Focus**: Tailor programs by grade level
            5. **Activity Engagement**: Increase extracurricular participation
            """)
        
        with col2:
            st.info("📌 **For Students**")
            st.markdown("""
            1. **Increase Study Time**: Aim for 18+ hours per week
            2. **Balance Subjects**: Focus on weaker subject areas
            3. **Get Support Early**: Seek tutoring before scores drop
            4. **Participate in Activities**: Join extracurriculars for wellness
            5. **Use Services**: Take advantage of school services
            """)
        
        st.markdown("---")
        
        # Data-driven recommendations
        st.subheader("📊 Data-Driven Recommendations")
        
        # Analyze study hours impact
        study_impact = db.execute_query("""
            SELECT 
                CASE 
                    WHEN sh.study_hours_per_week < 10 THEN 'Low (<10 hrs)'
                    WHEN sh.study_hours_per_week < 15 THEN 'Medium (10-15 hrs)'
                    ELSE 'High (>15 hrs)'
                END as study_category,
                ROUND(AVG(es.math_score)::numeric, 1) as avg_math,
                ROUND(AVG(es.reading_score)::numeric, 1) as avg_reading,
                ROUND(AVG(es.writing_score)::numeric, 1) as avg_writing,
                COUNT(*) as count
            FROM student s
            LEFT JOIN study_habits sh ON s.id_student = sh.id_student
            LEFT JOIN exam_scores es ON s.id_student = es.id_student
            GROUP BY study_category
            ORDER BY count DESC
        """)
        
        if study_impact is not None and len(study_impact) > 0:
            st.write("**Study Hours Impact on Performance:**")
            st.dataframe(study_impact, use_container_width=True)
else:
    st.error("❌ Database connection failed!")
