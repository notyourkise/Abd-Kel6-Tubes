import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import DatabaseConnection
from modules.styles import get_custom_css

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

db = DatabaseConnection()
db.connect()

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

# --- CLEANING HELPER ---
def clean_category(series):
    return series.fillna("Tidak Diketahui")

st.title("Deep Analytics")

tab1, tab2, tab3 = st.tabs(["Performance Factors", "Demographics", "Correlations"])

# --- TAB 1: TEST PREPARATION (Complex JOIN) ---
with tab1:
    st.subheader("Impact of Test Preparation")
    
    # Logic: Left Join untuk melihat siapa yang ambil course 'Test Preparation Course'
    # Jika srv.service_name NULL, berarti dia tidak ambil course itu (None)
    prep_query = """
        SELECT 
            CASE 
                WHEN srv.service_name = 'Test Preparation Course' THEN 'Completed' 
                ELSE 'None' 
            END as status,
            AVG(e.math_score) as math, 
            AVG(e.reading_score) as reading, 
            AVG(e.writing_score) as writing 
        FROM student s
        JOIN exam_scores e ON s.id_student = e.id_student
        LEFT JOIN student_services ss ON s.id_student = ss.id_student
        LEFT JOIN services srv ON ss.service_id = srv.service_id AND srv.service_name = 'Test Preparation Course'
        GROUP BY status
    """
    prep_df = db.execute_query(prep_query)
    
    if not prep_df.empty:
        prep_df[['math', 'reading', 'writing']] = prep_df[['math', 'reading', 'writing']].round(2)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.bar(prep_df, x='status', y=['math', 'reading', 'writing'], barmode='group')
            fig = apply_gold_theme(fig)
            fig.update_layout(xaxis_title="Status Persiapan", yaxis_title="Nilai Rata-rata")
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("""
            **Analisis:** Grafik ini membandingkan rata-rata nilai siswa yang mengambil kursus persiapan vs yang tidak.
            Biasanya, siswa dengan status **Completed** memiliki skor lebih tinggi di ketiga mata pelajaran.
            """)

# --- TAB 2: DEMOGRAPHICS (Etnis) ---
with tab2:
    st.subheader("Ethnicity & Performance")
    
    # Update: ethnicity -> race_ethnicity
    # Update: Ambil nilai dari exam_scores
    eth_query = """
        SELECT s.race_ethnicity, 
               AVG(e.math_score) as math, 
               AVG(e.reading_score) as reading, 
               AVG(e.writing_score) as writing 
        FROM student s
        JOIN exam_scores e ON s.id_student = e.id_student
        GROUP BY s.race_ethnicity
        ORDER BY s.race_ethnicity
    """
    eth_df = db.execute_query(eth_query)
    
    if not eth_df.empty:
        eth_df[['math', 'reading', 'writing']] = eth_df[['math', 'reading', 'writing']].round(2)
        
        fig = px.bar(eth_df, x='race_ethnicity', y=['math', 'reading', 'writing'], barmode='group')
        fig = apply_gold_theme(fig)
        fig.update_layout(xaxis_title="Kelompok Etnis", yaxis_title="Nilai Rata-rata")
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 3: CORRELATIONS ---
with tab3:
    st.subheader("Score Correlations")
    
    # Update: Ambil langsung dari exam_scores
    scores = db.execute_query("SELECT math_score, reading_score, writing_score FROM exam_scores")
    
    if not scores.empty:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(scores, x='reading_score', y='writing_score', title="Reading vs Writing")
            fig = apply_gold_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.scatter(scores, x='math_score', y='reading_score', title="Math vs Reading")
            fig = apply_gold_theme(fig)
            st.plotly_chart(fig, use_container_width=True)