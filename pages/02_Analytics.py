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

def clean_category(series):
    def _normalize(value):
        if value is None:
            return "Tidak Diketahui"
        if isinstance(value, str):
            stripped = value.strip()
            if stripped == "":
                return "Tidak Diketahui"
            if stripped.lower() in {"undefined", "none", "null"}:
                return "Tidak Diketahui"
        return value
    return series.apply(_normalize)

st.title("Deep Analytics")

tab1, tab2, tab3 = st.tabs(["Performance Factors", "Demographics", "Correlations"])

with tab1:
    st.subheader("Impact of Test Preparation")
    prep_df = db.execute_query("""
        SELECT test_preparation_course, 
               AVG(math_score) as math, 
               AVG(reading_score) as reading, 
               AVG(writing_score) as writing 
        FROM student 
        GROUP BY test_preparation_course
    """)
    
    if not prep_df.empty:
        prep_df['test_preparation_course'] = clean_category(prep_df['test_preparation_course'])
        prep_df[['math', 'reading', 'writing']] = prep_df[['math', 'reading', 'writing']].round(2)
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.bar(prep_df, x='test_preparation_course', y=['math', 'reading', 'writing'], barmode='group')
            fig = apply_gold_theme(fig)
            fig.update_layout(
                xaxis_title="Program Persiapan",
                yaxis_title="Nilai Rata-rata"
            )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown("""
            **Tujuan grafik:** Memetakan dampak program persiapan ujian terhadap tiga jenis nilai.
            **Cara baca:** Bandingkan tinggi bar antar kategori untuk melihat sejauh mana latihan tambahan meningkatkan performa.
            **Insight yang dicari:** Apakah investasi waktu dan biaya untuk kursus persiapan layak karena mampu mendorong nilai rata-rata.
            """)

with tab2:
    st.subheader("Ethnicity & Performance")
    eth_df = db.execute_query("""
        SELECT ethnicity, 
               AVG(math_score) as math, 
               AVG(reading_score) as reading, 
               AVG(writing_score) as writing 
        FROM student 
        GROUP BY ethnicity
    """)
    
    if not eth_df.empty:
        eth_df['ethnicity'] = clean_category(eth_df['ethnicity'])
        eth_df[['math', 'reading', 'writing']] = eth_df[['math', 'reading', 'writing']].round(2)
        fig = px.bar(eth_df, x='ethnicity', y=['math', 'reading', 'writing'], barmode='group')
        fig = apply_gold_theme(fig)
        fig.update_layout(
            xaxis_title="Kelompok Etnis",
            yaxis_title="Nilai Rata-rata"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        **Tujuan grafik:** Membandingkan capaian rata-rata tiap kelompok demografis.
        **Cara baca:** Bar yang lebih tinggi menunjukkan kelompok yang relatif unggul di mata pelajaran tertentu.
        **Insight yang dicari:** Identifikasi kesenjangan performa sehingga sekolah bisa menargetkan intervensi yang lebih adil.
        """)

with tab3:
    st.subheader("Score Correlations")
    scores = db.execute_query("SELECT math_score, reading_score, writing_score FROM student")
    
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
        st.markdown("""
        **Tujuan grafik:** Mengukur hubungan antar nilai mata pelajaran sehingga korelasi positif/negatif terlihat jelas.
        **Cara baca:** Titik yang membentuk garis diagonal rapat menandakan korelasi kuat; sebaran acak menandakan hubungan lemah.
        **Insight yang dicari:** Mengetahui mata pelajaran mana yang bergerak bersama untuk merancang strategi pengajaran terpadu.
        """)
