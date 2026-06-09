import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
import time

# ── Local imports ──────────────────────────────────────────────────────────────
from database import (
    get_cities, get_destinations, get_schedules_for_route,
    get_food_price, get_hotel_price, get_food_pricing, get_hotel_pricing,
    create_booking, get_booking_by_id, verify_owner_login,
    get_all_bookings, get_all_schedules, add_city, toggle_city,
    add_destination, toggle_destination, add_schedule, update_schedule_price,
    toggle_schedule, update_food_price, update_hotel_price,
    update_booking_status, change_owner_password,
)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="YatraGlobe 🌏 – India's Premier Tour Booking",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS  –  Your custom colour palette
#  FFF9D2 | FFEBCC | BFDDF0 | 8CC0EB | 9AB17A | C3CC9B | E4DFB5 | FBE8CE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ══ Import Google Font ══ */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* ══ Root palette ══ */
:root {
    --cream:      #FFF9D2;
    --peach:      #FFEBCC;
    --sky-light:  #BFDDF0;
    --sky:        #8CC0EB;
    --sage:       #9AB17A;
    --sage-light: #C3CC9B;
    --sand:       #E4DFB5;
    --warm:       #FBE8CE;
    --dark-text:  #1E2A3A;
    --mid-text:   #2C3E50;
    --accent:     #D4720A;
    --success:    #4A7C59;
    --danger:     #C0392B;
}

/* ══ App background ══ */
body, .stApp {
    background: linear-gradient(150deg, #1a2a3a 0%, #1e3a4a 40%, #0f2233 100%) !important;
    font-family: 'Poppins', 'Segoe UI', sans-serif !important;
}

/* ══ Sidebar ══ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f2d 0%, #1a3447 50%, #0f2233 100%) !important;
    border-right: 2px solid #8CC0EB44 !important;
}
section[data-testid="stSidebar"] * { color: #BFDDF0 !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #1e3a52, #2a5270) !important;
    color: #FFF9D2 !important;
    border: 1px solid #8CC0EB66 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    margin: 3px 0 !important;
    transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #8CC0EB, #BFDDF0) !important;
    color: #1E2A3A !important;
    transform: translateX(4px) !important;
    box-shadow: 0 4px 15px #8CC0EB44 !important;
}

/* ══ Hero banner ══ */
.hero-banner {
    background: linear-gradient(135deg, #0d3349 0%, #1a5276 50%, #0d3349 100%);
    border: 2px solid #8CC0EB55;
    border-radius: 20px;
    padding: 45px 35px;
    text-align: center;
    margin-bottom: 28px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5), inset 0 1px 0 #8CC0EB33;
    animation: fadeInDown 0.7s ease-out;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 30% 50%, #8CC0EB18 0%, transparent 60%),
                radial-gradient(ellipse at 70% 50%, #9AB17A18 0%, transparent 60%);
}
.hero-banner h1 {
    color: #FFF9D2;
    font-size: 3.2rem; font-weight: 800;
    letter-spacing: 3px; margin: 0;
    text-shadow: 0 2px 20px #8CC0EB88;
    position: relative;
}
.hero-banner p {
    color: #BFDDF0;
    font-size: 1.15rem; margin-top: 10px;
    position: relative;
}
.hero-tagline {
    color: #FFF9D2 !important;
    font-size: 0.95rem !important;
    background: linear-gradient(135deg, #8CC0EB33, #9AB17A33);
    border-radius: 25px; padding: 8px 20px;
    display: inline-block; margin-top: 10px;
    border: 1px solid #8CC0EB44;
}

/* ══ Section headers ══ */
.section-header {
    color: #FFF9D2;
    font-size: 1.5rem; font-weight: 700;
    border-left: 5px solid #8CC0EB;
    padding: 6px 0 6px 15px;
    margin: 22px 0 14px;
    background: linear-gradient(90deg, #8CC0EB18, transparent);
    border-radius: 0 8px 8px 0;
}

/* ══ Cards ══ */
.booking-card {
    background: linear-gradient(145deg, #112233ee, #1a3347ee);
    border: 1px solid #8CC0EB33;
    border-radius: 16px;
    padding: 22px;
    margin: 10px 0;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35);
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    backdrop-filter: blur(8px);
}
.booking-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(140,192,235,0.2);
    border-color: #8CC0EB88;
}

/* ══ Destination card ══ */
.dest-card {
    background: linear-gradient(145deg, #0f2538, #1a3a52);
    border-radius: 14px;
    padding: 18px 12px;
    text-align: center;
    border: 1px solid #8CC0EB33;
    cursor: pointer;
    transition: all 0.25s;
    min-height: 130px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.dest-card:hover {
    border-color: #BFDDF0;
    transform: scale(1.05) translateY(-3px);
    background: linear-gradient(145deg, #1a4060, #1e5070);
    box-shadow: 0 8px 24px #8CC0EB33;
}
.dest-card .icon { font-size: 2.4rem; }
.dest-card .name { color: #FFF9D2; font-weight: 700; margin-top: 8px; font-size: 0.95rem; }
.dest-card .desc { color: #C3CC9B; font-size: 0.72rem; margin-top: 4px; line-height: 1.3; }

/* ══ City pill ══ */
.city-pill {
    display: inline-block;
    background: linear-gradient(135deg, #1a3a52, #1e4a62);
    color: #BFDDF0;
    border: 1px solid #8CC0EB55;
    border-radius: 25px;
    padding: 7px 16px; margin: 4px;
    font-weight: 600; font-size: 0.85rem;
    box-shadow: 0 2px 8px rgba(140,192,235,0.2);
    transition: all 0.2s;
}
.city-pill:hover {
    background: linear-gradient(135deg, #8CC0EB, #BFDDF0);
    color: #1E2A3A !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 14px #8CC0EB55;
}

/* ══ Feature card ══ */
.feature-card {
    background: linear-gradient(145deg, #0f2538, #1a3a52);
    border: 1px solid #9AB17A44;
    border-radius: 16px;
    padding: 24px 18px;
    text-align: center;
    transition: all 0.25s;
}
.feature-card:hover {
    border-color: #9AB17A;
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(154,177,122,0.2);
}
.feature-card .f-icon { font-size: 3rem; }
.feature-card h4 { color: #FFF9D2; margin: 10px 0 6px; font-size: 1rem; font-weight: 700; }
.feature-card p  { color: #C3CC9B; font-size: 0.85rem; margin: 0; }

/* ══ Price badge ══ */
.price-badge {
    background: linear-gradient(135deg, #1e5070, #2a6080);
    color: #FFF9D2;
    border: 1px solid #8CC0EB66;
    border-radius: 25px;
    padding: 8px 22px;
    font-weight: 700;
    display: inline-block;
    font-size: 1.05rem;
    box-shadow: 0 3px 12px #8CC0EB33;
}

/* ══ Summary box ══ */
.summary-box {
    background: linear-gradient(145deg, #0d2235, #142d42);
    border: 2px solid #8CC0EB55;
    border-radius: 18px;
    padding: 28px;
    margin: 18px 0;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}
.summary-box h3 { color: #FFF9D2; font-size: 1.4rem; margin-bottom: 16px; }
.summary-row {
    display: flex; justify-content: space-between;
    padding: 9px 0;
    border-bottom: 1px solid #8CC0EB22;
    color: #BFDDF0;
    font-size: 0.95rem;
}
.summary-row span:first-child { color: #C3CC9B; }
.summary-total {
    display: flex; justify-content: space-between;
    padding: 14px 0 4px;
    color: #FFF9D2;
    font-size: 1.25rem; font-weight: 700;
    border-top: 2px solid #8CC0EB55;
    margin-top: 6px;
}

/* ══ Booking success ══ */
.booking-success {
    background: linear-gradient(135deg, #1a4a30, #0f3020);
    border: 2px solid #9AB17A;
    border-radius: 18px;
    padding: 35px;
    text-align: center;
    color: #FFF9D2;
    margin: 22px 0;
    box-shadow: 0 10px 35px rgba(154,177,122,0.3);
    animation: slideUp 0.6s ease-out;
}
.booking-success h2 { font-size: 2rem; margin: 0; color: #FFF9D2; }
.booking-id {
    font-size: 2.8rem; font-weight: 800;
    letter-spacing: 5px; color: #FFF9D2;
    background: linear-gradient(135deg, #1e5038, #2a6048);
    border: 2px solid #9AB17A;
    border-radius: 14px;
    padding: 12px 28px;
    display: inline-block;
    margin: 18px 0;
    box-shadow: 0 4px 20px rgba(154,177,122,0.3);
}

/* ══ Bus option card ══ */
.bus-card {
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    border: 2px solid transparent;
    cursor: pointer;
    transition: all 0.2s;
    margin: 6px;
}
.bus-ac {
    background: linear-gradient(145deg, #0f2d42, #1a3d52);
    border-color: #8CC0EB44;
}
.bus-ac:hover, .bus-ac.selected {
    border-color: #8CC0EB;
    box-shadow: 0 6px 20px #8CC0EB33;
    background: linear-gradient(145deg, #1a3d52, #2a5070);
}
.bus-nonac {
    background: linear-gradient(145deg, #1a2a0f, #253a18);
    border-color: #9AB17A44;
}
.bus-nonac:hover, .bus-nonac.selected {
    border-color: #9AB17A;
    box-shadow: 0 6px 20px #9AB17A33;
    background: linear-gradient(145deg, #253a18, #304a22);
}
.bus-card h4 { color: #FFF9D2; margin: 10px 0 5px; font-size: 1rem; }
.bus-card p  { color: #C3CC9B; font-size: 0.82rem; margin: 0; }

/* ══ Step indicator ══ */
.step-active   { color: #FFF9D2 !important; font-weight: 700 !important; }
.step-done     { color: #9AB17A !important; font-weight: 600 !important; }
.step-pending  { color: #8CC0EB66 !important; }

/* ══ Hotel card ══ */
.hotel-card {
    background: linear-gradient(145deg, #12203a, #1a2e48);
    border: 1px solid #BFDDF055;
    border-radius: 14px;
    padding: 18px;
    margin: 8px 0;
    color: #BFDDF0;
}

/* ══ Stat card ══ */
.stat-card {
    background: linear-gradient(145deg, #0f2538, #1a3347);
    border: 1px solid #8CC0EB33;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: all 0.2s;
}
.stat-card:hover { transform: translateY(-3px); border-color: #8CC0EB88; }
.stat-card .stat-val { color: #FFF9D2; font-size: 2rem; font-weight: 800; }
.stat-card .stat-lbl { color: #C3CC9B; font-size: 0.85rem; margin-top: 4px; }

/* ══ INPUT FIX – dark text on light background ══ */
/* Text inputs */
.stTextInput > div > div > input {
    background-color: #E8F4FD !important;
    color: #1E2A3A !important;
    border: 2px solid #8CC0EB !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #BFDDF0 !important;
    box-shadow: 0 0 0 3px #8CC0EB33 !important;
    background-color: #F0F9FF !important;
}
.stTextInput > div > div > input::placeholder { color: #6a8fa8 !important; }

/* Textarea */
.stTextArea > div > div > textarea {
    background-color: #E8F4FD !important;
    color: #1E2A3A !important;
    border: 2px solid #8CC0EB !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #BFDDF0 !important;
    box-shadow: 0 0 0 3px #8CC0EB33 !important;
}
.stTextArea > div > div > textarea::placeholder { color: #6a8fa8 !important; }

/* Number input */
.stNumberInput > div > div > input {
    background-color: #E8F4FD !important;
    color: #1E2A3A !important;
    border: 2px solid #8CC0EB !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* Select box */
.stSelectbox > div > div {
    background-color: #E8F4FD !important;
    color: #1E2A3A !important;
    border: 2px solid #8CC0EB !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}
.stSelectbox > div > div > div { color: #1E2A3A !important; }
/* Dropdown menu items */
[data-baseweb="select"] * { color: #1E2A3A !important; background-color: #E8F4FD !important; }
[data-baseweb="popover"] * { color: #1E2A3A !important; background-color: #ddeef8 !important; }

/* Date input */
.stDateInput > div > div > input {
    background-color: #E8F4FD !important;
    color: #1E2A3A !important;
    border: 2px solid #8CC0EB !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* Time input */
.stTimeInput > div > div > input {
    background-color: #E8F4FD !important;
    color: #1E2A3A !important;
    border: 2px solid #8CC0EB !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* Password input */
input[type="password"] {
    background-color: #E8F4FD !important;
    color: #1E2A3A !important;
    border: 2px solid #8CC0EB !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* ══ Labels ══ */
label, .stRadio > div > label, .stCheckbox > label,
.stSelectbox label, .stTextInput label, .stTextArea label,
.stNumberInput label, .stDateInput label, .stTimeInput label,
.stSlider label, div[data-testid="stWidgetLabel"] {
    color: #BFDDF0 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

/* ══ Radio buttons ══ */
.stRadio > div { gap: 10px !important; }
.stRadio > div > label {
    background: linear-gradient(135deg, #0f2538, #1a3347) !important;
    border: 2px solid #8CC0EB33 !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    color: #BFDDF0 !important;
    transition: all 0.2s !important;
}
.stRadio > div > label:hover {
    border-color: #8CC0EB !important;
    background: linear-gradient(135deg, #1a3a52, #2a4a62) !important;
}

/* ══ Checkboxes ══ */
.stCheckbox > label {
    background: linear-gradient(135deg, #0f2538, #1a3347) !important;
    border: 1px solid #8CC0EB33 !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    color: #BFDDF0 !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stCheckbox > label:hover {
    border-color: #9AB17A !important;
    background: linear-gradient(135deg, #1a2a1a, #253520) !important;
}

/* ══ Slider ══ */
.stSlider > div > div > div > div { background: #8CC0EB !important; }
.stSlider [data-testid="stTickBar"] { color: #BFDDF0 !important; }
.stSlider span { color: #FFF9D2 !important; }

/* ══ Main action buttons ══ */
.stButton > button {
    background: linear-gradient(135deg, #1a4060, #2a5878) !important;
    color: #FFF9D2 !important;
    border: 2px solid #8CC0EB55 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.3px !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #8CC0EB, #BFDDF0) !important;
    color: #1E2A3A !important;
    border-color: #BFDDF0 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px #8CC0EB44 !important;
}

/* ══ Metrics ══ */
div[data-testid="stMetricValue"] { color: #FFF9D2 !important; font-size: 1.8rem !important; font-weight: 800 !important; }
div[data-testid="stMetricLabel"] { color: #BFDDF0 !important; font-weight: 600 !important; }
div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #0f2538, #1a3347) !important;
    border: 1px solid #8CC0EB33 !important;
    border-radius: 14px !important;
    padding: 16px !important;
}

/* ══ Progress bar ══ */
.stProgress > div > div { background: linear-gradient(90deg, #8CC0EB, #9AB17A) !important; border-radius: 10px !important; }
.stProgress > div { background: #1a3347 !important; border-radius: 10px !important; }

/* ══ Dataframe ══ */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
.stDataFrame [data-testid="stDataFrame"] { background: #0f2538 !important; }

/* ══ Tabs ══ */
.stTabs [data-baseweb="tab-list"] { background: #0f2538 !important; border-radius: 12px !important; padding: 4px !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #8CC0EB !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a4060, #2a5878) !important;
    color: #FFF9D2 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

/* ══ Alert / Info boxes ══ */
.stAlert { border-radius: 12px !important; }
.stSuccess { background: #1a4a30 !important; color: #C3CC9B !important; border: 1px solid #9AB17A !important; }
.stError   { background: #3a1a1a !important; color: #FBE8CE !important; border: 1px solid #C0392B !important; }
.stWarning { background: #3a2a10 !important; color: #FFF9D2 !important; border: 1px solid #D4720A !important; }
.stInfo    { background: #0f2538 !important; color: #BFDDF0 !important; border: 1px solid #8CC0EB !important; }

/* ══ Divider ══ */
hr { border-color: #8CC0EB22 !important; }

/* ══ Scrollbar ══ */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f2538; }
::-webkit-scrollbar-thumb { background: #8CC0EB55; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #8CC0EB; }

/* ══ Animations ══ */
@keyframes fadeInDown { from { opacity: 0; transform: translateY(-24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideUp    { from { opacity: 0; transform: translateY(24px);  } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse      { 0%,100% { box-shadow: 0 0 0 0 #8CC0EB44; } 50% { box-shadow: 0 0 0 10px #8CC0EB00; } }

/* ══ Number input spinner buttons ══ */
button[data-testid="baseButton-secondary"] { color: #1E2A3A !important; background: #8CC0EB !important; }

/* ══ Download button ══ */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1a4a30, #2a5a40) !important;
    color: #FFF9D2 !important;
    border: 2px solid #9AB17A55 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #9AB17A, #C3CC9B) !important;
    color: #1E2A3A !important;
}

/* ══ Caption text ══ */
.stCaption { color: #8CC0EB99 !important; }
small, .stMarkdown small { color: #C3CC9B !important; }

/* ══ Markdown text in main area ══ */
.stMarkdown p, .stMarkdown li { color: #BFDDF0 !important; }
.stMarkdown strong { color: #FFF9D2 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #FFF9D2 !important; }

</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
for key, default in {
    "owner_logged_in": False,
    "owner_username": "",
    "page": "home",
    "selected_destination": "",
    "selected_pickup": "",
    "booking_step": 1,
    "booking_data": {},
    "last_booking_id": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:18px 0 12px">'
        '<div style="font-size:3.5rem;filter:drop-shadow(0 0 10px #8CC0EB)">🌏</div>'
        '<h2 style="color:#FFF9D2;margin:6px 0 2px;font-size:1.6rem;font-weight:800;letter-spacing:2px">YatraGlobe</h2>'
        '<p style="color:#8CC0EB;font-size:0.8rem;margin:0">India\'s Premier Tour Booking</p>'
        '<div style="width:60%;height:2px;background:linear-gradient(90deg,transparent,#8CC0EB,transparent);margin:12px auto"></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    nav_options = {
        "🏠  Home": "home",
        "🗺️  Book Your Tour": "booking",
        "🔍  Track Booking": "track",
        "ℹ️  About Us": "about",
        "🔐  Owner Login": "owner",
    }
    for label, page_key in nav_options.items():
        if st.button(label, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.session_state.booking_step = 1
            st.rerun()

    if st.session_state.owner_logged_in:
        st.divider()
        st.markdown(
            f'<div style="text-align:center;background:#1a3347;border:1px solid #8CC0EB44;'
            f'border-radius:10px;padding:10px;margin:5px">'
            f'<span style="font-size:1.5rem">👤</span>'
            f'<p style="color:#FFF9D2;margin:4px 0;font-weight:700">{st.session_state.owner_username}</p>'
            f'<p style="color:#8CC0EB;font-size:0.75rem;margin:0">Admin</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button("🚪  Logout"):
            st.session_state.owner_logged_in = False
            st.session_state.page = "home"
            st.rerun()

    st.divider()
    st.markdown(
        '<p style="color:#8CC0EB55;font-size:0.72rem;text-align:center;margin-top:10px">'
        '© 2025 YatraGlobe<br>All rights reserved</p>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  DESTINATION ICONS + COLORS
# ══════════════════════════════════════════════════════════════════════════════
DEST_ICONS = {
    "Manali":            "🏔️", "Rishikesh":      "🕉️",  "Goa":              "🏖️",
    "Ladakh":            "🏜️", "Shimla":          "🌲",  "Mussoorie":        "🌫️",
    "Nainital":          "🏞️", "Jaisalmer":       "🏰",  "Udaipur":          "🏯",
    "Darjeeling":        "🍵", "Andaman Islands": "🌊",  "Kerala Backwaters": "🚤",
    "Varanasi":          "🪔", "Agra":            "🕌",  "Amritsar":         "⭐",
    "Coorg":             "☕", "Ooty":            "🚂",  "Ranthambore":      "🐯",
    "Jim Corbett":       "🌳", "Spiti Valley":    "❄️",
}


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    # ── Hero ──
    st.markdown(
        """
        <div class="hero-banner">
            <div style="font-size:1rem;color:#8CC0EB;letter-spacing:4px;text-transform:uppercase;margin-bottom:8px">
                ✦ Welcome to ✦
            </div>
            <h1>🌏 YatraGlobe</h1>
            <p>✈️ Explore India's Most Beautiful Destinations – Book Your Dream Tour Today!</p>
            <div class="hero-tagline">
                🏔️ Mountains &nbsp;|&nbsp; 🏖️ Beaches &nbsp;|&nbsp; 🕉️ Spiritual &nbsp;|&nbsp;
                🌲 Hills &nbsp;|&nbsp; 🏜️ Deserts &nbsp;|&nbsp; 🌊 Islands
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Quick Stats ──
    bookings = get_all_bookings()
    cities   = get_cities()
    dests    = get_destinations()

    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (c1, "🎫", "Total Bookings",    str(len(bookings))),
        (c2, "🏙️", "Pickup Cities",    str(len(cities))),
        (c3, "🗺️", "Destinations",     str(len(dests))),
        (c4, "⭐", "Happy Tourists",    f"{len(bookings)*4+1250}+"),
    ]
    for col, icon, lbl, val in stats:
        col.markdown(
            f'<div class="stat-card">'
            f'<div style="font-size:2rem">{icon}</div>'
            f'<div class="stat-val">{val}</div>'
            f'<div class="stat-lbl">{lbl}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Destinations Grid ──
    st.markdown('<div class="section-header">🗺️ Popular Destinations</div>', unsafe_allow_html=True)
    if dests:
        cols_per_row = 5
        for row_start in range(0, len(dests), cols_per_row):
            row_dests = dests[row_start: row_start + cols_per_row]
            cols = st.columns(len(row_dests))
            for col, dest in zip(cols, row_dests):
                with col:
                    icon = DEST_ICONS.get(dest["destination_name"], "📍")
                    desc_short = (dest.get("description") or "")[:48]
                    st.markdown(
                        f'<div class="dest-card">'
                        f'<div class="icon">{icon}</div>'
                        f'<div class="name">{dest["destination_name"]}</div>'
                        f'<div class="desc">{desc_short}…</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    if st.button("Book →", key=f"book_dest_{dest['id']}"):
                        st.session_state.selected_destination = dest["destination_name"]
                        st.session_state.page = "booking"
                        st.session_state.booking_step = 1
                        st.rerun()
    else:
        st.info("No destinations found. Please check your database connection.")

    st.markdown("---")

    # ── Pickup Cities ──
    st.markdown('<div class="section-header">🚌 Pickup Cities Across India</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#C3CC9B;margin-bottom:12px">📍 We pick you up from your city! Our buses cover 20+ major cities.</p>', unsafe_allow_html=True)
    if cities:
        city_html = "".join(
            f'<span class="city-pill">📍 {c["city_name"]}</span>' for c in cities
        )
        st.markdown(city_html, unsafe_allow_html=True)

    st.markdown("---")

    # ── Why Choose Us ──
    st.markdown('<div class="section-header">⭐ Why Choose YatraGlobe?</div>', unsafe_allow_html=True)
    features = [
        ("🚌", "Luxury AC Buses",   "Sleeper & semi-sleeper AC buses with GPS live tracking and onboard WiFi"),
        ("🏨", "Premium Hotels",     "Choose from 5★ luxury to budget stays. Handpicked, verified properties"),
        ("🍽️", "Curated Food Menu",  "Fresh Veg & Non-Veg meals. Breakfast, Lunch & Dinner options available"),
        ("🔒", "100% Secure",        "Safe payments, instant booking confirmation & dedicated support 24/7"),
    ]
    w1, w2, w3, w4 = st.columns(4)
    for col, (icon, title, desc) in zip([w1, w2, w3, w4], features):
        col.markdown(
            f'<div class="feature-card">'
            f'<div class="f-icon">{icon}</div>'
            f'<h4>{title}</h4>'
            f'<p>{desc}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Bus Types Preview ──
    st.markdown('<div class="section-header">🚌 Our Fleet</div>', unsafe_allow_html=True)
    bc1, bc2 = st.columns(2)
    with bc1:
        st.markdown(
            '<div class="bus-card bus-ac">'
            '<div style="font-size:3rem">🚌❄️</div>'
            '<h4>AC Luxury Bus</h4>'
            '<p style="color:#BFDDF0;font-size:0.9rem;margin:8px 0">✅ Air Conditioned &nbsp;|&nbsp; ✅ Recliner Seats<br>'
            '✅ Charging Points &nbsp;|&nbsp; ✅ Blanket & Pillow<br>✅ Entertainment Screen &nbsp;|&nbsp; ✅ GPS Tracked</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    with bc2:
        st.markdown(
            '<div class="bus-card bus-nonac">'
            '<div style="font-size:3rem">🚌🪟</div>'
            '<h4>Non-AC Deluxe Bus</h4>'
            '<p style="color:#C3CC9B;font-size:0.9rem;margin:8px 0">✅ Window Seats &nbsp;|&nbsp; ✅ Comfortable Seats<br>'
            '✅ Charging Points &nbsp;|&nbsp; ✅ More Affordable<br>✅ Spacious Legroom &nbsp;|&nbsp; ✅ GPS Tracked</p>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        if st.button("🎫 Book Your Tour Now!", key="hero_book"):
            st.session_state.page = "booking"
            st.session_state.booking_step = 1
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: BOOKING  (multi-step)
# ══════════════════════════════════════════════════════════════════════════════
def page_booking():
    st.markdown(
        '<div class="hero-banner" style="padding:22px 30px">'
        '<h1 style="font-size:2.2rem">🎫 Book Your Dream Tour</h1>'
        '<p>Complete the steps below to secure your perfect trip 🗺️</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Progress ──
    step = st.session_state.booking_step
    st.progress((step - 1) / 4)

    step_labels = [
        ("👤", "Tourist Details"),
        ("📍", "Route & Bus"),
        ("🍽️", "Food & Hotel"),
        ("💳", "Confirm & Pay"),
    ]
    cols_p = st.columns(4)
    for i, (col, (ico, lbl)) in enumerate(zip(cols_p, step_labels)):
        if i + 1 == step:
            cls = "step-active"
            bg  = "background:linear-gradient(135deg,#1a4060,#2a5878);border:2px solid #8CC0EB;"
        elif i + 1 < step:
            cls = "step-done"
            bg  = "background:linear-gradient(135deg,#1a4a30,#2a5a40);border:2px solid #9AB17A;"
        else:
            cls = "step-pending"
            bg  = "background:#0f2538;border:2px solid #8CC0EB22;"
        col.markdown(
            f'<div style="{bg}border-radius:12px;padding:10px;text-align:center;">'
            f'<div style="font-size:1.4rem">{ico}</div>'
            f'<div class="{cls}" style="font-size:0.78rem;margin-top:4px">{lbl}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    bd = st.session_state.booking_data

    # ────────────────────────────────────────────────────────────────────────
    if step == 1:
        st.markdown('<div class="section-header">👤 Tourist Information</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name  = st.text_input("🧑 Full Name *",    value=bd.get("name", ""),  placeholder="Enter your full name")
            age   = st.number_input("🎂 Age *",         min_value=1, max_value=100, value=bd.get("age", 25))
            phone = st.text_input("📱 Phone Number",   value=bd.get("phone", ""), placeholder="+91 XXXXX XXXXX")
        with c2:
            address = st.text_area("🏠 Current Address *", value=bd.get("address", ""), placeholder="House No, Street, City, State, PIN", height=105)
            email   = st.text_input("📧 Email Address", value=bd.get("email", ""),  placeholder="your@email.com")

        st.markdown('<div class="section-header">🎫 Ticket Selection</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#C3CC9B">Drag the slider to select number of travellers:</p>', unsafe_allow_html=True)
        num_tickets = st.slider("Number of Tickets", min_value=1, max_value=20, value=bd.get("num_tickets", 1))

        # Ticket display
        ticket_html = "".join(
            f'<span style="display:inline-block;background:linear-gradient(135deg,#1a4060,#2a5878);'
            f'color:#FFF9D2;border:1px solid #8CC0EB55;border-radius:8px;padding:6px 12px;margin:3px;font-size:0.85rem">🎫 Ticket {i+1}</span>'
            for i in range(num_tickets)
        )
        st.markdown(f'<div style="margin:10px 0">{ticket_html}</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#BFDDF0;font-size:1rem">Total: <b style="color:#FFF9D2">{num_tickets} ticket(s)</b> selected</p>', unsafe_allow_html=True)

        travel_date = st.date_input(
            "📅 Travel Date *",
            value=bd.get("travel_date", date.today() + timedelta(days=7)),
            min_value=date.today() + timedelta(days=1),
        )

        if st.button("Next ➡️  Step 2: Route & Bus"):
            if not name.strip():
                st.error("❌ Please enter your full name.")
            elif not address.strip():
                st.error("❌ Please enter your current address.")
            else:
                st.session_state.booking_data.update({
                    "name": name, "age": age, "phone": phone,
                    "address": address, "email": email,
                    "num_tickets": num_tickets, "travel_date": travel_date,
                })
                st.session_state.booking_step = 2
                st.rerun()

    # ────────────────────────────────────────────────────────────────────────
    elif step == 2:
        cities = get_cities()
        dests  = get_destinations()
        city_names = [c["city_name"] for c in cities]
        dest_names = [d["destination_name"] for d in dests]

        st.markdown('<div class="section-header">📍 Select Your Pickup City</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#C3CC9B">Slide to find your nearest pickup point 🚌</p>', unsafe_allow_html=True)

        if city_names:
            city_idx = st.select_slider(
                "🏙️ Pickup City",
                options=range(len(city_names)),
                value=city_names.index(bd.get("pickup_city", city_names[0])) if bd.get("pickup_city") in city_names else 0,
                format_func=lambda i: f"📍 {city_names[i]}",
            )
            selected_city = city_names[city_idx]
            st.markdown(
                f'<div class="booking-card" style="border-left:4px solid #8CC0EB">'
                f'<div style="display:flex;align-items:center;gap:12px">'
                f'<span style="font-size:2.5rem">🏙️</span>'
                f'<div><h3 style="color:#FFF9D2;margin:0">📍 {selected_city}</h3>'
                f'<p style="color:#BFDDF0;margin:4px 0 0">Our bus will pick you up from the main bus stand / designated stop in {selected_city}.</p></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.error("No cities available.")
            selected_city = ""

        st.markdown('<div class="section-header">🗺️ Select Your Destination</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#C3CC9B">Slide to explore amazing destinations 🏔️</p>', unsafe_allow_html=True)

        if dest_names:
            presel   = bd.get("destination") or st.session_state.get("selected_destination", dest_names[0])
            dest_idx = st.select_slider(
                "🗺️ Tourist Destination",
                options=range(len(dest_names)),
                value=dest_names.index(presel) if presel in dest_names else 0,
                format_func=lambda i: f"{DEST_ICONS.get(dest_names[i],'📍')} {dest_names[i]}",
            )
            selected_dest = dest_names[dest_idx]
            dest_info     = next((d for d in dests if d["destination_name"] == selected_dest), {})
            st.markdown(
                f'<div class="booking-card" style="border-left:4px solid #9AB17A">'
                f'<div style="display:flex;align-items:center;gap:12px">'
                f'<span style="font-size:2.5rem">{DEST_ICONS.get(selected_dest,"📍")}</span>'
                f'<div><h3 style="color:#FFF9D2;margin:0">{selected_dest}</h3>'
                f'<p style="color:#C3CC9B;margin:4px 0 0">{dest_info.get("description","")}</p></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.error("No destinations available.")
            selected_dest = ""

        # ── Bus Type ──
        st.markdown('<div class="section-header">🚌 Choose Bus Type</div>', unsafe_allow_html=True)
        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown(
                '<div class="bus-card bus-ac">'
                '<div style="font-size:2.8rem">🚌❄️</div>'
                '<h4 style="color:#FFF9D2">AC Luxury Bus</h4>'
                '<p style="color:#BFDDF0;font-size:0.82rem">Air Conditioned · Recliner Seats<br>Charging Points · Blanket & Pillow</p>'
                '</div>',
                unsafe_allow_html=True,
            )
        with bc2:
            st.markdown(
                '<div class="bus-card bus-nonac">'
                '<div style="font-size:2.8rem">🚌🪟</div>'
                '<h4 style="color:#FFF9D2">Non-AC Deluxe Bus</h4>'
                '<p style="color:#C3CC9B;font-size:0.82rem">Window Seats · More Affordable<br>Spacious Legroom · Charging Points</p>'
                '</div>',
                unsafe_allow_html=True,
            )

        bus_type = st.radio(
            "Select Bus Type",
            ["🚌❄️ AC Bus", "🚌🪟 Non-AC Bus"],
            index=0 if bd.get("bus_type", "AC") == "AC" else 1,
            horizontal=True,
        )
        bus_type_clean = "AC" if "AC Bus" in bus_type else "Non-AC"

        # ── Schedules ──
        schedules = get_schedules_for_route(selected_city, selected_dest) if selected_city and selected_dest else []
        selected_schedule_id = None
        base_price = 0.0

        if schedules:
            st.markdown('<div class="section-header">🕐 Available Bus Timings</div>', unsafe_allow_html=True)
            for i, s in enumerate(schedules):
                dep   = str(s.get("departure_time", ""))[:5]
                arr   = str(s.get("arrival_time", ""))[:5] if s.get("arrival_time") else "N/A"
                btype = s.get("bus_type", "")
                price = float(s.get("price", 0))
                icon  = "❄️" if btype == "AC" else "🪟"
                st.markdown(
                    f'<div class="booking-card" style="padding:14px 18px;margin:6px 0">'
                    f'<span style="color:#FFF9D2;font-weight:700">{icon} {dep} → {arr}</span>'
                    f'&nbsp;&nbsp;<span style="color:#C3CC9B">{btype}</span>'
                    f'&nbsp;&nbsp;<span class="price-badge" style="font-size:0.9rem">₹{price:.0f}/person</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            sch_labels = []
            for s in schedules:
                dep   = str(s.get("departure_time", ""))[:5]
                arr   = str(s.get("arrival_time", ""))[:5] if s.get("arrival_time") else "N/A"
                btype = s.get("bus_type", "")
                price = float(s.get("price", 0))
                sch_labels.append(f"🕐 {dep} → {arr}  |  {btype}  |  ₹{price:.0f}/person")

            sel_sch_idx      = st.selectbox("Select Bus Timing", range(len(sch_labels)), format_func=lambda i: sch_labels[i])
            selected_schedule_id = schedules[sel_sch_idx]["id"]
            base_price           = float(schedules[sel_sch_idx]["price"]) * bd.get("num_tickets", 1)
            st.markdown(
                f'<p class="price-badge">🎫 Total Ticket Price: ₹{base_price:.0f} for {bd.get("num_tickets",1)} person(s)</p>',
                unsafe_allow_html=True,
            )
        else:
            st.warning(f"⚠️ No scheduled buses found for **{selected_city} → {selected_dest}**. Default fare applied. Please contact us.")
            base_price = 1000.0 * bd.get("num_tickets", 1)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("⬅️ Back"):
                st.session_state.booking_step = 1
                st.rerun()
        with col_next:
            if st.button("Next ➡️  Step 3: Food & Hotel"):
                if not selected_city or not selected_dest:
                    st.error("Please select both pickup city and destination.")
                else:
                    st.session_state.booking_data.update({
                        "pickup_city": selected_city, "destination": selected_dest,
                        "bus_type": bus_type_clean, "schedule_id": selected_schedule_id,
                        "base_ticket_price": base_price,
                    })
                    st.session_state.booking_step = 3
                    st.rerun()

    # ────────────────────────────────────────────────────────────────────────
    elif step == 3:
        st.markdown('<div class="section-header">🍽️ Food Preferences</div>', unsafe_allow_html=True)

        # Food type selector with visual cards
        st.markdown('<p style="color:#C3CC9B">Choose your meal preference for the trip:</p>', unsafe_allow_html=True)
        fc1, fc2, fc3 = st.columns(3)
        food_cards = [
            ("🥗", "Veg",      "Pure vegetarian meals\nFresh & healthy"),
            ("🍗", "Non-Veg",  "Chicken, mutton & more\nProtein-rich meals"),
            ("🚫", "No Food",  "I'll arrange food\nmyself"),
        ]
        for col, (ico, lbl, desc) in zip([fc1, fc2, fc3], food_cards):
            col.markdown(
                f'<div class="booking-card" style="text-align:center;padding:16px;border-color:#8CC0EB33">'
                f'<div style="font-size:2rem">{ico}</div>'
                f'<p style="color:#FFF9D2;font-weight:700;margin:6px 0">{lbl}</p>'
                f'<p style="color:#C3CC9B;font-size:0.78rem;white-space:pre-line">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        food_pref       = st.radio("Select Food Type", ["🥗 Veg", "🍗 Non-Veg", "🚫 No Food"],
                                    index=["🥗 Veg","🍗 Non-Veg","🚫 No Food"].index(bd.get("food_pref_display","🥗 Veg")),
                                    horizontal=True)
        food_type_clean = "Veg" if "Veg" in food_pref else ("Non-Veg" if "Non-Veg" in food_pref else "No Food")

        food_total = 0.0
        breakfast = lunch = dinner = False

        if food_type_clean != "No Food":
            st.markdown('<p style="color:#BFDDF0;font-weight:600;margin-top:16px">🍴 Select Meals to Include:</p>', unsafe_allow_html=True)
            mc1, mc2, mc3 = st.columns(3)
            bp = get_food_price(food_type_clean, "Breakfast")
            lp = get_food_price(food_type_clean, "Lunch")
            dp = get_food_price(food_type_clean, "Dinner")
            with mc1:
                st.markdown(f'<div style="text-align:center;padding:8px;color:#BFDDF0"><span style="font-size:1.8rem">🌅</span><br><b>Breakfast</b><br><span style="color:#C3CC9B">₹{bp:.0f}/person</span></div>', unsafe_allow_html=True)
                breakfast = st.checkbox(f"Add Breakfast", value=bd.get("breakfast", False), key="cb_bfast")
            with mc2:
                st.markdown(f'<div style="text-align:center;padding:8px;color:#BFDDF0"><span style="font-size:1.8rem">☀️</span><br><b>Lunch</b><br><span style="color:#C3CC9B">₹{lp:.0f}/person</span></div>', unsafe_allow_html=True)
                lunch     = st.checkbox(f"Add Lunch",      value=bd.get("lunch",     False), key="cb_lunch")
            with mc3:
                st.markdown(f'<div style="text-align:center;padding:8px;color:#BFDDF0"><span style="font-size:1.8rem">🌙</span><br><b>Dinner</b><br><span style="color:#C3CC9B">₹{dp:.0f}/person</span></div>', unsafe_allow_html=True)
                dinner    = st.checkbox(f"Add Dinner",     value=bd.get("dinner",    False), key="cb_dinner")

            n = bd.get("num_tickets", 1)
            if breakfast: food_total += bp * n
            if lunch:     food_total += lp * n
            if dinner:    food_total += dp * n
            if food_total > 0:
                st.markdown(f'<p class="price-badge">🍽️ Food Total: ₹{food_total:.0f}</p>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-header">🏨 Hotel Options</div>', unsafe_allow_html=True)

        hotel_data   = get_hotel_pricing()
        hotel_cats   = ["🚫 None (No Hotel)"] + [f"🏨 {h['hotel_category']}" for h in hotel_data]
        hotel_prices = {f"🏨 {h['hotel_category']}": float(h['price_per_night']) for h in hotel_data}
        hotel_stars  = {"5 Star": "⭐⭐⭐⭐⭐", "4 Star": "⭐⭐⭐⭐", "3 Star": "⭐⭐⭐",
                        "2 Star": "⭐⭐", "Budget/General": "🛏️", "Hostel/Dormitory": "🏠"}

        # Hotel cards
        hc_cols = st.columns(min(len(hotel_data), 3))
        for i, h in enumerate(hotel_data[:6]):
            col = hc_cols[i % 3]
            stars = hotel_stars.get(h["hotel_category"], "🏨")
            col.markdown(
                f'<div class="booking-card" style="padding:14px;text-align:center;border-color:#BFDDF033">'
                f'<div style="font-size:1.6rem">🏨</div>'
                f'<p style="color:#FFF9D2;font-weight:700;margin:5px 0;font-size:0.9rem">{h["hotel_category"]}</p>'
                f'<p style="color:#E4DFB5;font-size:0.8rem">{stars}</p>'
                f'<p style="color:#8CC0EB;font-weight:700">₹{float(h["price_per_night"]):.0f}/night</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        hotel_choice = st.selectbox("Select Hotel Category", hotel_cats,
                                     index=hotel_cats.index(bd.get("hotel_display","🚫 None (No Hotel)")) if bd.get("hotel_display") in hotel_cats else 0)
        hotel_total  = 0.0
        num_nights   = 0

        if hotel_choice != "🚫 None (No Hotel)":
            price_per  = hotel_prices.get(hotel_choice, 0)
            num_nights = st.slider("🌙 Number of Nights", min_value=1, max_value=30, value=bd.get("num_hotel_nights", 1))
            hotel_total = price_per * num_nights * bd.get("num_tickets", 1)
            st.markdown(
                f'<div class="booking-card" style="border-color:#BFDDF055;padding:14px">'
                f'<span style="font-size:1.5rem">🏨</span> '
                f'<span style="color:#FFF9D2;font-weight:700">{hotel_choice.replace("🏨 ","")}</span>&nbsp;'
                f'<span style="color:#C3CC9B">| ₹{price_per:.0f}/night × {num_nights} nights × {bd.get("num_tickets",1)} person(s)</span><br>'
                f'<span class="price-badge" style="margin-top:10px;display:inline-block">🏨 Hotel Total: ₹{hotel_total:.0f}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("⬅️ Back"):
                st.session_state.booking_step = 2
                st.rerun()
        with col_next:
            if st.button("Next ➡️  Step 4: Confirm & Pay"):
                hotel_cat_clean = hotel_choice.replace("🚫 ", "").replace("🏨 ", "").replace("None (No Hotel)", "None")
                st.session_state.booking_data.update({
                    "food_preference": food_type_clean, "food_pref_display": food_pref,
                    "breakfast": breakfast, "lunch": lunch, "dinner": dinner,
                    "food_total": food_total,
                    "hotel_category": hotel_cat_clean if hotel_cat_clean != "None (No Hotel)" else "None",
                    "hotel_display": hotel_choice,
                    "num_hotel_nights": num_nights, "hotel_total": hotel_total,
                })
                st.session_state.booking_step = 4
                st.rerun()

    # ────────────────────────────────────────────────────────────────────────
    elif step == 4:
        st.markdown('<div class="section-header">📋 Booking Summary & Confirmation</div>', unsafe_allow_html=True)
        d     = st.session_state.booking_data
        total = d.get("base_ticket_price", 0) + d.get("food_total", 0) + d.get("hotel_total", 0)

        meals_str = " + ".join(filter(None, [
            "Breakfast" if d.get("breakfast") else "",
            "Lunch"     if d.get("lunch")     else "",
            "Dinner"    if d.get("dinner")    else "",
        ])) or "None"

        st.markdown(
            f"""
            <div class="summary-box">
                <h3>📋 Your Booking Summary</h3>
                <div class="summary-row"><span>👤 Tourist Name</span><span>{d.get("name","—")}</span></div>
                <div class="summary-row"><span>🎂 Age</span><span>{d.get("age","—")}</span></div>
                <div class="summary-row"><span>📱 Phone</span><span>{d.get("phone","—")}</span></div>
                <div class="summary-row"><span>📅 Travel Date</span><span>{d.get("travel_date","—")}</span></div>
                <div class="summary-row"><span>🎫 No. of Tickets</span><span>{d.get("num_tickets","—")}</span></div>
                <div class="summary-row"><span>📍 Pickup City</span><span>{d.get("pickup_city","—")}</span></div>
                <div class="summary-row"><span>🗺️ Destination</span><span>{d.get("destination","—")}</span></div>
                <div class="summary-row"><span>🚌 Bus Type</span><span>{"❄️ AC" if d.get("bus_type")=="AC" else "🪟 Non-AC"}</span></div>
                <div class="summary-row"><span>🍽️ Food Type</span><span>{d.get("food_preference","None")}</span></div>
                <div class="summary-row"><span>🍴 Meals</span><span>{meals_str}</span></div>
                <div class="summary-row"><span>🏨 Hotel</span><span>{d.get("hotel_category","None")} ({d.get("num_hotel_nights",0)} nights)</span></div>
                <div class="summary-row"><span>🎫 Ticket Cost</span><span>₹{d.get("base_ticket_price",0):.0f}</span></div>
                <div class="summary-row"><span>🍽️ Food Cost</span><span>₹{d.get("food_total",0):.0f}</span></div>
                <div class="summary-row"><span>🏨 Hotel Cost</span><span>₹{d.get("hotel_total",0):.0f}</span></div>
                <div class="summary-total"><span>💰 TOTAL AMOUNT</span><span>₹{total:.0f}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        d["total_amount"] = total

        col_back, col_confirm = st.columns(2)
        with col_back:
            if st.button("⬅️ Back"):
                st.session_state.booking_step = 3
                st.rerun()
        with col_confirm:
            if st.button("✅ Confirm Booking & Pay Now"):
                with st.spinner("⏳ Processing your booking…"):
                    time.sleep(1.5)
                    booking_id = create_booking(d)
                if booking_id:
                    st.session_state.last_booking_id = booking_id
                    st.markdown(
                        f"""
                        <div class="booking-success">
                            <div style="font-size:3rem">🎉</div>
                            <h2>Booking Confirmed!</h2>
                            <p style="color:#C3CC9B">Your tour has been booked successfully. Save your Booking ID!</p>
                            <div class="booking-id">{booking_id}</div>
                            <p>📧 Confirmation → {d.get("email","your email")}<br>
                               📱 SMS → {d.get("phone","your number")}</p>
                            <p style="font-size:1.2rem;margin-top:10px">Total Paid: <b>₹{total:.0f}</b></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.balloons()
                    st.session_state.booking_step = 1
                    st.session_state.booking_data = {}
                    st.session_state.selected_destination = ""
                else:
                    st.error("❌ Booking failed. Please check database connection and try again.")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: TRACK BOOKING
# ══════════════════════════════════════════════════════════════════════════════
def page_track():
    st.markdown(
        '<div class="hero-banner" style="padding:22px 30px">'
        '<h1 style="font-size:2.2rem">🔍 Track Your Booking</h1>'
        '<p>Enter your Booking ID to check your tour status</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    tc1, tc2, tc3 = st.columns([1, 2, 1])
    with tc2:
        st.markdown('<div class="booking-card">', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;font-size:2.5rem;margin-bottom:10px">🎫</div>', unsafe_allow_html=True)
        booking_id = st.text_input("Enter Booking ID", placeholder="e.g. YG12345678").strip()
        track_btn  = st.button("🔍 Track My Booking")
        st.markdown('</div>', unsafe_allow_html=True)

    if track_btn:
        if not booking_id:
            st.error("Please enter a booking ID.")
        else:
            b = get_booking_by_id(booking_id)
            if b:
                status_color = {"Confirmed": "#9AB17A", "Pending": "#FBE8CE", "Cancelled": "#C0392B"}.get(b["booking_status"], "#8CC0EB")
                status_icon  = {"Confirmed": "✅", "Pending": "⏳", "Cancelled": "❌"}.get(b["booking_status"], "ℹ️")
                st.markdown(
                    f"""
                    <div class="summary-box">
                        <h3>📋 Booking – {b["booking_id"]}</h3>
                        <div class="summary-row"><span>Status</span>
                            <span style="color:{status_color};font-weight:700;font-size:1rem">{status_icon} {b["booking_status"]}</span></div>
                        <div class="summary-row"><span>👤 Tourist</span><span>{b["tourist_name"]}</span></div>
                        <div class="summary-row"><span>📍 Pickup</span><span>{b["pickup_city"]}</span></div>
                        <div class="summary-row"><span>🗺️ Destination</span><span>{b["destination"]}</span></div>
                        <div class="summary-row"><span>📅 Travel Date</span><span>{b["travel_date"]}</span></div>
                        <div class="summary-row"><span>🎫 Tickets</span><span>{b["num_tickets"]}</span></div>
                        <div class="summary-row"><span>🚌 Bus</span><span>{"❄️ AC" if b["bus_type"]=="AC" else "🪟 Non-AC"}</span></div>
                        <div class="summary-row"><span>🏨 Hotel</span><span>{b["hotel_category"]}</span></div>
                        <div class="summary-total"><span>💰 Total Paid</span><span>₹{float(b["total_amount"]):.0f}</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.error(f"❌ No booking found with ID **{booking_id}**. Please verify and try again.")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ABOUT
# ══════════════════════════════════════════════════════════════════════════════
def page_about():
    st.markdown(
        '<div class="hero-banner">'
        '<h1 style="font-size:2.6rem">🌏 About YatraGlobe</h1>'
        '<p>India\'s most trusted tour booking platform since 2020</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            '<div class="booking-card">'
            '<h3 style="color:#FFF9D2">🎯 Our Mission</h3>'
            '<p style="color:#BFDDF0">YatraGlobe is dedicated to making travel in India accessible, comfortable, '
            'and affordable for everyone. We provide seamless tour booking with luxury buses, '
            'top-rated hotels, and authentic dining experiences.</p>'
            '<p style="color:#C3CC9B;margin-top:10px">🚌 20+ pickup cities &nbsp;|&nbsp; 🗺️ 20+ destinations<br>'
            '🏨 100+ hotel partners &nbsp;|&nbsp; ⭐ 5000+ happy tourists</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="booking-card">'
            '<h3 style="color:#FFF9D2">📞 Contact Us</h3>'
            '<p style="color:#BFDDF0">'
            '📱 <b>+91 98765 43210</b><br><br>'
            '📧 info@yatraglobe.com<br>'
            '🌐 www.yatraglobe.com<br>'
            '🏢 New Delhi – 110001, India<br><br>'
            '🕐 <span style="color:#C3CC9B">Support: 7AM – 11PM, All Days</span>'
            '</p>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-header" style="margin-top:24px">🏆 Our Achievements</div>', unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4)
    achievements = [
        ("🏆", "Best Tour App", "2023 Travel Awards"),
        ("⭐", "4.8★ Rating",   "10,000+ Reviews"),
        ("🌏", "All India",     "20+ States Covered"),
        ("🔒", "ISO Certified", "Secure & Trusted"),
    ]
    for col, (ico, title, sub) in zip([a1,a2,a3,a4], achievements):
        col.markdown(
            f'<div class="stat-card">'
            f'<div style="font-size:2rem">{ico}</div>'
            f'<div class="stat-val" style="font-size:1.1rem">{title}</div>'
            f'<div class="stat-lbl">{sub}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: OWNER LOGIN / DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_owner():
    if not st.session_state.owner_logged_in:
        st.markdown(
            '<div class="hero-banner" style="padding:22px 30px">'
            '<h1 style="font-size:2.2rem">🔐 Owner Login</h1>'
            '<p>Secure admin panel – authorised personnel only</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        lc1, lc2, lc3 = st.columns([1, 2, 1])
        with lc2:
            st.markdown(
                '<div class="booking-card" style="text-align:center">'
                '<div style="font-size:3rem;margin-bottom:10px">🔐</div>'
                '<h3 style="color:#FFF9D2">Admin Login</h3>',
                unsafe_allow_html=True,
            )
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
            if st.button("🔐 Login to Dashboard"):
                if verify_owner_login(username.strip(), password):
                    st.session_state.owner_logged_in = True
                    st.session_state.owner_username  = username
                    st.success("✅ Login successful! Welcome back.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")
            st.markdown('</div>', unsafe_allow_html=True)
            # st.caption("Default credentials: username = admin | password = Admin@1234")
        return

    # ── Dashboard ──
    st.markdown(
        f'<div class="hero-banner" style="padding:22px 30px">'
        f'<h1 style="font-size:2.2rem">⚙️ Owner Dashboard</h1>'
        f'<p>Welcome back, <b>{st.session_state.owner_username}</b>! Manage your YatraGlobe business here.</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📊 Overview", "🏙️ Cities", "🗺️ Destinations", "🚌 Bus Schedules", "💰 Pricing", "📋 Bookings"]
    )

    with tab1:
        bookings  = get_all_bookings()
        total_rev = sum(float(b.get("total_amount", 0)) for b in bookings)
        confirmed = sum(1 for b in bookings if b.get("booking_status") == "Confirmed")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📋 Total Bookings",       len(bookings))
        c2.metric("✅ Confirmed Bookings",    confirmed)
        c3.metric("💰 Total Revenue",         f"₹{total_rev:,.0f}")
        c4.metric("🗺️ Active Destinations",  len(get_destinations()))

        if bookings:
            st.markdown("### 📋 Recent Bookings")
            df = pd.DataFrame(bookings)[["booking_id","tourist_name","pickup_city","destination","travel_date","total_amount","booking_status"]].head(10)
            st.dataframe(df, use_container_width=True)

    with tab2:
        st.markdown("### 🏙️ Manage Pickup Cities")
        all_cities = execute_all_cities()
        if all_cities:
            st.dataframe(pd.DataFrame(all_cities)[["id","city_name","is_active"]], use_container_width=True)
        nc1, nc2 = st.columns([3,1])
        with nc1: new_city = st.text_input("City Name", key="new_city_input")
        with nc2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Add City"):
                if new_city.strip():
                    add_city(new_city.strip()); st.success(f"✅ '{new_city}' added!"); st.rerun()
        tc1, tc2, tc3 = st.columns(3)
        with tc1: toggle_id_city     = st.number_input("City ID",  min_value=1, key="toggle_city_id", step=1)
        with tc2: toggle_status_city = st.selectbox("Status", [1,0], format_func=lambda x:"Active" if x else "Inactive", key="toggle_city_status")
        with tc3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Update"):
                toggle_city(int(toggle_id_city), toggle_status_city); st.success("Updated!"); st.rerun()

    with tab3:
        st.markdown("### 🗺️ Manage Destinations")
        all_dests_admin = execute_all_destinations()
        if all_dests_admin:
            st.dataframe(pd.DataFrame(all_dests_admin)[["id","destination_name","description","is_active"]], use_container_width=True)
        d1, d2 = st.columns(2)
        with d1: new_dest_name = st.text_input("Destination Name", key="new_dest_name")
        with d2: new_dest_desc = st.text_input("Description",      key="new_dest_desc")
        if st.button("➕ Add Destination"):
            if new_dest_name.strip():
                add_destination(new_dest_name.strip(), new_dest_desc.strip()); st.success(f"✅ '{new_dest_name}' added!"); st.rerun()

    with tab4:
        st.markdown("### 🚌 Manage Bus Schedules")
        schedules = get_all_schedules()
        if schedules:
            st.dataframe(pd.DataFrame(schedules)[["id","from_city","to_destination","departure_time","arrival_time","bus_type","price","is_active"]], use_container_width=True)
        cities_admin = get_cities(); dests_admin = get_destinations()
        sc1, sc2 = st.columns(2)
        with sc1:
            sel_from = st.selectbox("From City",      [c["city_name"] for c in cities_admin], key="sched_from")
            sel_to   = st.selectbox("To Destination", [d["destination_name"] for d in dests_admin], key="sched_to")
            sel_type = st.selectbox("Bus Type",       ["AC","Non-AC"], key="sched_type")
        with sc2:
            dep_time = st.time_input("Departure Time", key="sched_dep")
            arr_time = st.time_input("Arrival Time",   key="sched_arr")
            price    = st.number_input("Price/Person (₹)", min_value=0.0, value=1000.0, key="sched_price")
        if st.button("➕ Add Schedule"):
            from_id = next((c["id"] for c in cities_admin if c["city_name"]==sel_from), None)
            to_id   = next((d["id"] for d in dests_admin  if d["destination_name"]==sel_to), None)
            if from_id and to_id:
                add_schedule(from_id, to_id, str(dep_time), str(arr_time), sel_type, price); st.success("✅ Schedule added!"); st.rerun()
        usc1, usc2, usc3 = st.columns(3)
        with usc1: upd_id      = st.number_input("Schedule ID",  min_value=1, key="upd_sched_id", step=1)
        with usc2: new_price_s = st.number_input("New Price (₹)", min_value=0.0, key="upd_sched_price")
        with usc3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Update Price"):
                update_schedule_price(int(upd_id), new_price_s); st.success("✅ Price updated!"); st.rerun()

    with tab5:
        st.markdown("### 💰 Manage Pricing")
        st.markdown("#### 🍽️ Food Pricing")
        food_rows = get_food_pricing()
        if food_rows: st.dataframe(pd.DataFrame(food_rows), use_container_width=True)
        fp1, fp2, fp3 = st.columns(3)
        with fp1: food_upd_id    = st.number_input("Food ID",       min_value=1, key="food_upd_id", step=1)
        with fp2: food_new_price = st.number_input("New Price (₹)", min_value=0.0, key="food_new_price")
        with fp3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Update Food Price"):
                update_food_price(int(food_upd_id), food_new_price); st.success("✅ Food price updated!"); st.rerun()
        st.markdown("#### 🏨 Hotel Pricing")
        hotel_rows = get_hotel_pricing()
        if hotel_rows: st.dataframe(pd.DataFrame(hotel_rows), use_container_width=True)
        hp1, hp2, hp3 = st.columns(3)
        with hp1: hotel_upd_id    = st.number_input("Hotel ID",          min_value=1, key="hotel_upd_id", step=1)
        with hp2: hotel_new_price = st.number_input("New Price (₹/night)", min_value=0.0, key="hotel_new_price")
        with hp3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Update Hotel Price"):
                update_hotel_price(int(hotel_upd_id), hotel_new_price); st.success("✅ Hotel price updated!"); st.rerun()
        st.markdown("#### 🔑 Change Owner Password")
        op1, op2 = st.columns(2)
        with op1: new_pass  = st.text_input("New Password",     type="password", key="new_pass")
        with op2: conf_pass = st.text_input("Confirm Password", type="password", key="conf_pass")
        if st.button("🔑 Change Password"):
            if new_pass and new_pass == conf_pass:
                change_owner_password(st.session_state.owner_username, new_pass); st.success("✅ Password changed!")
            else:
                st.error("Passwords do not match or are empty.")

    with tab6:
        st.markdown("### 📋 All Bookings")
        all_b = get_all_bookings()
        if all_b:
            df_b = pd.DataFrame(all_b)
            st.dataframe(df_b, use_container_width=True)
            bs1, bs2, bs3 = st.columns(3)
            with bs1: upd_bid    = st.text_input("Booking ID",  key="upd_bid")
            with bs2: upd_status = st.selectbox("New Status", ["Confirmed","Pending","Cancelled"], key="upd_status")
            with bs3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Update Status"):
                    if upd_bid.strip():
                        update_booking_status(upd_bid.strip(), upd_status); st.success("✅ Status updated!"); st.rerun()
            csv = df_b.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Bookings CSV", csv, "yatraglobe_bookings.csv", "text/csv")
        else:
            st.info("No bookings yet.")


# ── Helper admin queries ──────────────────────────────────────────────────────
def execute_all_cities():
    from database import execute_query
    return execute_query("SELECT * FROM cities ORDER BY id", fetch=True) or []

def execute_all_destinations():
    from database import execute_query
    return execute_query("SELECT * FROM destinations ORDER BY id", fetch=True) or []


# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
page = st.session_state.page
if   page == "home":    page_home()
elif page == "booking": page_booking()
elif page == "track":   page_track()
elif page == "about":   page_about()
elif page == "owner":   page_owner()
else:                   page_home()
