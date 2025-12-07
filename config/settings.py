import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'student_performance_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
}

# Application Configuration
APP_NAME = "Student Performance Analytics"
APP_ICON = "📊"
PAGE_LAYOUT = "wide"

# Streamlit Configuration
STREAMLIT_CONFIG = {
    'theme': {
        'primaryColor': '#FF6B6B',
        'backgroundColor': '#FFFFFF',
        'secondaryBackgroundColor': '#F0F2F6',
        'textColor': '#262730',
        'font': 'sans serif',
    }
}
