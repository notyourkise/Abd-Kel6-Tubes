
def get_custom_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:wght@300;400;700&display=swap');

        :root {
            --gold-primary: #D4AF37;
            --gold-secondary: #C5A028;
            --gold-dim: #8A7120;
            --bg-dark: #0A0A0A;
            --bg-card: #141414;
            --text-main: #E0E0E0;
            --text-muted: #A0A0A0;
        }

        /* Global Reset & Typography */
        .stApp {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Lato', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Cinzel', serif;
            color: var(--gold-primary) !important;
            font-weight: 700;
            letter-spacing: 1px;
        }
        
        h1 { font-size: 2.5rem; text-transform: uppercase; border-bottom: 2px solid var(--gold-dim); padding-bottom: 10px; margin-bottom: 30px; }
        h2 { font-size: 1.8rem; margin-top: 20px; }
        h3 { font-size: 1.4rem; color: var(--gold-secondary) !important; }

        /* Header */
        [data-testid="stHeader"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-bottom: 1px solid #1f1f1f;
        }

        [data-testid="stHeader"] * {
            color: #FFFFFF !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #000000;
            border-right: 1px solid #333;
        }
        
        /* Force all sidebar text to be white */
        [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
        
        /* Specific fix for navigation links */
        [data-testid="stSidebarNav"] span {
            color: #FFFFFF !important;
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background-color: var(--bg-card);
            border: 1px solid #333;
            border-left: 3px solid var(--gold-primary);
            padding: 20px;
            border-radius: 0px; /* Sharp edges for modern look */
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            transition: transform 0.2s;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: var(--gold-secondary);
        }

        [data-testid="stMetricLabel"] {
            color: var(--text-muted) !important;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        [data-testid="stMetricValue"] {
            color: var(--gold-primary) !important;
            font-family: 'Cinzel', serif;
            font-size: 2rem !important;
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            border: 1px solid #333;
            background-color: var(--bg-card);
        }
        
        [data-testid="stDataFrame"] th {
            background-color: #1A1A1A !important;
            color: var(--gold-primary) !important;
            font-family: 'Cinzel', serif;
            border-bottom: 1px solid var(--gold-dim) !important;
        }
        
        [data-testid="stDataFrame"] td {
            color: var(--text-main) !important;
            background-color: var(--bg-card) !important;
            border-bottom: 1px solid #222 !important;
        }

        /* Custom HTML tables (pyarrow fallback) */
        .lux-table-wrapper {
            overflow-x: auto;
            border: 1px solid #333;
            background-color: var(--bg-card);
            margin-bottom: 2rem;
        }

        table.lux-table {
            width: 100%;
            border-collapse: collapse;
            color: var(--text-main);
            font-family: 'Lato', sans-serif;
            table-layout: fixed;
        }

        table.lux-table th {
            background-color: #1A1A1A;
            color: var(--gold-primary);
            text-transform: uppercase;
            font-size: 0.85rem;
            border-bottom: 1px solid var(--gold-dim);
            padding: 12px 16px;
            text-align: center;
        }

        table.lux-table td {
            padding: 12px 16px;
            border-bottom: 1px solid #222;
            text-align: center;
        }

        /* Profile info cards */
        .profile-card {
            background: linear-gradient(135deg, #151515, #1E1E1E);
            border: 1px solid #333;
            padding: 18px;
            border-radius: 6px;
            color: #FFFFFF;
            min-height: 70px;
        }

        .profile-card .profile-label {
            display: block;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 1px;
            color: #B5B5B5;
            margin-bottom: 6px;
        }

        .profile-card .profile-value {
            font-size: 1.1rem;
            font-weight: 600;
            color: #FFFFFF;
        }

        /* Inputs & Selectboxes */
        .stTextInput > div > div > input, .stSelectbox > div > div {
            background-color: #1A1A1A;
            color: var(--text-main);
            border: 1px solid #333;
            border-radius: 0px;
        }

        .stNumberInput input, .stDateInput input, .stTimeInput input {
            background-color: #1A1A1A;
            color: var(--text-main);
            border: 1px solid #333;
            border-radius: 0px;
        }

        /* Placeholder text */
        .stTextInput input::placeholder,
        .stSelectbox input::placeholder,
        .stNumberInput input::placeholder,
        .stDateInput input::placeholder,
        .stTimeInput input::placeholder,
        textarea::placeholder {
            color: #FFFFFF !important;
            opacity: 0.75;
        }

        /* Disabled inputs & placeholders */
        input:disabled,
        textarea:disabled,
        select:disabled {
            color: #FFFFFF !important;
            opacity: 1;
        }

        input:disabled::placeholder,
        textarea:disabled::placeholder,
        select:disabled::placeholder {
            color: #FFFFFF !important;
            opacity: 0.9;
        }
        
        /* Widget Labels - Fix for invisible text */
        .stTextInput label, .stSelectbox label, .stSlider label, .stNumberInput label {
            color: #E0E0E0 !important;
            font-weight: 600;
        }
        
        /* Selectbox Menu Fix */
        div[data-baseweb="select"] > div {
            background-color: #1A1A1A !important;
            color: #E0E0E0 !important;
            border-color: #333 !important;
        }
        
        div[data-baseweb="popover"] {
            background-color: #1A1A1A !important;
        }
        
        div[data-baseweb="menu"] {
            background-color: #1A1A1A !important;
        }
        
        .stTextInput > div > div > input:focus, .stSelectbox > div > div:focus {
            border-color: var(--gold-primary);
            box-shadow: none;
        }

        /* Buttons */
        .stButton > button {
            background-color: transparent;
            color: var(--gold-primary);
            border: 1px solid var(--gold-primary);
            border-radius: 0px;
            font-family: 'Cinzel', serif;
            text-transform: uppercase;
            padding: 0.5rem 2rem;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background-color: var(--gold-primary);
            color: #000000;
            border-color: var(--gold-primary);
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent;
            border-bottom: 1px solid #333;
        }

        .stTabs [data-baseweb="tab"] {
            color: var(--text-muted);
            font-family: 'Cinzel', serif;
            border-radius: 0px;
        }

        .stTabs [aria-selected="true"] {
            color: var(--gold-primary) !important;
            background-color: transparent !important;
            border-bottom: 2px solid var(--gold-primary);
        }

        /* Plotly */
        .js-plotly-plot .plotly .main-svg {
            background: transparent !important;
        }
        
        /* Dividers */
        hr {
            border-color: #333;
            margin: 3rem 0;
        }
        
        /* Alerts */
        .stAlert {
            background-color: #1A1A1A;
            border: 1px solid #333;
            color: var(--text-main);
            border-radius: 0px;
        }
    </style>
    """
