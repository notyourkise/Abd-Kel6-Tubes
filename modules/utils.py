import streamlit as st
import pandas as pd

def format_dataframe_display(df):
    """Format DataFrame for display"""
    if df is not None and len(df) > 0:
        return df
    return pd.DataFrame()

def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers"""
    try:
        return numerator / denominator if denominator != 0 else default
    except:
        return default

def calculate_average_score(math_score, reading_score, writing_score):
    """Calculate average exam score"""
    scores = [s for s in [math_score, reading_score, writing_score] if s is not None]
    if scores:
        return sum(scores) / len(scores)
    return 0

def categorize_performance(score):
    """Categorize student performance based on average score"""
    if score >= 80:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Satisfactory"
    elif score >= 50:
        return "Needs Improvement"
    else:
        return "Poor"
