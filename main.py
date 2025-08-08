# app.py
import streamlit as st
from datetime import datetime
import pandas as pd
from urllib.parse import urlparse

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Intern Attendance System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- FANCY CSS STYLING ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Title styling */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Custom cards */
    .info-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(116, 185, 255, 0.3);
        transform: translateY(0);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(116, 185, 255, 0.4);
    }
    
    .success-card {
        background: linear-gradient(135deg, #55efc4 0%, #00b894 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(85, 239, 196, 0.3);
        animation: slideInFromTop 0.5s ease-out;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(253, 121, 168, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(116, 185, 255, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(116, 185, 255, 0.4);
        background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e6ed;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #74b9ff;
        box-shadow: 0 0 0 3px rgba(116, 185, 255, 0.1);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e6ed;
        padding: 0.75rem 1rem;
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #74b9ff;
        margin: 0.5rem 0;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Animations */
    @keyframes slideInFromTop {
        0% {
            opacity: 0;
            transform: translateY(-30px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInScale {
        0% {
            opacity: 0;
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .fade-in {
        animation: fadeInScale 0.6s ease-out;
    }
    
    /* Status badges */
    .status-early {
        background: linear-gradient(135deg, #55efc4 0%, #00b894 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-late {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-absent {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Sidebar improvements */
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    .css-1d391kg .stTextInput label {
        color: white !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------- CONFIG ----------
USER_DB = {
    "haula": "1234",
    "derrick": "5678",
    "lynette": "9999",
    "cathy": "9999",
    "ronnie": "9999",
    "pato": "9999",
    "jovan": "9999",
    "elvis": "9999",
    "hillary": "9999",
    "joanita": "9999",
    "philiper": "9999",
    "johnlucky": "9999",
    "chris": "9999",
    "owen": "9999",
    "deo": "9999",
    "joel": "9999",
    "abasa": "9999"
}

ATTENDANCE_FILE = "attendance.csv"

# ---------- LOGIN SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: white; margin-bottom: 2rem;">🔐 Login Portal</h2>
    </div>
    """, unsafe_allow_html=True)
    
    username = st.text_input("👤 Username", placeholder="Enter your username")
    pin = st.text_input("🔐 PIN", type="password", placeholder="Enter your PIN")
    
    if username and pin:
        if username not in USER_DB or USER_DB[username] != pin:
            st.markdown("""
            <div class="warning-card">
                <strong>❌ Invalid Credentials</strong><br>
                Please check your username and PIN.
            </div>
            """, unsafe_allow_html=True)
            st.stop()
        else:
            st.markdown("""
            <div class="success-card">
                <strong>✅ Login Successful!</strong><br>
                Welcome back!
            </div>
            """, unsafe_allow_html=True)
            name = username.capitalize()
    else:
        st.markdown("""
        <div class="info-card">
            <strong>🚀 Welcome!</strong><br>
            Please enter your credentials to continue.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# ---------- MAIN PAGE ----------
st.markdown("""
<div class="main-container fade-in">
    <h1 class="main-title">📋 Intern Attendance System</h1>
</div>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    # ---------- DISCIPLINE SELECTION ----------
    st.markdown("""
    <div class="info-card">
        <h3 style="margin: 0; font-size: 1.5rem;">🏢 Select Your Department</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Get discipline from URL
    try:
        query_params = st.experimental_get_query_params()
        discipline = query_params.get("block", [""])[0].capitalize()
    except:
        discipline = ""
    
    if discipline not in ["Civil", "Electrical", "Mechanical"]:
        discipline = st.selectbox(
            "Choose your discipline/block:",
            ["Civil", "Electrical", "Mechanical"],
            index=0
        )
    else:
        st.markdown(f"""
        <div class="success-card">
            <strong>🧭 Auto-detected Department: {discipline}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # ---------- SPECIAL STATUS ----------
    st.markdown("""
    <div class="info-card" style="margin-top: 2rem;">
        <h3 style="margin: 0; font-size: 1.5rem;">📝 Special Status</h3>
    </div>
    """, unsafe_allow_html=True)
    
    status_choice = st.selectbox(
        "Select if you have any special circumstances:",
        ["None", "On Leave", "On Official Duty"]
    )

with col2:
    # ---------- CURRENT TIME DISPLAY ----------
    current_time = datetime.now()
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #667eea; margin: 0;">🕐 Current Time</h3>
        <h2 style="margin: 0.5rem 0 0 0;">{current_time.strftime("%H:%M:%S")}</h2>
        <p style="margin: 0; color: #666;">{current_time.strftime("%A, %B %d, %Y")}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ---------- USER INFO ----------
    st.markdown(f"""
    <div class="metric-card" style="margin-top: 1rem;">
        <h3 style="color: #667eea; margin: 0;">👤 User Info</h3>
        <h2 style="margin: 0.5rem 0 0 0;">{name}</h2>
        <p style="margin: 0; color: #666;">{discipline} Department</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- CHECK-IN BUTTON ----------
st.markdown("<br>", unsafe_allow_html=True)

col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
with col_center2:
    if st.button("✅ Check In Now", key="checkin"):
        now = datetime.now()
        current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        current_hour_min = now.time()
        
        # Attendance logic
        if status_choice == "On Leave":
            status = "Leave"
            status_class = "status-early"
        elif status_choice == "On Official Duty":
            status = "Official Duty"
            status_class = "status-early"
        else:
            if current_hour_min < datetime.strptime("08:00", "%H:%M").time():
                status = "Early"
                status_class = "status-early"
            elif datetime.strptime("08:00", "%H:%M").time() <= current_hour_min <= datetime.strptime("08:20", "%H:%M").time():
                status = "Late"
                status_class = "status-late"
            else:
                status = "Absent"
                status_class = "status-absent"
        
        # Record data
        new_row = {
            "Name": name,
            "Discipline": discipline,
            "Status": status,
            "Time": current_time_str,
            "Remarks": status_choice if status_choice != "None" else ""
        }
        
        # Save to CSV
        try:
            df = pd.read_csv(ATTENDANCE_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Name", "Discipline", "Status", "Time", "Remarks"])
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(ATTENDANCE_FILE, index=False)
        
        st.markdown(f"""
        <div class="success-card" style="margin-top: 2rem;">
            <h3 style="margin: 0;">🎉 Attendance Recorded!</h3>
            <p style="margin: 0.5rem 0 0 0;">
                Status: <span class="{status_class}">{status}</span><br>
                Time: {current_time_str}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ---------- ADMIN PANEL ----------
st.markdown("<br><br>", unsafe_allow_html=True)

with st.expander("🔐 Admin Panel: View Attendance Records", expanded=False):
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
        
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            date_filter = st.date_input(
                "📅 Filter by Date:",
                value=datetime.now().date()
            )
        
        with col_filter2:
            discipline_filter = st.selectbox(
                "🏢 Filter by Department:",
                ["All", "Civil", "Electrical", "Mechanical"]
            )
        
        # Apply filters
        filtered_df = df[df["Time"].str.startswith(str(date_filter))]
        
        if discipline_filter != "All":
            filtered_df = filtered_df[filtered_df["Discipline"] == discipline_filter]
        
        if not filtered_df.empty:
            # Display metrics
            col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
            
            with col_metric1:
                early_count = len(filtered_df[filtered_df["Status"] == "Early"])
                st.metric("✅ Early", early_count)
            
            with col_metric2:
                late_count = len(filtered_df[filtered_df["Status"] == "Late"])
                st.metric("⚠️ Late", late_count)
            
            with col_metric3:
                absent_count = len(filtered_df[filtered_df["Status"] == "Absent"])
                st.metric("❌ Absent", absent_count)
            
            with col_metric4:
                total_count = len(filtered_df)
                st.metric("📊 Total", total_count)
            
            # Display data table
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400
            )
        else:
            st.markdown("""
            <div class="info-card">
                <h3 style="margin: 0;">📭 No Records Found</h3>
                <p style="margin: 0.5rem 0 0 0;">No attendance records match your filter criteria.</p>
            </div>
            """, unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.markdown("""
        <div class="warning-card">
            <h3 style="margin: 0;">📋 No Data Available</h3>
            <p style="margin: 0.5rem 0 0 0;">No attendance records have been created yet.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
    <p style="margin: 0;">Made with ❤️ for intern management</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">© 2025 Intern Attendance System</p>
</div>
""", unsafe_allow_html=True)