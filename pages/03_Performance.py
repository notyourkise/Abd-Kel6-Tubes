import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.database import DatabaseConnection
from modules.styles import get_custom_css

st.set_page_config(page_title="Performance", page_icon="📊", layout="wide")
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

st.title("Student Performance Distribution")

# Fetch All Scores
scores_df = db.execute_query("SELECT math_score, reading_score, writing_score FROM exam_scores")

if not scores_df.empty:
    # Hitung Rata-rata Total per Siswa
    scores_df['average'] = (scores_df['math_score'] + scores_df['reading_score'] + scores_df['writing_score']) / 3
    
    # --- ROW 1: HISTOGRAMS ---
    st.subheader("Score Distribution Patterns")
    tab1, tab2, tab3, tab4 = st.tabs(["Math", "Reading", "Writing", "Overall Average"])
    
    def plot_hist(column, color, title):
        fig = px.histogram(scores_df, x=column, nbins=20, title=title, color_discrete_sequence=[color])
        fig = apply_gold_theme(fig)
        fig.update_layout(bargap=0.1)
        return fig

    with tab1: st.plotly_chart(plot_hist('math_score', '#D4AF37', 'Math Score Distribution'), use_container_width=True)
    with tab2: st.plotly_chart(plot_hist('reading_score', '#C5A028', 'Reading Score Distribution'), use_container_width=True)
    with tab3: st.plotly_chart(plot_hist('writing_score', '#8A7120', 'Writing Score Distribution'), use_container_width=True)
    with tab4: st.plotly_chart(plot_hist('average', '#F0D585', 'Average Score Distribution'), use_container_width=True)

    st.markdown("---")

    # --- ROW 2: PASS/FAIL ANALYSIS ---
    st.subheader("Pass vs Fail Analysis (Threshold: 60)")
    
    # Tentukan Pass/Fail (Misal KKM = 60)
    PASS_MARK = 60
    scores_df['status'] = scores_df['average'].apply(lambda x: 'Passed' if x >= PASS_MARK else 'Failed')
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Pie Chart
        status_counts = scores_df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        fig = px.pie(status_counts, values='count', names='status', hole=0.5, 
                     color='status', color_discrete_map={'Passed':'#D4AF37', 'Failed':'#8B0000'})
        fig = apply_gold_theme(fig)
        fig.update_layout(title="Overall Pass Rate")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Box Plot Comparison
        fig = px.box(scores_df, y=['math_score', 'reading_score', 'writing_score'], 
                     title="Score Spread & Outliers")
        fig = apply_gold_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No data available in exam_scores table.")