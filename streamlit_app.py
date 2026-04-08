import streamlit as st
from ui.user_dashboard import show_user_dashboard
from ui.ai_dashboard import show_ai_dashboard

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main-header {font-size: 3rem; color: #1f77b4; text-align: center; margin-bottom: 2rem;}
    .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px;}
    .stButton > button {background: linear-gradient(45deg, #4CAF50, #45a049); color: white; border-radius: 20px; padding: 0.5rem 2rem;}
    </style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="AI Trading System", 
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar - Global Controls
st.sidebar.title("⚙️ Controls")
selected_stock = st.sidebar.selectbox("Select Stock", ["AAPL", "AMZN", "GOOGL", "MSFT", "NVDA"])
st.session_state.selected_stock = selected_stock



# Hero Header
st.markdown('<h1 class="main-header">🚀 AI Trading System</h1>', unsafe_allow_html=True)
st.markdown("---")

# Tabs instead of radio
tab1, tab2 = st.tabs(["👤 User Dashboard", "🤖 AI Trading"])

with tab1:
    st.info(f"**Selected Stock: {selected_stock}**")
    show_user_dashboard()

with tab2:
    st.info(f"**Selected Stock: {selected_stock}**")
    show_ai_dashboard()
