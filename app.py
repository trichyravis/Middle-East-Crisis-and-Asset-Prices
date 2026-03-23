
"""
2026 Iran War – US-Israel Operation Epic Fury Market Impact Analyzer
Prof. V. Ravichandran | The Mountain Path - World of Finance
Analyzes Crude Oil, Gold, Silver & Major Stock Indices
Crisis Event: February 28, 2026 – US-Israel Joint Strikes on Iran (Operation Epic Fury)
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import scipy.stats as stats
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="2026 Iran War – Market Impact Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CRISIS EVENT ───────────────────────────────────────────────────────────────
CRISIS_DATE = datetime(2026, 2, 28)
PRE_START   = CRISIS_DATE - timedelta(days=62)   # ~2 months before (Dec 28, 2025)
POST_END    = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)  # always today

# ─── ASSET UNIVERSE ─────────────────────────────────────────────────────────────
ASSETS = {
    "🛢 Energy & Commodities": {
        "Crude Oil (WTI)":    {"ticker": "CL=F",  "color": "#FF6B35", "category": "commodity"},
        "Brent Crude":        {"ticker": "BZ=F",  "color": "#FF9500", "category": "commodity"},
        "Natural Gas":        {"ticker": "NG=F",  "color": "#55EFC4", "category": "commodity"},
        "XLE (Energy ETF)":   {"ticker": "XLE",   "color": "#00B894", "category": "etf"},
    },
    "🪙 Safe Haven & Currencies": {
        "Gold":               {"ticker": "GC=F",    "color": "#FFD700", "category": "commodity"},
        "Silver":             {"ticker": "SI=F",    "color": "#C0C0C0", "category": "commodity"},
        "US 10Y Treasury":    {"ticker": "^TNX",    "color": "#74B9FF", "category": "bond"},
        "DXY (USD Index)":    {"ticker": "DX-Y.NYB","color": "#A29BFE", "category": "currency"},
        "USD/INR":            {"ticker": "INR=X",   "color": "#FF6B9D", "category": "currency"},
    },
    "📈 US Markets": {
        "S&P 500":            {"ticker": "^GSPC", "color": "#00D4FF", "category": "index"},
        "NASDAQ 100":         {"ticker": "^NDX",  "color": "#4ECDC4", "category": "index"},
        "Dow Jones":          {"ticker": "^DJI",  "color": "#45B7D1", "category": "index"},
        "VIX (Fear Index)":   {"ticker": "^VIX",  "color": "#FF4757", "category": "volatility"},
    },
    "🌍 Global Indices": {
        "FTSE 100 (UK)":      {"ticker": "^FTSE", "color": "#6C63FF", "category": "index"},
        "DAX (Germany)":      {"ticker": "^GDAXI","color": "#A29BFE", "category": "index"},
        "Nikkei 225 (Japan)": {"ticker": "^N225", "color": "#FD79A8", "category": "index"},
        "Nifty 50 (India)":   {"ticker": "^NSEI", "color": "#FFEAA7", "category": "index"},
    },
    "🛡 War & Geopolitical Proxies": {
        "ITA (Defense ETF)":  {"ticker": "ITA",      "color": "#E17055", "category": "etf"},
        "LMT (Lockheed)":     {"ticker": "LMT",      "color": "#FD79A8", "category": "stock"},
        "RTX (Raytheon)":     {"ticker": "RTX",      "color": "#FDCB6E", "category": "stock"},
        "Israeli ETF (EIS)":  {"ticker": "EIS",      "color": "#55EFC4", "category": "etf"},
    },
    "₿ Crypto": {
        "Bitcoin (BTC-USD)":  {"ticker": "BTC-USD",  "color": "#F7931A", "category": "crypto"},
        "Ethereum (ETH-USD)": {"ticker": "ETH-USD",  "color": "#627EEA", "category": "crypto"},
    }
}

# Flatten for easy lookup
FLAT_ASSETS = {}
for group, items in ASSETS.items():
    for name, meta in items.items():
        FLAT_ASSETS[name] = meta

# ─── CSS STYLING ─────────────────────────────────────────────────────────────────
st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@300;400;600&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: #1a2332;
    color: #e6f1ff;
}

.stApp {
    background: linear-gradient(135deg, #1a2332 0%, #243447 50%, #2a3f5f 100%);
}

/* Hero Header */
.hero-header {
    background: linear-gradient(135deg, #003366 0%, #004d80 50%, #003366 100%);
    border: 1px solid rgba(0,77,128,0.6);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    user-select: none;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(255,215,0,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #FFD700;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 20px rgba(255,215,0,0.3);
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #a0aec0;
    font-weight: 300;
    margin: 0.2rem 0;
}
.hero-crisis {
    display: inline-block;
    background: rgba(255,71,87,0.15);
    border: 1px solid rgba(255,71,87,0.4);
    border-radius: 20px;
    padding: 0.3rem 1rem;
    color: #ff6b6b;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
}
.hero-brand {
    font-size: 0.85rem;
    color: #667eea;
    margin-top: 1rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* KPI Cards */
.kpi-row {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
    flex-wrap: wrap;
}
.kpi-card {
    background: linear-gradient(135deg, #003366 0%, #112240 100%);
    border: 1px solid rgba(0,77,128,0.4);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    flex: 1;
    min-width: 160px;
    position: relative;
    overflow: hidden;
    user-select: none;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #FFD700);
    border-radius: 12px 12px 0 0;
}
.kpi-label {
    font-size: 0.75rem;
    color: #8892b0;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.4rem;
    color: #8892b0;
    -webkit-text-fill-color: #8892b0;
}
.kpi-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #e6f1ff;
    -webkit-text-fill-color: #e6f1ff;
}
.kpi-change {
    font-size: 0.8rem;
    margin-top: 0.2rem;
    font-family: 'JetBrains Mono', monospace;
}
.pos { color: #28a745; -webkit-text-fill-color: #28a745; }
.neg { color: #dc3545; -webkit-text-fill-color: #dc3545; }
.neu { color: #8892b0; -webkit-text-fill-color: #8892b0; }

/* Section headers */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #FFD700;
    -webkit-text-fill-color: #FFD700;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,215,0,0.2);
    user-select: none;
}

/* Data table */
.styled-table {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
}

/* Crisis badge */
.crisis-badge {
    background: rgba(255,71,87,0.1);
    border: 1px solid rgba(255,71,87,0.3);
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    margin: 1rem 0;
    color: #ff6b6b;
    -webkit-text-fill-color: #ff6b6b;
    user-select: none;
}

/* ── SIDEBAR: background ── */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #003366 0%, #1a2332 100%) !important;
    border-right: 1px solid rgba(0,77,128,0.3);
}
section[data-testid="stSidebar"] .block-container {
    padding: 1rem;
}

/* ── SIDEBAR: ALL text — force light colour ── */
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] h5,
section[data-testid="stSidebar"] h6,
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] small {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}

/* ── SIDEBAR: headings → gold ── */
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] h3 {
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    font-weight: 700 !important;
}

/* ── SIDEBAR: bold text → light blue ── */
section[data-testid="stSidebar"] strong {
    color: #ADD8E6 !important;
    -webkit-text-fill-color: #ADD8E6 !important;
}

/* ── SIDEBAR: checkbox labels ── */
section[data-testid="stSidebar"] [data-testid="stCheckbox"] label,
section[data-testid="stSidebar"] [data-testid="stCheckbox"] span,
section[data-testid="stSidebar"] [data-testid="stCheckbox"] p {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
    font-size: 0.9rem !important;
}

/* ── SIDEBAR: checkbox tick border ── */
section[data-testid="stSidebar"] [data-baseweb="checkbox"] div {
    border-color: #FFD700 !important;
}

/* ── SIDEBAR: links → gold ── */
section[data-testid="stSidebar"] a {
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    text-decoration: none !important;
}
section[data-testid="stSidebar"] a:hover {
    color: #ffe566 !important;
    -webkit-text-fill-color: #ffe566 !important;
    text-decoration: underline !important;
}

/* ── SIDEBAR: stMarkdown and widget label text ── */
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}

/* ── SIDEBAR: hr ── */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,215,0,0.25) !important;
}

/* ── MAIN AREA: global text ── */
.stApp, .stApp * {
    color: #e6f1ff;
}
.stApp p, .stApp span, .stApp li, .stApp td, .stApp th {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}
.stMarkdown p, .stMarkdown span, .stMarkdown li {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}

/* ── MAIN AREA: widget labels ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
[data-testid="stWidgetLabel"] label {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}

/* ── MAIN AREA: checkboxes ── */
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] span {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}

/* ── MAIN AREA: expander — full override ── */
[data-testid="stExpander"] {
    background: #112240 !important;
    border: 1px solid rgba(0,77,128,0.5) !important;
    border-radius: 8px !important;
}

/* Expander header ribbon — the clickable bar */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] > details > summary,
[data-testid="stExpander"] details summary {
    background: linear-gradient(135deg, #003366 0%, #004d80 100%) !important;
    border-radius: 8px !important;
    padding: 0.7rem 1rem !important;
    border-bottom: 1px solid rgba(255,215,0,0.15) !important;
    cursor: pointer !important;
}

/* Every text node inside the header ribbon */
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary label,
[data-testid="stExpander"] summary div,
[data-testid="stExpander"] summary svg {
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    fill: #FFD700 !important;
}

/* Expanded state — keep styling consistent */
[data-testid="stExpander"] details[open] summary {
    background: linear-gradient(135deg, #004d80 0%, #003366 100%) !important;
    border-bottom: 1px solid rgba(255,215,0,0.3) !important;
    border-radius: 8px 8px 0 0 !important;
}

/* ALL content inside expander body */
[data-testid="stExpander"] *,
[data-testid="stExpander"] p,
[data-testid="stExpander"] span,
[data-testid="stExpander"] label,
[data-testid="stExpander"] div {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}

/* ── METRIC: label (the small text above the number) ── */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] span,
[data-testid="stMetricLabel"] div,
[data-testid="stExpander"] [data-testid="stMetricLabel"],
[data-testid="stExpander"] [data-testid="stMetricLabel"] * {
    color: #ADD8E6 !important;
    -webkit-text-fill-color: #ADD8E6 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* ── METRIC: the big number ── */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] p,
[data-testid="stMetricValue"] span,
div[data-testid="stMetricValue"],
[data-testid="stExpander"] [data-testid="stMetricValue"],
[data-testid="stExpander"] [data-testid="stMetricValue"] * {
    font-family: 'JetBrains Mono', monospace !important;
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

/* ── METRIC: delta (the small change badge) ── */
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] *,
[data-testid="stMetricDelta"] p,
[data-testid="stMetricDelta"] span,
[data-testid="stExpander"] [data-testid="stMetricDelta"],
[data-testid="stExpander"] [data-testid="stMetricDelta"] * {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
}
/* Delta positive = green, negative = red — override Streamlit's own colouring */
[data-testid="stMetricDelta"][data-direction="up"] *,
[data-testid="stMetricDelta"][data-direction="up"] {
    color: #28a745 !important;
    -webkit-text-fill-color: #28a745 !important;
}
[data-testid="stMetricDelta"][data-direction="down"] *,
[data-testid="stMetricDelta"][data-direction="down"] {
    color: #dc3545 !important;
    -webkit-text-fill-color: #dc3545 !important;
}

/* ── MAIN AREA: info/warning/error boxes ── */
[data-testid="stInfo"],
[data-testid="stWarning"],
[data-testid="stError"],
[data-testid="stSuccess"] {
    color: #e6f1ff !important;
}
[data-testid="stInfo"] p, [data-testid="stInfo"] span,
[data-testid="stWarning"] p, [data-testid="stWarning"] span,
[data-testid="stError"] p, [data-testid="stError"] span,
[data-testid="stSuccess"] p, [data-testid="stSuccess"] span {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(135deg, #003366 0%, #004d80 100%) !important;
    border-radius: 10px !important;
    padding: 6px !important;
    gap: 4px !important;
    border: 1px solid rgba(255,215,0,0.15) !important;
    flex-wrap: wrap !important;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.04) !important;
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
    border-radius: 7px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.1rem !important;
    border: 1px solid rgba(173,216,230,0.15) !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
    min-height: 42px !important;
}
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255,215,0,0.1) !important;
    border-color: rgba(255,215,0,0.35) !important;
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
}
.stTabs [data-baseweb="tab"]:hover p,
.stTabs [data-baseweb="tab"]:hover span {
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(255,215,0,0.2) 0%, rgba(255,183,0,0.12) 100%) !important;
    border: 1.5px solid rgba(255,215,0,0.55) !important;
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    box-shadow: 0 2px 10px rgba(255,215,0,0.15) !important;
}
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span {
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

/* ── SELECTS ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #003366 !important;
    border-color: rgba(0,77,128,0.5) !important;
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] th {
    background: #003366 !important;
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
}
[data-testid="stDataFrame"] td {
    color: #e6f1ff !important;
    -webkit-text-fill-color: #e6f1ff !important;
}

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] button {
    background: #003366 !important;
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    border: 1px solid rgba(255,215,0,0.4) !important;
    font-weight: 600 !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #004d80 !important;
    border-color: #FFD700 !important;
}

hr { border-color: rgba(255,215,0,0.15) !important; }

/* ── REFRESH BUTTON ── */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #003366 0%, #004d80 100%) !important;
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    border: 1.5px solid #FFD700 !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.3px !important;
    padding: 0.35rem 1rem !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #FFD700 0%, #ffb700 100%) !important;
    color: #003366 !important;
    -webkit-text-fill-color: #003366 !important;
    border-color: #FFD700 !important;
    box-shadow: 0 0 12px rgba(255,215,0,0.4) !important;
}
div[data-testid="stButton"] button p,
div[data-testid="stButton"] button span {
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    font-weight: 700 !important;
}
div[data-testid="stButton"] button:hover p,
div[data-testid="stButton"] button:hover span {
    color: #003366 !important;
    -webkit-text-fill-color: #003366 !important;
}
</style>
""")


# ─── DATA FETCHING ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=21600, show_spinner=False)
def fetch_data(ticker: str, start: datetime, end: datetime) -> pd.DataFrame:
    try:
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[['Close']].copy()
        df.columns = ['Price']
        df.index = pd.to_datetime(df.index)
        df = df.dropna()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=21600, show_spinner=False)
def fetch_all_assets():
    all_data = {}
    for name, meta in FLAT_ASSETS.items():
        df = fetch_data(meta['ticker'], PRE_START - timedelta(days=5), POST_END + timedelta(days=5))
        if not df.empty:
            all_data[name] = df
    return all_data


def compute_metrics(df: pd.DataFrame, crisis_date: datetime) -> dict:
    """Compute pre/post crisis metrics"""
    pre_df  = df[df.index < crisis_date]
    post_df = df[df.index >= crisis_date]

    if pre_df.empty or post_df.empty:
        return {}

    pre_ret  = pre_df['Price'].pct_change().dropna()
    post_ret = post_df['Price'].pct_change().dropna()

    # Normalized to crisis day (first available price)
    pre_norm  = (pre_df['Price'] / pre_df['Price'].iloc[-1] - 1) * 100
    post_norm = (post_df['Price'] / post_df['Price'].iloc[0] - 1) * 100

    # t-test: is post mean return significantly different from pre?
    t_stat, p_val = stats.ttest_ind(post_ret, pre_ret) if (len(pre_ret) > 3 and len(post_ret) > 3) else (np.nan, np.nan)

    return {
        "pre_start_price":  pre_df['Price'].iloc[0],
        "pre_end_price":    pre_df['Price'].iloc[-1],
        "post_start_price": post_df['Price'].iloc[0],
        "post_end_price":   post_df['Price'].iloc[-1],
        "pre_return_pct":   ((pre_df['Price'].iloc[-1] / pre_df['Price'].iloc[0]) - 1) * 100,
        "post_return_pct":  ((post_df['Price'].iloc[-1] / post_df['Price'].iloc[0]) - 1) * 100,
        "pre_volatility":   pre_ret.std() * np.sqrt(252) * 100,
        "post_volatility":  post_ret.std() * np.sqrt(252) * 100,
        "pre_sharpe":       (pre_ret.mean() / pre_ret.std() * np.sqrt(252)) if pre_ret.std() > 0 else np.nan,
        "post_sharpe":      (post_ret.mean() / post_ret.std() * np.sqrt(252)) if post_ret.std() > 0 else np.nan,
        "pre_max_dd":       ((pre_df['Price'] / pre_df['Price'].cummax()) - 1).min() * 100,
        "post_max_dd":      ((post_df['Price'] / post_df['Price'].cummax()) - 1).min() * 100,
        "t_stat":           t_stat,
        "p_val":            p_val,
        "pre_df":           pre_df,
        "post_df":          post_df,
        "pre_norm":         pre_norm,
        "post_norm":        post_norm,
    }


# ─── PLOT HELPERS ────────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26,35,50,0.85)',
    font=dict(family='Source Sans 3, sans-serif', color='#e6f1ff', size=12),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.05)',
        linecolor='rgba(255,255,255,0.1)',
        tickfont=dict(family='JetBrains Mono', size=10),
        showspikes=True, spikecolor='rgba(255,215,0,0.4)', spikethickness=1
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.05)',
        linecolor='rgba(255,255,255,0.1)',
        tickfont=dict(family='JetBrains Mono', size=10),
        showspikes=True, spikecolor='rgba(255,215,0,0.4)', spikethickness=1
    ),
    hovermode='x unified',
    legend=dict(
        bgcolor='rgba(10,15,30,0.8)',
        bordercolor='rgba(255,215,0,0.2)',
        borderwidth=1,
        font=dict(size=11)
    ),
    margin=dict(l=60, r=30, t=50, b=50)
)

CRISIS_DATE_STR = CRISIS_DATE.strftime("%Y-%m-%d")

def add_crisis_line(fig, row=None, col=None):
    """
    add_vline with annotation is broken in Plotly 6.x for datetime axes
    (shapeannotation._mean fails on timestamp arithmetic).
    Use add_shape + add_annotation instead — fully equivalent, no bug.
    """
    shape_kwargs = dict(row=row, col=col) if row else {}
    annot_kwargs = dict(row=row, col=col) if row else {}

    fig.add_shape(
        type="line",
        x0=CRISIS_DATE_STR, x1=CRISIS_DATE_STR,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(color="rgba(255,71,87,0.8)", width=2, dash="dash"),
        **shape_kwargs
    )
    fig.add_annotation(
        x=CRISIS_DATE_STR,
        y=1.0,
        xref="x", yref="paper",
        text="💥 Feb 28 Op.Epic Fury",
        showarrow=False,
        font=dict(color="#ff6b6b", size=11),
        xanchor="left",
        yanchor="bottom",
        bgcolor="rgba(26,35,50,0.7)",
        bordercolor="rgba(255,71,87,0.4)",
        borderwidth=1,
        **annot_kwargs
    )


# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1rem 0; user-select:none;'>
        <div style='font-family:Playfair Display,serif; font-size:1.3rem; color:#FFD700; -webkit-text-fill-color:#FFD700; font-weight:700;'>
            The Mountain Path
        </div>
        <div style='font-size:0.75rem; color:#8892b0; -webkit-text-fill-color:#8892b0; margin-top:4px;'>World of Finance</div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("#### 🗓 Crisis Timeline")
    st.markdown("""
    <div style='background:rgba(255,71,87,0.08); border:1px solid rgba(255,71,87,0.35); border-radius:8px;
                padding:0.9rem 1.2rem; margin:0.5rem 0; user-select:none; line-height:1.7;'>
        <div style='color:#FFD700;-webkit-text-fill-color:#FFD700;font-size:0.72rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;'>Escalation Timeline</div>
        <div style='font-size:0.79rem;'>
        <span style='color:#ff9966;-webkit-text-fill-color:#ff9966;font-weight:700;'>Jun 13 2025</span>
        <span style='color:#c8d6e5;-webkit-text-fill-color:#c8d6e5;'> — 12-Day War: Israel strikes Iran nuclear sites</span><br>
        <span style='color:#ff9966;-webkit-text-fill-color:#ff9966;font-weight:700;'>Dec 28 2025</span>
        <span style='color:#c8d6e5;-webkit-text-fill-color:#c8d6e5;'> — Mass protests erupt across Iran</span><br>
        <span style='color:#ff9966;-webkit-text-fill-color:#ff9966;font-weight:700;'>Feb 6 2026</span>
        <span style='color:#c8d6e5;-webkit-text-fill-color:#c8d6e5;'> — US-Iran nuclear talks begin in Geneva</span><br>
        <span style='color:#ff6b6b;-webkit-text-fill-color:#ff6b6b;font-weight:700;'>Feb 28 2026</span>
        <span style='color:#ff6b6b;-webkit-text-fill-color:#ff6b6b;font-weight:700;'> — Op. Epic Fury: US+Israel strike Iran ★</span><br>
        <span style='color:#ff9966;-webkit-text-fill-color:#ff9966;font-weight:700;'>Mar 1 2026</span>
        <span style='color:#c8d6e5;-webkit-text-fill-color:#c8d6e5;'> — Iran retaliates: 500+ missiles &amp; drones</span><br>
        <span style='color:#ff9966;-webkit-text-fill-color:#ff9966;font-weight:700;'>Mar 2026</span>
        <span style='color:#c8d6e5;-webkit-text-fill-color:#c8d6e5;'> — Strait of Hormuz closed, Brent &gt;$100</span>
        </div>
        <div style='font-size:0.72rem;color:#8892b0;-webkit-text-fill-color:#8892b0;margin-top:6px;'>★ = Reference crisis date (Feb 28, 2026)</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📦 Select Assets")
    selected = []
    for group, items in ASSETS.items():
        st.markdown(f"**{group}**")
        for name in items:
            if st.checkbox(name, value=name in [
                "Crude Oil (WTI)", "Brent Crude", "Gold",
                "S&P 500", "VIX (Fear Index)",
                "ITA (Defense ETF)", "LMT (Lockheed)", "RTX (Raytheon)",
                "US 10Y Treasury", "DXY (USD Index)", "USD/INR", "Bitcoin (BTC-USD)"
            ], key=f"cb_{name}"):
                selected.append(name)

    st.markdown("---")
    st.markdown("#### ⚙ Chart Options")
    normalize = st.checkbox("Normalize to Crisis Date", value=True,
                            help="Show % change from Feb 28, 2026 — Operation Epic Fury launch day")
    show_vol  = st.checkbox("Show Volatility Band", value=False)
    log_scale = st.checkbox("Log Y-Axis", value=False)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#667eea; -webkit-text-fill-color:#667eea; text-align:center; user-select:none;'>
        Prof. V. Ravichandran<br>
        28+ Yrs Corporate Finance &amp; Banking<br>
        10+ Yrs Academic Excellence<br><br>
        <a href='https://themountainpathacademy.com' style='color:#FFD700; -webkit-text-fill-color:#FFD700;'>
        🌐 themountainpathacademy.com</a><br><br>
        <a href='https://www.linkedin.com/in/trichyravis' style='color:#FFD700; -webkit-text-fill-color:#FFD700;'>LinkedIn</a>
        &nbsp;|&nbsp;
        <a href='https://github.com/trichyravis' style='color:#FFD700; -webkit-text-fill-color:#FFD700;'>GitHub</a>
    </div>
    """, unsafe_allow_html=True)


# ─── HERO HEADER ─────────────────────────────────────────────────────────────────
st.html("""
<div class='hero-header'>
    <div class='hero-title'>2026 Iran War – Operation Epic Fury: Market Impact Analyzer</div>
    <div class='hero-subtitle'>Crude Oil · Gold · Silver · Strait of Hormuz Risk · Defense Stocks · Safe-Haven Flight</div>
    <div class='hero-crisis'>💥 Feb 28, 2026 — US &amp; Israel launch Operation Epic Fury on Iran | Strait of Hormuz Closed</div>
    <div class='hero-brand'>
        The Mountain Path – World of Finance &nbsp;|&nbsp; Prof. V. Ravichandran
        &nbsp;|&nbsp; <a href='https://themountainpathacademy.com' style='color:#FFD700;'>themountainpathacademy.com</a>
    </div>
</div>
""")


# ─── FLASH SUMMARY BANNER ────────────────────────────────────────────────────────
st.markdown("""
<div style='
    background: linear-gradient(90deg, rgba(255,71,87,0.12) 0%, rgba(255,165,0,0.1) 50%, rgba(255,71,87,0.12) 100%);
    border: 1px solid rgba(255,120,50,0.45);
    border-left: 4px solid #FF4757;
    border-radius: 8px;
    padding: 0.75rem 1.4rem;
    margin-bottom: 1rem;
    user-select: none;
    animation: pulse-border 3s ease-in-out infinite;
'>
<span style='color:#FF4757;-webkit-text-fill-color:#FF4757;font-weight:700;font-size:0.85rem;letter-spacing:0.5px;'>
⚡ LIVE STUDY &nbsp;|&nbsp;
</span>
<span style='color:#FFD700;-webkit-text-fill-color:#FFD700;font-weight:700;font-size:0.85rem;'>
2026 Iran War — Operation Epic Fury &nbsp;|&nbsp;
</span>
<span style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;font-size:0.85rem;'>
US &amp; Israel struck Iran on <strong style='color:#ff9966;-webkit-text-fill-color:#ff9966;'>Feb 28, 2026</strong>.
Strait of Hormuz closed. Brent crude surged past <strong style='color:#ff9966;-webkit-text-fill-color:#ff9966;'>$100/bbl</strong>.
Gold, Defense ETFs &amp; DXY spiked. INR depreciated on risk-off flows. Bitcoin tested its safe-haven narrative. Global equity markets fell sharply.
This tool compares market behaviour <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>2 months before</strong> vs
<strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>post-war</strong> across 23 assets — Commodities, Equities, Currencies, Crypto &amp; Defense — in real time.
</span>
</div>
""", unsafe_allow_html=True)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────────
# ─── LAST UPDATED + REFRESH ─────────────────────────────────────────────────────
_now = datetime.now()
_market_note = "Markets closed — showing last close prices" if _now.weekday() >= 5 else "Live market data"
rc1, rc2, rc3 = st.columns([3, 1, 1])
with rc1:
    st.markdown(
        f"<span style='font-size:0.78rem;color:#8892b0;-webkit-text-fill-color:#8892b0;'>"
        f"🕐 Data as of: <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>"
        f"{_now.strftime('%d %b %Y, %H:%M IST')}</strong> &nbsp;|&nbsp; {_market_note} "
        f"&nbsp;|&nbsp; Cache refreshes every 6 hours</span>",
        unsafe_allow_html=True
    )
with rc2:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
with rc3:
    st.markdown(
        f"<span style='font-size:0.78rem;color:#8892b0;-webkit-text-fill-color:#8892b0;'>"
        f"📅 Post-war window: <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>"
        f"{POST_END.strftime('%d %b %Y')}</strong></span>",
        unsafe_allow_html=True
    )

with st.spinner("⏳ Fetching real-time market data from Yahoo Finance…"):
    all_data = fetch_all_assets()

if not selected:
    st.warning("⚠ Please select at least one asset from the sidebar.")
    st.stop()

# Filter to selected & available
available = [a for a in selected if a in all_data and not all_data[a].empty]
if not available:
    st.error("No data available for selected assets. Please check your connection.")
    st.stop()

# Trim to analysis window
trimmed = {}
for name in available:
    df = all_data[name]
    mask = (df.index >= PRE_START) & (df.index <= POST_END)
    trimmed[name] = df[mask]


# ─── TABS ────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 Price Dashboard",
    "📉 Normalized Returns",
    "⚖ Pre vs Post Analysis",
    "🌡 Volatility & Risk",
    "🔗 Correlation Matrix",
    "📋 Statistical Summary",
    "ℹ About This Project",
])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1: PRICE DASHBOARD
# ════════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.html("<div class='section-header'>Raw Price Trajectories</div>")
    st.markdown(f"*Analysis window: {PRE_START.strftime('%d %b %Y')} → {POST_END.strftime('%d %b %Y')} | Crisis: Feb 28, 2026 (Op. Epic Fury)*")

    # USD/INR spotlight note
    if "USD/INR" in available:
        st.markdown("""
        <div style='background:rgba(255,107,157,0.08);border:1px solid rgba(255,107,157,0.3);
                    border-left:3px solid #FF6B9D;border-radius:6px;padding:0.6rem 1.1rem;
                    margin-bottom:0.5rem;font-size:0.82rem;'>
        <span style='color:#FF6B9D;-webkit-text-fill-color:#FF6B9D;font-weight:700;'>🇮🇳 USD/INR Watch</span>
        <span style='color:#c8d6e5;-webkit-text-fill-color:#c8d6e5;'>
        &nbsp;— A rising USD/INR means INR depreciation (more rupees per dollar).
        During geopolitical crises, risk-off flows strengthen USD and weaken EM currencies like INR.
        Compare the pre-war vs post-war slope to measure the rupee's stress response.
        </span>
        </div>""", unsafe_allow_html=True)

    # Bitcoin spotlight note
    if "Bitcoin (BTC-USD)" in available:
        st.markdown("""
        <div style='background:rgba(247,147,26,0.08);border:1px solid rgba(247,147,26,0.3);
                    border-left:3px solid #F7931A;border-radius:6px;padding:0.6rem 1.1rem;
                    margin-bottom:0.5rem;font-size:0.82rem;'>
        <span style='color:#F7931A;-webkit-text-fill-color:#F7931A;font-weight:700;'>₿ Bitcoin Watch</span>
        <span style='color:#c8d6e5;-webkit-text-fill-color:#c8d6e5;'>
        &nbsp;— Bitcoin trades 24×7 and reacts instantly to geopolitical shocks.
        Watch whether BTC behaves as a <strong style='color:#FFD700;-webkit-text-fill-color:#FFD700;'>safe-haven (like Gold)</strong>
        or a <strong style='color:#FF4757;-webkit-text-fill-color:#FF4757;'>risk asset (like equities)</strong>
        in the pre-war vs post-war periods. Correlation with Gold vs VIX tells the story.
        </span>
        </div>""", unsafe_allow_html=True)

    # KPI Row
    st.html("<div class='kpi-row'>")
    kpi_cols = st.columns(min(len(available), 5))
    for i, name in enumerate(available[:5]):
        df = trimmed[name]
        if df.empty: continue
        pre  = df[df.index < CRISIS_DATE]
        post = df[df.index >= CRISIS_DATE]
        if pre.empty or post.empty: continue
        chg = ((post['Price'].iloc[-1] / post['Price'].iloc[0]) - 1) * 100
        color_cls = "pos" if chg >= 0 else "neg"
        color_hex  = "#28a745" if chg >= 0 else "#dc3545"
        with kpi_cols[i]:
            arrow = "▲" if chg >= 0 else "▼"
            kpi_html = f"""
            <div class='kpi-card' style='--accent:{FLAT_ASSETS[name]["color"]};' user-select='none'>
                <div class='kpi-label' style='color:#8892b0;-webkit-text-fill-color:#8892b0;'>{name}</div>
                <div class='kpi-value' style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;font-family:JetBrains Mono,monospace;font-size:1.4rem;font-weight:600;'>{post['Price'].iloc[-1]:.2f}</div>
                <div style='font-size:0.8rem;margin-top:0.2rem;font-family:JetBrains Mono,monospace;color:{color_hex};-webkit-text-fill-color:{color_hex};'>Post-Crisis: {arrow} {abs(chg):.1f}%</div>
            </div>
            """
            st.html(kpi_html)

    # Individual price charts per asset (4 columns layout)
    n = len(available)
    ncols = min(2, n)
    rows_needed = (n + ncols - 1) // ncols

    for row_i in range(rows_needed):
        cols = st.columns(ncols)
        for col_i in range(ncols):
            asset_i = row_i * ncols + col_i
            if asset_i >= n:
                break
            name = available[asset_i]
            df   = trimmed[name]
            color = FLAT_ASSETS[name]['color']

            with cols[col_i]:
                fig = go.Figure()

                # Pre-crisis area
                pre_df  = df[df.index < CRISIS_DATE]
                post_df = df[df.index >= CRISIS_DATE]

                if not pre_df.empty:
                    _h = color.lstrip('#')
                    _r,_g,_b = int(_h[0:2],16), int(_h[2:4],16), int(_h[4:6],16)
                    fig.add_trace(go.Scatter(
                        x=pre_df.index, y=pre_df['Price'],
                        mode='lines',
                        name='Pre-Crisis',
                        line=dict(color=color, width=2),
                        fill='tozeroy',
                        fillcolor=f'rgba({_r},{_g},{_b},0.12)',
                    ))

                if not post_df.empty:
                    fig.add_trace(go.Scatter(
                        x=post_df.index, y=post_df['Price'],
                        mode='lines',
                        name='Post-Crisis',
                        line=dict(color='#ff6b6b', width=2.5),
                        fill='tozeroy',
                        fillcolor='rgba(255,107,107,0.08)',
                    ))

                if show_vol and len(df) > 10:
                    rolling_std = df['Price'].pct_change().rolling(5).std() * df['Price']
                    fig.add_trace(go.Scatter(
                        x=df.index, y=df['Price'] + rolling_std,
                        mode='lines', line=dict(color='rgba(255,255,255,0.1)', width=0),
                        showlegend=False, name='Vol Upper'))
                    fig.add_trace(go.Scatter(
                        x=df.index, y=df['Price'] - rolling_std,
                        mode='lines', line=dict(color='rgba(255,255,255,0.1)', width=0),
                        fill='tonexty', fillcolor='rgba(255,255,255,0.04)',
                        showlegend=False, name='Vol Band'))

                add_crisis_line(fig)

                layout = CHART_LAYOUT.copy()
                layout.update(title=dict(text=name, font=dict(color=color, size=13)), height=280)
                if log_scale:
                    layout['yaxis'] = dict(**layout['yaxis'], type='log')
                fig.update_layout(**layout)
                st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2: NORMALIZED RETURNS
# ════════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.html("<div class='section-header'>Normalized Returns – All Assets (Indexed to Feb 28, 2026 = 0%)</div>")

    if normalize:
        fig = go.Figure()
        for name in available:
            df = trimmed[name]
            if df.empty: continue
            color = FLAT_ASSETS[name]['color']

            # Find Feb 28 2026 price or closest
            ref_candidates = df[df.index >= CRISIS_DATE]
            if ref_candidates.empty: continue
            ref_price = ref_candidates['Price'].iloc[0]

            norm = (df['Price'] / ref_price - 1) * 100

            fig.add_trace(go.Scatter(
                x=norm.index, y=norm.values,
                mode='lines', name=name,
                line=dict(color=color, width=2),
                hovertemplate=f"<b>{name}</b><br>%{{x|%d %b %Y}}<br>%{{y:.2f}}%<extra></extra>"
            ))

        fig.add_hline(y=0, line=dict(color='rgba(255,215,0,0.4)', width=1, dash='dot'))
        add_crisis_line(fig)

        # Shade pre-crisis region
        fig.add_shape(
            type="rect",
            x0=PRE_START.strftime("%Y-%m-%d"), x1=CRISIS_DATE_STR,
            y0=0, y1=1, xref="x", yref="paper",
            fillcolor="rgba(0,100,255,0.04)", line_width=0
        )
        fig.add_annotation(
            x=PRE_START.strftime("%Y-%m-%d"), y=0.97,
            xref="x", yref="paper",
            text="Pre-Crisis Period", showarrow=False,
            font=dict(color="#667eea", size=11),
            xanchor="left", yanchor="top",
            bgcolor="rgba(26,35,50,0.0)"
        )
        # Shade post-crisis region
        fig.add_shape(
            type="rect",
            x0=CRISIS_DATE_STR, x1=POST_END.strftime("%Y-%m-%d"),
            y0=0, y1=1, xref="x", yref="paper",
            fillcolor="rgba(255,71,87,0.04)", line_width=0
        )
        fig.add_annotation(
            x=POST_END.strftime("%Y-%m-%d"), y=0.97,
            xref="x", yref="paper",
            text="Post-Crisis Period", showarrow=False,
            font=dict(color="#ff6b6b", size=11),
            xanchor="right", yanchor="top",
            bgcolor="rgba(26,35,50,0.0)"
        )

        layout = CHART_LAYOUT.copy()
        layout.update(
            title="% Change from Feb 28, 2026 — Operation Epic Fury Launch Day",
            height=520,
            yaxis_title="% Return vs Crisis Day",
            xaxis_title="Date"
        )
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

    # Cumulative return bar
    st.markdown("#### 📊 Cumulative Return Comparison: Pre vs Post Crisis")
    pre_rets  = []
    post_rets = []
    labels    = []
    colors_list = []

    for name in available:
        df = trimmed[name]
        if df.empty: continue
        pre_df  = df[df.index < CRISIS_DATE]
        post_df = df[df.index >= CRISIS_DATE]
        if pre_df.empty or post_df.empty: continue
        pre_r  = ((pre_df['Price'].iloc[-1] / pre_df['Price'].iloc[0]) - 1) * 100
        post_r = ((post_df['Price'].iloc[-1] / post_df['Price'].iloc[0]) - 1) * 100
        labels.append(name)
        pre_rets.append(pre_r)
        post_rets.append(post_r)
        colors_list.append(FLAT_ASSETS[name]['color'])

    if labels:
        fig2 = go.Figure()
        def hex_to_rgba(h, a=0.6):
            h = h.lstrip('#')
            r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
            return f'rgba({r},{g},{b},{a})'

        fig2.add_trace(go.Bar(
            name='Pre-Crisis (~2 months)',
            x=labels, y=pre_rets,
            marker_color=[hex_to_rgba(c, 0.55) for c in colors_list],
            marker_line_color=colors_list,
            marker_line_width=2,
        ))
        fig2.add_trace(go.Bar(
            name='Post-Crisis (~2 months)',
            x=labels, y=post_rets,
            marker_color=['rgba(255,107,107,0.6)' if v < 0 else 'rgba(40,167,69,0.6)' for v in post_rets],
            marker_line_color=['#dc3545' if v < 0 else '#28a745' for v in post_rets],
            marker_line_width=2,
        ))
        fig2.add_hline(y=0, line=dict(color='rgba(255,255,255,0.3)', width=1))

        layout2 = CHART_LAYOUT.copy()
        layout2.update(
            barmode='group',
            title="Cumulative % Return: 2 Months Before vs Post-Feb 28, 2026 US-Israel Strikes on Iran",
            height=420,
            yaxis_title="% Return",
            xaxis_tickangle=-30
        )
        fig2.update_layout(**layout2)
        st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3: PRE vs POST ANALYSIS
# ════════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("<div class='section-header'>Pre vs Post Crisis – Detailed Comparison</div>", unsafe_allow_html=True)

    for name in available:
        df = trimmed[name]
        if df.empty: continue
        m = compute_metrics(df, CRISIS_DATE)
        if not m: continue

        color = FLAT_ASSETS[name]['color']
        post_better = m['post_return_pct'] > m['pre_return_pct']

        with st.expander(f"{'📈' if m['post_return_pct']>=0 else '📉'} {name}", expanded=False):
            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Pre-Crisis Return",
                          f"{m['pre_return_pct']:.2f}%",
                          delta=None)
                st.metric("Pre Volatility (Ann.)",
                          f"{m['pre_volatility']:.1f}%")

            with c2:
                st.metric("Post-Crisis Return",
                          f"{m['post_return_pct']:.2f}%",
                          delta=f"{m['post_return_pct'] - m['pre_return_pct']:.2f}% vs pre")
                st.metric("Post Volatility (Ann.)",
                          f"{m['post_volatility']:.1f}%",
                          delta=f"{m['post_volatility'] - m['pre_volatility']:.1f}%")

            with c3:
                st.metric("Pre Max Drawdown",
                          f"{m['pre_max_dd']:.2f}%")
                st.metric("Pre Sharpe Ratio",
                          f"{m['pre_sharpe']:.2f}" if not np.isnan(m['pre_sharpe']) else "N/A")

            with c4:
                st.metric("Post Max Drawdown",
                          f"{m['post_max_dd']:.2f}%",
                          delta=f"{m['post_max_dd'] - m['pre_max_dd']:.2f}%")
                st.metric("Post Sharpe Ratio",
                          f"{m['post_sharpe']:.2f}" if not np.isnan(m['post_sharpe']) else "N/A")

            # Statistical significance
            if not np.isnan(m['p_val']):
                sig = "✅ Statistically Significant" if m['p_val'] < 0.05 else "⚠ Not Significant at 5%"
                st.info(f"**t-test:** t = {m['t_stat']:.3f}, p-value = {m['p_val']:.4f} | {sig}")

            # Mini price chart with dual-color
            fig = go.Figure()
            pre_df  = m['pre_df']
            post_df = m['post_df']

            fig.add_trace(go.Scatter(x=pre_df.index, y=pre_df['Price'],
                mode='lines', name='Pre', line=dict(color='#667eea', width=2)))
            fig.add_trace(go.Scatter(x=post_df.index, y=post_df['Price'],
                mode='lines', name='Post', line=dict(color=color, width=2)))
            add_crisis_line(fig)

            mini_layout = CHART_LAYOUT.copy()
            mini_layout.update(height=220, margin=dict(l=40, r=20, t=30, b=30), showlegend=True)
            fig.update_layout(**mini_layout)
            st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4: VOLATILITY & RISK
# ════════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.html("<div class='section-header'>Volatility Regime Shift & Risk Metrics</div>")

    c1, c2 = st.columns(2)

    # Rolling Volatility
    with c1:
        st.markdown("#### 30-Day Rolling Volatility (Annualized)")
        fig = go.Figure()
        for name in available:
            df = trimmed[name]
            if df.empty or len(df) < 15: continue
            color = FLAT_ASSETS[name]['color']
            rets = df['Price'].pct_change().dropna()
            roll_vol = rets.rolling(15).std() * np.sqrt(252) * 100
            fig.add_trace(go.Scatter(
                x=roll_vol.index, y=roll_vol.values,
                mode='lines', name=name,
                line=dict(color=color, width=1.8),
                hovertemplate=f"<b>{name}</b><br>%{{x|%d %b %Y}}<br>Vol: %{{y:.1f}}%<extra></extra>"
            ))
        add_crisis_line(fig)
        layout = CHART_LAYOUT.copy()
        layout.update(height=380, yaxis_title="Annualized Volatility (%)")
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

    # Volatility Comparison Bar
    with c2:
        st.markdown("#### Pre vs Post Volatility Shift")
        vol_data = []
        for name in available:
            df = trimmed[name]
            if df.empty: continue
            m = compute_metrics(df, CRISIS_DATE)
            if m:
                vol_data.append({
                    'Asset': name[:20],
                    'Pre Vol': round(m['pre_volatility'], 1),
                    'Post Vol': round(m['post_volatility'], 1),
                    'Vol Change': round(m['post_volatility'] - m['pre_volatility'], 1),
                    'Color': FLAT_ASSETS[name]['color']
                })

        if vol_data:
            vdf = pd.DataFrame(vol_data)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                name='Pre-Crisis Vol', x=vdf['Asset'], y=vdf['Pre Vol'],
                marker_color='rgba(102,126,234,0.7)', marker_line_color='#667eea', marker_line_width=1.5))
            fig2.add_trace(go.Bar(
                name='Post-Crisis Vol', x=vdf['Asset'], y=vdf['Post Vol'],
                marker_color=[('rgba(220,53,69,0.7)' if v>0 else 'rgba(40,167,69,0.7)') for v in vdf['Vol Change']],
                marker_line_color=['#dc3545' if v>0 else '#28a745' for v in vdf['Vol Change']],
                marker_line_width=1.5))
            layout2 = CHART_LAYOUT.copy()
            layout2.update(barmode='group', height=380,
                           yaxis_title="Annualized Volatility (%)", xaxis_tickangle=-30)
            fig2.update_layout(**layout2)
            st.plotly_chart(fig2, use_container_width=True)

    # Return Distribution
    st.markdown("#### Return Distribution: Pre vs Post Crisis")
    dist_cols = st.columns(min(len(available), 4))

    for i, name in enumerate(available[:4]):
        df = trimmed[name]
        if df.empty: continue
        color = FLAT_ASSETS[name]['color']
        pre_ret  = df[df.index < CRISIS_DATE]['Price'].pct_change().dropna() * 100
        post_ret = df[df.index >= CRISIS_DATE]['Price'].pct_change().dropna() * 100

        with dist_cols[i % len(dist_cols)]:
            fig3 = go.Figure()
            if len(pre_ret) > 5:
                fig3.add_trace(go.Histogram(
                    x=pre_ret, name='Pre', opacity=0.6,
                    marker_color='#667eea', nbinsx=20, histnorm='probability density'))
            if len(post_ret) > 5:
                fig3.add_trace(go.Histogram(
                    x=post_ret, name='Post', opacity=0.6,
                    marker_color=color, nbinsx=20, histnorm='probability density'))

            layout3 = CHART_LAYOUT.copy()
            layout3.update(
                barmode='overlay', height=250,
                title=dict(text=name[:18], font=dict(color=color, size=11)),
                margin=dict(l=30, r=10, t=35, b=30),
                showlegend=True
            )
            fig3.update_layout(**layout3)
            st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 5: CORRELATION MATRIX
# ════════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("<div class='section-header'>Cross-Asset Correlation: Pre vs Post Crisis</div>", unsafe_allow_html=True)

    def build_corr(data_dict, names, crisis, period='pre'):
        price_df = pd.DataFrame()
        for name in names:
            df = data_dict.get(name, pd.DataFrame())
            if df.empty: continue
            if period == 'pre':
                sub = df[df.index < crisis]['Price']
            else:
                sub = df[df.index >= crisis]['Price']
            price_df[name[:15]] = sub

        if price_df.empty or len(price_df) < 5:
            return None
        rets = price_df.pct_change().dropna()
        return rets.corr()

    pre_corr  = build_corr(trimmed, available, CRISIS_DATE, 'pre')
    post_corr = build_corr(trimmed, available, CRISIS_DATE, 'post')

    col1, col2 = st.columns(2)

    def plot_corr(corr_df, title, colorscale):
        if corr_df is None:
            return go.Figure()
        z = corr_df.values
        labels = list(corr_df.columns)
        text = [[f"{v:.2f}" for v in row] for row in z]

        fig = go.Figure(go.Heatmap(
            z=z, x=labels, y=labels,
            text=text, texttemplate="%{text}",
            colorscale=colorscale,
            zmid=0, zmin=-1, zmax=1,
            colorbar=dict(title="ρ", tickfont=dict(family='JetBrains Mono', size=10)),
            hoverongaps=False
        ))
        layout = CHART_LAYOUT.copy()
        layout.update(
            title=title, height=480,
            xaxis=dict(**layout['xaxis'], tickangle=-30),
            yaxis=dict(**layout['yaxis'], autorange='reversed')
        )
        fig.update_layout(**layout)
        return fig

    with col1:
        fig_pre = plot_corr(pre_corr, "Pre-War Correlations (Dec 28, 2025 – Feb 27, 2026)",
                            [[0,'#dc3545'],[0.5,'#1a2332'],[1,'#28a745']])
        st.plotly_chart(fig_pre, use_container_width=True)

    with col2:
        fig_post = plot_corr(post_corr, "Post-War Correlations (Feb 28 – Mar 22, 2026)",
                             [[0,'#dc3545'],[0.5,'#1a2332'],[1,'#28a745']])
        st.plotly_chart(fig_post, use_container_width=True)

    # Correlation change
    if pre_corr is not None and post_corr is not None:
        common = list(set(pre_corr.columns) & set(post_corr.columns))
        if common:
            diff = post_corr.loc[common, common] - pre_corr.loc[common, common]
            fig_diff = plot_corr(diff, "Correlation Regime Shift: Pre vs Post Operation Epic Fury (Feb 28, 2026)",
                                 [[0,'#dc3545'],[0.5,'#1a2332'],[1,'#28a745']])
            st.plotly_chart(fig_diff, use_container_width=True)
            st.caption("🔴 Red = correlation increased | 🟢 Green = correlation decreased | White = no change")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 6: STATISTICAL SUMMARY TABLE
# ════════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.html("<div class='section-header'>Comprehensive Statistical Summary</div>")

    rows = []
    for name in available:
        df = trimmed[name]
        if df.empty: continue
        m = compute_metrics(df, CRISIS_DATE)
        if not m: continue

        sig = ""
        if not np.isnan(m.get('p_val', np.nan)):
            sig = "✅" if m['p_val'] < 0.05 else "⚠"

        rows.append({
            "Asset":            name,
            "Pre Return (%)":   round(m['pre_return_pct'], 2),
            "Post Return (%)":  round(m['post_return_pct'], 2),
            "Δ Return (%)":     round(m['post_return_pct'] - m['pre_return_pct'], 2),
            "Pre Vol (%)":      round(m['pre_volatility'], 1),
            "Post Vol (%)":     round(m['post_volatility'], 1),
            "Δ Vol (%)":        round(m['post_volatility'] - m['pre_volatility'], 1),
            "Pre Sharpe":       round(m['pre_sharpe'], 2) if not np.isnan(m['pre_sharpe']) else "N/A",
            "Post Sharpe":      round(m['post_sharpe'], 2) if not np.isnan(m['post_sharpe']) else "N/A",
            "Pre MDD (%)":      round(m['pre_max_dd'], 2),
            "Post MDD (%)":     round(m['post_max_dd'], 2),
            "p-value":          round(m['p_val'], 4) if not np.isnan(m.get('p_val', np.nan)) else "N/A",
            "Sig 5%":           sig,
        })

    if rows:
        summary_df = pd.DataFrame(rows)
        summary_df = summary_df.set_index("Asset")

        def color_cell(val):
            if isinstance(val, (int, float)):
                if val > 0:   return 'color: #28a745'
                elif val < 0: return 'color: #dc3545'
            return ''

        styled = summary_df.style\
            .applymap(color_cell, subset=["Pre Return (%)", "Post Return (%)", "Δ Return (%)",
                                          "Δ Vol (%)", "Pre MDD (%)", "Post MDD (%)"])\
            .set_properties(**{
                'background-color': '#0d1f3c',
                'color': '#e6f1ff',
                'border-color': 'rgba(0,82,204,0.2)',
                'font-family': 'JetBrains Mono, monospace',
                'font-size': '12px',
            })\
            .set_table_styles([{
                'selector': 'th',
                'props': [
                    ('background-color', '#001233'),
                    ('color', '#FFD700'),
                    ('font-family', 'Source Sans 3, sans-serif'),
                    ('font-weight', '600'),
                    ('font-size', '11px'),
                ]
            }])

        st.dataframe(styled, use_container_width=True, height=400)

        # Download
        csv = summary_df.reset_index().to_csv(index=False)
        st.download_button(
            "⬇ Download Summary as CSV",
            data=csv,
            file_name="2026_iran_war_operation_epic_fury_market_analysis.csv",
            mime="text/csv"
        )

    # Key Findings — crypto-aware, category-tagged
    st.markdown("---")
    st.markdown("#### 📝 Key Findings: 2026 Iran War Market Impact")

    CATEGORY_EMOJI = {
        "commodity": "🛢", "etf": "📦", "index": "📈",
        "volatility": "🌡", "bond": "🏦", "currency": "💱",
        "crypto": "₿", "stock": "🏭"
    }

    findings = []
    for name in available:
        df = trimmed[name]
        if df.empty: continue
        m = compute_metrics(df, CRISIS_DATE)
        if not m: continue
        cat  = FLAT_ASSETS[name].get("category", "")
        emoji = CATEGORY_EMOJI.get(cat, "")
        findings.append({
            "name": name, "emoji": emoji, "category": cat,
            "post_ret": m['post_return_pct'],
            "pre_ret":  m['pre_return_pct'],
            "delta":    m['post_return_pct'] - m['pre_return_pct'],
            "post_vol": m['post_volatility'],
            "pre_vol":  m['pre_volatility'],
        })

    # ── Row 1: Winners / Losers ──────────────────────────────────────────────
    kf_c1, kf_c2 = st.columns(2)
    with kf_c1:
        st.markdown("""<div style='color:#28a745;-webkit-text-fill-color:#28a745;
            font-weight:700;font-size:0.95rem;margin-bottom:0.4rem;'>
            🏆 Biggest Post-War Winners</div>""", unsafe_allow_html=True)
        for f in sorted(findings, key=lambda x: x["post_ret"], reverse=True)[:5]:
            st.markdown(f"""<div style='background:rgba(40,167,69,0.08);border-left:3px solid #28a745;
                border-radius:4px;padding:0.35rem 0.8rem;margin-bottom:0.3rem;font-size:0.85rem;'>
                <span style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;font-weight:600;'>
                {f["emoji"]} {f["name"]}</span>
                <span style='color:#28a745;-webkit-text-fill-color:#28a745;float:right;font-family:JetBrains Mono,monospace;font-weight:700;'>
                {f["post_ret"]:+.2f}%</span></div>""", unsafe_allow_html=True)

    with kf_c2:
        st.markdown("""<div style='color:#dc3545;-webkit-text-fill-color:#dc3545;
            font-weight:700;font-size:0.95rem;margin-bottom:0.4rem;'>
            📉 Biggest Post-War Losers</div>""", unsafe_allow_html=True)
        for f in sorted(findings, key=lambda x: x["post_ret"])[:5]:
            st.markdown(f"""<div style='background:rgba(220,53,69,0.08);border-left:3px solid #dc3545;
                border-radius:4px;padding:0.35rem 0.8rem;margin-bottom:0.3rem;font-size:0.85rem;'>
                <span style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;font-weight:600;'>
                {f["emoji"]} {f["name"]}</span>
                <span style='color:#dc3545;-webkit-text-fill-color:#dc3545;float:right;font-family:JetBrains Mono,monospace;font-weight:700;'>
                {f["post_ret"]:+.2f}%</span></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Category-group summaries ─────────────────────────────────────
    kf_c3, kf_c4, kf_c5 = st.columns(3)

    crypto_findings  = [f for f in findings if f["category"] == "crypto"]
    currency_findings = [f for f in findings if f["category"] == "currency"]
    energy_findings  = [f for f in findings if f["category"] == "commodity"]
    defense_findings = [f for f in findings if f["category"] in ("etf","stock") and
                        f["name"] in ("ITA (Defense ETF)","LMT (Lockheed)","RTX (Raytheon)")]
    haven_findings   = [f for f in findings if f["name"] in ("Gold","Silver","US 10Y Treasury")]

    with kf_c3:
        if crypto_findings:
            st.markdown("""<div style='background:#112240;border:1px solid rgba(247,147,26,0.3);
                border-top:3px solid #F7931A;border-radius:8px;padding:1rem 1.2rem;'>
                <div style='color:#F7931A;-webkit-text-fill-color:#F7931A;font-weight:700;
                margin-bottom:0.6rem;'>₿ Crypto Response</div>""", unsafe_allow_html=True)
            for f in crypto_findings:
                color = "#28a745" if f["post_ret"] >= 0 else "#dc3545"
                arrow = "▲" if f["post_ret"] >= 0 else "▼"
                role  = "Safe-Haven ✓" if f["post_ret"] > 0 else "Risk Asset ✗"
                st.markdown(f"""<div style='font-size:0.82rem;margin-bottom:0.4rem;'>
                    <span style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;'>{f["name"]}</span><br>
                    <span style='color:{color};-webkit-text-fill-color:{color};font-family:JetBrains Mono,monospace;'>
                    {arrow} {f["post_ret"]:+.2f}%</span>
                    <span style='color:#8892b0;-webkit-text-fill-color:#8892b0;font-size:0.75rem;'>
                    &nbsp;→ {role}</span></div>""", unsafe_allow_html=True)
            vol_change = np.mean([f["post_vol"]-f["pre_vol"] for f in crypto_findings])
            st.markdown(f"""<div style='font-size:0.78rem;color:#8892b0;-webkit-text-fill-color:#8892b0;
                border-top:1px solid rgba(247,147,26,0.2);margin-top:0.5rem;padding-top:0.5rem;'>
                Avg vol shift: <span style='color:#F7931A;-webkit-text-fill-color:#F7931A;'>
                {vol_change:+.1f}%</span> annualised</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with kf_c4:
        if currency_findings:
            st.markdown("""<div style='background:#112240;border:1px solid rgba(255,107,157,0.3);
                border-top:3px solid #FF6B9D;border-radius:8px;padding:1rem 1.2rem;'>
                <div style='color:#FF6B9D;-webkit-text-fill-color:#FF6B9D;font-weight:700;
                margin-bottom:0.6rem;'>💱 Currency Response</div>""", unsafe_allow_html=True)
            for f in currency_findings:
                color = "#28a745" if f["post_ret"] >= 0 else "#dc3545"
                arrow = "▲" if f["post_ret"] >= 0 else "▼"
                note  = "USD strengthened" if f["name"]=="DXY (USD Index)" and f["post_ret"]>0 else                         "INR depreciated" if f["name"]=="USD/INR" and f["post_ret"]>0 else                         "USD weakened" if f["name"]=="DXY (USD Index)" else "INR appreciated"
                st.markdown(f"""<div style='font-size:0.82rem;margin-bottom:0.4rem;'>
                    <span style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;'>{f["name"]}</span><br>
                    <span style='color:{color};-webkit-text-fill-color:{color};font-family:JetBrains Mono,monospace;'>
                    {arrow} {f["post_ret"]:+.2f}%</span>
                    <span style='color:#8892b0;-webkit-text-fill-color:#8892b0;font-size:0.75rem;'>
                    &nbsp;→ {note}</span></div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if haven_findings:
            st.markdown("""<div style='background:#112240;border:1px solid rgba(255,215,0,0.3);
                border-top:3px solid #FFD700;border-radius:8px;padding:1rem 1.2rem;margin-top:0.8rem;'>
                <div style='color:#FFD700;-webkit-text-fill-color:#FFD700;font-weight:700;
                margin-bottom:0.6rem;'>🪙 Safe-Haven Response</div>""", unsafe_allow_html=True)
            for f in haven_findings:
                color = "#28a745" if f["post_ret"] >= 0 else "#dc3545"
                arrow = "▲" if f["post_ret"] >= 0 else "▼"
                st.markdown(f"""<div style='font-size:0.82rem;margin-bottom:0.4rem;'>
                    <span style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;'>{f["name"]}</span>
                    <span style='color:{color};-webkit-text-fill-color:{color};font-family:JetBrains Mono,monospace;float:right;'>
                    {arrow} {f["post_ret"]:+.2f}%</span></div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with kf_c5:
        if defense_findings:
            st.markdown("""<div style='background:#112240;border:1px solid rgba(225,112,85,0.3);
                border-top:3px solid #E17055;border-radius:8px;padding:1rem 1.2rem;'>
                <div style='color:#E17055;-webkit-text-fill-color:#E17055;font-weight:700;
                margin-bottom:0.6rem;'>🛡 Defense & War Premium</div>""", unsafe_allow_html=True)
            for f in defense_findings:
                color = "#28a745" if f["post_ret"] >= 0 else "#dc3545"
                arrow = "▲" if f["post_ret"] >= 0 else "▼"
                st.markdown(f"""<div style='font-size:0.82rem;margin-bottom:0.4rem;'>
                    <span style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;'>{f["name"]}</span>
                    <span style='color:{color};-webkit-text-fill-color:{color};font-family:JetBrains Mono,monospace;float:right;'>
                    {arrow} {f["post_ret"]:+.2f}%</span></div>""", unsafe_allow_html=True)
            avg_def = np.mean([f["post_ret"] for f in defense_findings])
            st.markdown(f"""<div style='font-size:0.78rem;color:#8892b0;-webkit-text-fill-color:#8892b0;
                border-top:1px solid rgba(225,112,85,0.2);margin-top:0.5rem;padding-top:0.5rem;'>
                Avg defense return: <span style='color:#E17055;-webkit-text-fill-color:#E17055;'>
                {avg_def:+.1f}%</span></div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if energy_findings:
            avg_en = np.mean([f["post_ret"] for f in energy_findings])
            st.markdown(f"""<div style='background:#112240;border:1px solid rgba(255,107,53,0.3);
                border-top:3px solid #FF6B35;border-radius:8px;padding:1rem 1.2rem;margin-top:0.8rem;'>
                <div style='color:#FF6B35;-webkit-text-fill-color:#FF6B35;font-weight:700;
                margin-bottom:0.4rem;'>🛢 Energy Shock</div>
                <div style='font-size:0.82rem;'>""", unsafe_allow_html=True)
            for f in energy_findings:
                color = "#28a745" if f["post_ret"] >= 0 else "#dc3545"
                arrow = "▲" if f["post_ret"] >= 0 else "▼"
                st.markdown(f"""<span style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;'>
                    {f["name"]}</span>
                    <span style='color:{color};-webkit-text-fill-color:{color};font-family:JetBrains Mono,monospace;float:right;'>
                    {arrow} {f["post_ret"]:+.2f}%</span><br>""", unsafe_allow_html=True)
            st.markdown(f"""</div>
                <div style='font-size:0.78rem;color:#8892b0;-webkit-text-fill-color:#8892b0;
                border-top:1px solid rgba(255,107,53,0.2);margin-top:0.5rem;padding-top:0.5rem;'>
                Avg energy return: <span style='color:#FF6B35;-webkit-text-fill-color:#FF6B35;'>
                {avg_en:+.1f}%</span> (Hormuz effect)</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:0.8rem; color:#667eea; text-align:center; padding:1rem;'>
        <strong>The Mountain Path – World of Finance</strong> &nbsp;|&nbsp;
        Prof. V. Ravichandran, 28+ Years Corporate Finance & Banking Experience, 10+ Years Academic Excellence<br>
        Visiting Faculty @ Leading Business Schools in Bangalore &amp; India<br>
        🌐 <a href='https://themountainpathacademy.com' style='color:#FFD700;'>themountainpathacademy.com</a>
        &nbsp;|&nbsp;
        <a href='https://www.linkedin.com/in/trichyravis' style='color:#FFD700;'>LinkedIn</a>
        &nbsp;|&nbsp;
        <a href='https://github.com/trichyravis' style='color:#FFD700;'>GitHub</a>
        <br><br>
        <em>Data sourced from Yahoo Finance via yfinance. For educational purposes only. Not financial advice.</em>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 7: ABOUT THIS PROJECT
# ════════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("<div class='section-header'>About This Project</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown("""
<div style='background:#112240;border:1px solid rgba(0,77,128,0.4);border-radius:12px;padding:1.5rem 2rem;margin-bottom:1rem;'>
<h4 style='color:#FFD700;-webkit-text-fill-color:#FFD700;margin-top:0;font-family:Playfair Display,serif;'>📌 Project Overview</h4>
<p style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;line-height:1.8;'>
This application is an <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>educational financial research tool</strong>
built to study the real-time market impact of the <strong style='color:#ff9966;-webkit-text-fill-color:#ff9966;'>2026 Iran War
(Operation Epic Fury)</strong> — the US-Israel joint military strikes on Iran that began on <strong style='color:#ff9966;-webkit-text-fill-color:#ff9966;'>February 28, 2026</strong>.
</p>
<p style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;line-height:1.8;'>
The tool fetches <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>live data from Yahoo Finance</strong> and compares
how 20 global financial assets behaved across two periods — approximately 2 months before and after the crisis trigger date —
giving students and practitioners a quantitative framework to understand <em>geopolitical risk pricing</em> in financial markets — including whether <strong style='color:#F7931A;-webkit-text-fill-color:#F7931A;'>Bitcoin acts as a safe-haven or risk asset</strong> during war, and how the <strong style='color:#FF6B9D;-webkit-text-fill-color:#FF6B9D;'>Indian Rupee (USD/INR)</strong> responds to global risk-off flows.
</p>
</div>
        """, unsafe_allow_html=True)

        st.markdown("""
<div style='background:#112240;border:1px solid rgba(0,77,128,0.4);border-radius:12px;padding:1.5rem 2rem;margin-bottom:1rem;'>
<h4 style='color:#FFD700;-webkit-text-fill-color:#FFD700;margin-top:0;font-family:Playfair Display,serif;'>🎯 Learning Objectives</h4>
<ul style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;line-height:2;padding-left:1.2rem;'>
<li>Understand how <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>geopolitical shocks</strong> transmit across asset classes — equities, bonds, commodities, currencies &amp; crypto</li>
<li>Analyse <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>safe-haven flight behaviour</strong> — Gold, USD, Treasuries vs risk-off equities</li>
<li>Measure <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>Strait of Hormuz risk</strong> pricing in WTI, Brent and Natural Gas</li>
<li>Test the <strong style='color:#F7931A;-webkit-text-fill-color:#F7931A;'>Bitcoin safe-haven narrative</strong> — does BTC behave like Gold or like equities in a war?</li>
<li>Evaluate <strong style='color:#FF6B9D;-webkit-text-fill-color:#FF6B9D;'>INR depreciation pressure</strong> via USD/INR vs DXY — EM currency stress under geopolitical risk</li>
<li>Quantify <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>volatility regime shifts</strong> using annualised standard deviation pre vs post crisis</li>
<li>Apply <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>statistical significance testing</strong> (Welch t-test) to return differences across all 23 assets</li>
<li>Interpret <strong style='color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;'>correlation regime change</strong> — does BTC correlate with Gold or VIX post-war?</li>
<li>Evaluate <strong style='color:#E17055;-webkit-text-fill-color:#E17055;'>defense sector war premium</strong> — ITA, LMT, RTX outperformance vs broader market</li>
</ul>
</div>
        """, unsafe_allow_html=True)

        st.markdown("""
<div style='background:#112240;border:1px solid rgba(0,77,128,0.4);border-radius:12px;padding:1.5rem 2rem;'>
<h4 style='color:#FFD700;-webkit-text-fill-color:#FFD700;margin-top:0;font-family:Playfair Display,serif;'>⚙ Technical Stack</h4>
<table style='width:100%;color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;font-size:0.85rem;border-collapse:collapse;'>
<tr><td style='padding:0.4rem 0.8rem 0.4rem 0;color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;font-weight:600;width:140px;'>Framework</td><td>Streamlit</td></tr>
<tr><td style='padding:0.4rem 0.8rem 0.4rem 0;color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;font-weight:600;'>Data Source</td><td>Yahoo Finance via yfinance (live, 6-hr cache + manual refresh)</td></tr>
<tr><td style='padding:0.4rem 0.8rem 0.4rem 0;color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;font-weight:600;'>Charting</td><td>Plotly (interactive, dark-themed)</td></tr>
<tr><td style='padding:0.4rem 0.8rem 0.4rem 0;color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;font-weight:600;'>Statistics</td><td>SciPy — Welch t-test, return distributions</td></tr>
<tr><td style='padding:0.4rem 0.8rem 0.4rem 0;color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;font-weight:600;'>Assets Covered</td><td>23 instruments across 6 categories (incl. USD/INR, BTC, ETH)</td></tr>
<tr><td style='padding:0.4rem 0.8rem 0.4rem 0;color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;font-weight:600;'>Crisis Date</td><td>Feb 28, 2026 (Operation Epic Fury)</td></tr>
<tr><td style='padding:0.4rem 0.8rem 0.4rem 0;color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;font-weight:600;'>Analysis Window</td><td>Dec 28, 2025 → Today (rolling live window)</td></tr>
</table>
</div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
<div style='background:linear-gradient(135deg,#003366,#112240);border:1px solid rgba(255,215,0,0.25);border-radius:12px;padding:1.5rem 2rem;margin-bottom:1rem;text-align:center;'>
<div style='font-family:Playfair Display,serif;font-size:1.4rem;color:#FFD700;-webkit-text-fill-color:#FFD700;font-weight:700;margin-bottom:0.3rem;'>The Mountain Path</div>
<div style='font-size:0.8rem;color:#ADD8E6;-webkit-text-fill-color:#ADD8E6;letter-spacing:2px;text-transform:uppercase;margin-bottom:1.2rem;'>World of Finance</div>
<div style='width:60px;height:2px;background:#FFD700;margin:0 auto 1.2rem auto;'></div>
<div style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;font-size:0.95rem;font-weight:700;margin-bottom:0.2rem;'>Prof. V. Ravichandran</div>
<div style='color:#8892b0;-webkit-text-fill-color:#8892b0;font-size:0.8rem;line-height:1.7;margin-bottom:1rem;'>
28+ Years Corporate Finance &amp; Banking<br>
10+ Years Academic Excellence<br>
Visiting Faculty @ Leading Business Schools<br>in Bangalore &amp; India
</div>
<div style='margin-bottom:0.8rem;'>
<a href='https://themountainpathacademy.com' style='color:#FFD700;-webkit-text-fill-color:#FFD700;font-size:0.85rem;text-decoration:none;display:block;margin-bottom:0.4rem;'>
🌐 themountainpathacademy.com</a>
<a href='https://www.linkedin.com/in/trichyravis' style='color:#FFD700;-webkit-text-fill-color:#FFD700;font-size:0.85rem;text-decoration:none;display:block;margin-bottom:0.4rem;'>
💼 LinkedIn: trichyravis</a>
<a href='https://github.com/trichyravis' style='color:#FFD700;-webkit-text-fill-color:#FFD700;font-size:0.85rem;text-decoration:none;display:block;'>
🐙 GitHub: trichyravis</a>
</div>
</div>
        """, unsafe_allow_html=True)

        st.markdown("""
<div style='background:#112240;border:1px solid rgba(0,77,128,0.4);border-radius:12px;padding:1.5rem 2rem;margin-bottom:1rem;'>
<h4 style='color:#FFD700;-webkit-text-fill-color:#FFD700;margin-top:0;font-size:1rem;'>📚 Courses This Supports</h4>
<ul style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;font-size:0.85rem;line-height:2;padding-left:1.2rem;margin:0;'>
<li>Financial Risk Management</li>
<li>Fixed Income Securities &amp; Analysis</li>
<li>Financial Derivatives</li>
<li>Investment Banking</li>
<li>Alternative Investment Markets</li>
<li>Value Risk &amp; Capital Markets</li>
</ul>
</div>
        """, unsafe_allow_html=True)

        st.markdown("""
<div style='background:rgba(255,71,87,0.07);border:1px solid rgba(255,71,87,0.25);border-radius:12px;padding:1rem 1.5rem;font-size:0.78rem;'>
<span style='color:#ff9966;-webkit-text-fill-color:#ff9966;font-weight:700;'>⚠ Disclaimer</span><br>
<span style='color:#8892b0;-webkit-text-fill-color:#8892b0;line-height:1.7;display:block;margin-top:0.3rem;'>
Data sourced from Yahoo Finance via yfinance. This tool is for
<strong style='color:#e6f1ff;-webkit-text-fill-color:#e6f1ff;'>educational purposes only</strong>.
Not financial advice. Past market behaviour does not guarantee future results.
</span>
</div>
        """, unsafe_allow_html=True)
