# Enhanced Colorful Sustainable Smart City Assistant
import streamlit as st
import requests
from streamlit_option_menu import option_menu
import sys
import os
import random
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
# Page configuration
st.set_page_config(
    page_title="Sustainable Smart City Assistant",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.components import (
    summary_card,
    chat_assistant,
    feedback_form,
    eco_tips,
    policy_summarizer,
    report_generator
)
# Enhanced Custom CSS with vibrant colors
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #FF1744, #FF9800, #FFEB3B, #4CAF50, #2196F3, #9C27B0);
        background-size: 400% 400%;
        animation: gradientShift 3s ease infinite;
        -webkit-background-clip: text;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 2rem;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .city-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease;
    }
    
    .city-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .green-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .blue-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    
    .orange-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .purple-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333 !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        background-size: 400% 400%;
        animation: backgroundShift 10s ease infinite;
    }
    
    @keyframes backgroundShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .alert-success {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(90deg, #f12711, #f5af19);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .alert-info {
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# City data with realistic metrics
CITY_DATA = {
    "New York": {
        "population": "8.4M",
        "air_quality": {"value": 42, "trend": "+5%", "status": "Good"},
        "water_usage": {"value": "1.2M", "unit": "gallons", "trend": "-3%"},
        "energy": {"value": "2,850", "unit": "MWh", "trend": "+2%"},
        "waste_recycled": {"value": "78%", "trend": "+12%"},
        "green_spaces": {"value": "29%", "trend": "+3%"},
        "public_transport": {"value": "62%", "trend": "+5%"},
        "carbon_footprint": {"value": "4.2", "unit": "tons/person", "trend": "-8%"},
        "temperature": {"value": "22°C", "trend": "+1°C"},
        "humidity": {"value": "65%", "trend": "-2%"},
        "traffic_flow": {"value": "Medium", "trend": "Stable"},
        "crime_rate": {"value": "Low", "trend": "-15%"},
        "color": "#FF6B6B"
    },
    "San Francisco": {
        "population": "875K",
        "air_quality": {"value": 38, "trend": "-2%", "status": "Good"},
        "water_usage": {"value": "890K", "unit": "gallons", "trend": "-8%"},
        "energy": {"value": "1,450", "unit": "MWh", "trend": "-5%"},
        "waste_recycled": {"value": "85%", "trend": "+8%"},
        "green_spaces": {"value": "35%", "trend": "+7%"},
        "public_transport": {"value": "58%", "trend": "+3%"},
        "carbon_footprint": {"value": "3.8", "unit": "tons/person", "trend": "-12%"},
        "temperature": {"value": "18°C", "trend": "0°C"},
        "humidity": {"value": "72%", "trend": "+1%"},
        "traffic_flow": {"value": "High", "trend": "+5%"},
        "crime_rate": {"value": "Medium", "trend": "-8%"},
        "color": "#4ECDC4"
    },
    "Chicago": {
        "population": "2.7M",
        "air_quality": {"value": 48, "trend": "+8%", "status": "Moderate"},
        "water_usage": {"value": "1.8M", "unit": "gallons", "trend": "+1%"},
        "energy": {"value": "3,200", "unit": "MWh", "trend": "+6%"},
        "waste_recycled": {"value": "72%", "trend": "+5%"},
        "green_spaces": {"value": "24%", "trend": "+2%"},
        "public_transport": {"value": "55%", "trend": "+1%"},
        "carbon_footprint": {"value": "4.8", "unit": "tons/person", "trend": "-3%"},
        "temperature": {"value": "15°C", "trend": "-2°C"},
        "humidity": {"value": "68%", "trend": "+3%"},
        "traffic_flow": {"value": "Medium", "trend": "-2%"},
        "crime_rate": {"value": "Medium", "trend": "-12%"},
        "color": "#45B7D1"
    },
    "Austin": {
        "population": "965K",
        "air_quality": {"value": 35, "trend": "-7%", "status": "Good"},
        "water_usage": {"value": "650K", "unit": "gallons", "trend": "-12%"},
        "energy": {"value": "1,250", "unit": "MWh", "trend": "-8%"},
        "waste_recycled": {"value": "82%", "trend": "+15%"},
        "green_spaces": {"value": "42%", "trend": "+12%"},
        "public_transport": {"value": "45%", "trend": "+8%"},
        "carbon_footprint": {"value": "3.2", "unit": "tons/person", "trend": "-18%"},
        "temperature": {"value": "26°C", "trend": "+3°C"},
        "humidity": {"value": "58%", "trend": "-1%"},
        "traffic_flow": {"value": "Low", "trend": "-8%"},
        "crime_rate": {"value": "Low", "trend": "-20%"},
        "color": "#96CEB4"
    },
    "Seattle": {
        "population": "745K",
        "air_quality": {"value": 32, "trend": "-12%", "status": "Good"},
        "water_usage": {"value": "520K", "unit": "gallons", "trend": "-15%"},
        "energy": {"value": "980", "unit": "MWh", "trend": "-12%"},
        "waste_recycled": {"value": "89%", "trend": "+18%"},
        "green_spaces": {"value": "48%", "trend": "+15%"},
        "public_transport": {"value": "68%", "trend": "+12%"},
        "carbon_footprint": {"value": "2.8", "unit": "tons/person", "trend": "-22%"},
        "temperature": {"value": "16°C", "trend": "+1°C"},
        "humidity": {"value": "78%", "trend": "+2%"},
        "traffic_flow": {"value": "Medium", "trend": "Stable"},
        "crime_rate": {"value": "Very Low", "trend": "-25%"},
        "color": "#FFEAA7"
    }
}

def create_enhanced_kpi_card(title, value, unit="", trend="", color="blue", icon="📊"):
    """Create an enhanced colorful KPI card"""
    color_class = f"{color}-card"
    
    trend_color = "🟢" if trend.startswith("+") or trend.startswith("-") and "carbon" in title.lower() else "🔴" if trend.startswith("+") else "🟢"
    
    st.markdown(f"""
    <div class="metric-card {color_class}">
        <h3>{icon} {title}</h3>
        <h2>{value} {unit}</h2>
        <p>{trend_color} {trend}</p>
    </div>
    """, unsafe_allow_html=True)

def create_city_overview_card(city_name, city_data):
    """Create a detailed city overview card"""
    st.markdown(f"""
    <div class="city-card">
        <h2>🏙️ {city_name} Overview</h2>
        <p><strong>Population:</strong> {city_data['population']}</p>
        <p><strong>Air Quality:</strong> {city_data['air_quality']['status']} (AQI: {city_data['air_quality']['value']})</p>
        <p><strong>Temperature:</strong> {city_data['temperature']['value']}</p>
        <p><strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

def show_real_time_updates():
    """Show real-time data updates"""
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    # Auto-refresh every 30 seconds
    if st.button("🔄 Refresh Data", type="primary"):
        st.session_state.last_update = datetime.now()
        st.rerun()
    
    st.caption(f"Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

def create_city_comparison_chart(cities_data):
    """Create a comparison chart for selected cities"""
    metrics = ['Air Quality', 'Energy Efficiency', 'Waste Recycling', 'Green Spaces']
    
    # Sample data for comparison
    comparison_data = {
        'City': list(cities_data.keys()),
        'Air Quality Score': [100 - city['air_quality']['value'] for city in cities_data.values()],
        'Recycling Rate': [int(city['waste_recycled']['value'].rstrip('%')) for city in cities_data.values()],
        'Green Space %': [int(city['green_spaces']['value'].rstrip('%')) for city in cities_data.values()],
        'Transport Usage': [int(city['public_transport']['value'].rstrip('%')) for city in cities_data.values()]
    }
    
    df = pd.DataFrame(comparison_data)
    
    # Create colorful bar chart
    fig = px.bar(df, 
                 x='City', 
                 y=['Air Quality Score', 'Recycling Rate', 'Green Space %', 'Transport Usage'],
                 title="🏆 City Sustainability Comparison",
                 color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    return fig

def main():
    # Animated main header
    st.markdown('<h1 class="main-header">🏙️ Sustainable Smart City Assistant</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar navigation with enhanced styling
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        st.markdown("""
        <style>
        .sidebar-title {
            color: #FFD700;
            font-size: 1.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        </style>
        <div class="sidebar-title">🎯 Navigation</div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=[
                "🏠 Dashboard",
                "💬 Chat Assistant", 
                "📝 Submit Feedback",
                "🌱 Eco Tips",
                "📄 Policy Search",
                "📊 KPI Analysis",
                "📈 Reports"
            ],
            icons=["house-fill", "chat-dots-fill", "pencil-fill", "leaf-fill", 
                   "search", "graph-up", "file-text-fill"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#1183BDCE", "font-size": "22px"},
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "8px",
                    "color": "#020202",
                    "background-color": "rgba(255,255,255,0.05)",
                    "border-radius": "15px",
                    "padding": "12px 16px",
                    "border": "1px solid rgba(255,255,255,0.1)",
                    "transition": "all 0.3s ease"
                },
                "nav-link-selected": {
                    "background-color": "rgba(255,215,0,0.2)",
                    "border": "2px solid #FFD700",
                    "color": "#E47C1B",
                    "font-weight": "bold",
                    "box-shadow": "0 4px 15px rgba(255,215,0,0.3)"
                },
            }
        )
    
    # Route to appropriate page
    if selected == "🏠 Dashboard":
        show_enhanced_dashboard()
    elif selected == "💬 Chat Assistant":
        chat_assistant.show_chat_assistant()
    elif selected == "📝 Submit Feedback":
        feedback_form.render_feedback_form()
    elif selected == "🌱 Eco Tips":
        eco_tips.render_eco_tips()
    elif selected == "📄 Policy Search":
        policy_summarizer.render_policy_summarizer()
    elif selected == "📊 KPI Analysis":
        show_enhanced_kpi_analysis()
    elif selected == "📈 Reports":
        report_generator.report_generation_page()

def show_enhanced_dashboard():
    """Enhanced colorful dashboard with dynamic city data"""
    st.header("🏠 Smart City Command Center")
    
    # Real-time updates section
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        show_real_time_updates()
    with col2:
        st.metric("🌡️ Global Temp", "23.5°C", "0.5°C")
    with col3:
        st.metric("🌍 Active Cities", "5", "+2")
    
    # City selection with enhanced UI
    st.markdown("---")
    st.subheader("🏙️ Select City for Detailed Analysis")
    
    cities = list(CITY_DATA.keys())
    selected_city = st.selectbox(
        "Choose a city to view real-time metrics:",
        cities,
        help="Select any city to see detailed sustainability metrics"
    )
    
    if selected_city:
        city_data = CITY_DATA[selected_city]
        
        # City overview card
        create_city_overview_card(selected_city, city_data)
        
        # Main KPI cards with enhanced colors
        st.markdown("### 📊 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_enhanced_kpi_card(
                "Air Quality Index",
                str(city_data['air_quality']['value']),
                "AQI",
                city_data['air_quality']['trend'],
                "green",
                "🌬️"
            )
        
        with col2:
            create_enhanced_kpi_card(
                "Water Usage",
                city_data['water_usage']['value'],
                city_data['water_usage']['unit'],
                city_data['water_usage']['trend'],
                "blue",
                "💧"
            )
        
        with col3:
            create_enhanced_kpi_card(
                "Energy Consumption",
                city_data['energy']['value'],
                city_data['energy']['unit'],
                city_data['energy']['trend'],
                "orange",
                "⚡"
            )
        
        with col4:
            create_enhanced_kpi_card(
                "Waste Recycled",
                city_data['waste_recycled']['value'],
                "",
                city_data['waste_recycled']['trend'],
                "purple",
                "♻️"
            )
        
        # Detailed city metrics
        st.markdown("### 🔍 Detailed City Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="alert-success">🌳 Environmental Metrics</div>', unsafe_allow_html=True)
            st.metric("Green Spaces", city_data['green_spaces']['value'], city_data['green_spaces']['trend'])
            st.metric("Carbon Footprint", f"{city_data['carbon_footprint']['value']} {city_data['carbon_footprint']['unit']}", city_data['carbon_footprint']['trend'])
            st.metric("Temperature", city_data['temperature']['value'], city_data['temperature']['trend'])
        
        with col2:
            st.markdown('<div class="alert-info">🚊 Transportation & Mobility</div>', unsafe_allow_html=True)
            st.metric("Public Transport Usage", city_data['public_transport']['value'], city_data['public_transport']['trend'])
            st.metric("Traffic Flow", city_data['traffic_flow']['value'], city_data['traffic_flow']['trend'])
            st.metric("Humidity", city_data['humidity']['value'], city_data['humidity']['trend'])
        
        with col3:
            st.markdown('<div class="alert-warning">🛡️ Safety & Quality of Life</div>', unsafe_allow_html=True)
            st.metric("Crime Rate", city_data['crime_rate']['value'], city_data['crime_rate']['trend'])
            st.metric("Population", city_data['population'], "Growing")
            
            # Dynamic status based on metrics
            if city_data['air_quality']['value'] < 40:
                st.success("🌟 Excellent Air Quality!")
            elif city_data['air_quality']['value'] < 60:
                st.info("✅ Good Air Quality")
            else:
                st.warning("⚠️ Air Quality Needs Attention")
        
        # City comparison chart
        st.markdown("---")
        st.subheader("🏆 City Comparison Dashboard")
        
        comparison_cities = st.multiselect(
            "Select cities to compare:",
            cities,
            default=[selected_city],
            help="Choose multiple cities to see comparative analysis"
        )
        
        if len(comparison_cities) > 1:
            selected_cities_data = {city: CITY_DATA[city] for city in comparison_cities}
            fig = create_city_comparison_chart(selected_cities_data)
            st.plotly_chart(fig, use_container_width=True)
        
        # Alerts and recommendations
        st.markdown("---")
        st.subheader("🚨 Alerts & Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if int(city_data['waste_recycled']['value'].rstrip('%')) > 80:
                st.success("🎉 Excellent recycling performance! Keep it up!")
            elif int(city_data['waste_recycled']['value'].rstrip('%')) > 60:
                st.info("👍 Good recycling rate. Consider launching awareness campaigns.")
            else:
                st.warning("⚠️ Recycling rate could be improved. Implement recycling programs.")
        
        with col2:
            if city_data['air_quality']['value'] > 50:
                st.error("🚨 Air quality alert! Consider traffic restrictions.")
            else:
                st.success("✅ Air quality is within acceptable limits.")

def show_enhanced_kpi_analysis():
    """Enhanced KPI Analysis page with colorful visualizations"""
    st.header("📊 Advanced KPI Analysis & Forecasting")
    
    # Colorful tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🔮 Forecasting", "⚠️ Anomalies", "📋 Upload Data"])
    
    with tab1:
        st.subheader("📈 Historical Trends")
        # Sample trend data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Air Quality': [35 + random.randint(-10, 10) for _ in dates],
            'Energy Usage': [1000 + random.randint(-200, 200) for _ in dates],
            'Recycling Rate': [70 + random.randint(-5, 15) for _ in dates]
        })
        
        fig = px.line(trend_data, x='Date', y=['Air Quality', 'Energy Usage', 'Recycling Rate'],
                     title="🏙️ City Metrics Trends Over Time",
                     color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#96CEB4'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🔮 AI-Powered Forecasting")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="alert-info">💡 Predictions for Next Quarter</div>', unsafe_allow_html=True)
            st.success("🌱 Air quality expected to improve by 12%")
            st.info("💧 Water usage predicted to decrease by 8%")
            st.warning("⚡ Energy demand may spike during summer months")
        
        with col2:
            st.markdown('<div class="alert-success">🎯 Confidence Levels</div>', unsafe_allow_html=True)
            st.metric("Air Quality Forecast", "95%", "High Confidence")
            st.metric("Energy Forecast", "87%", "Good Confidence")
            st.metric("Water Forecast", "92%", "High Confidence")
    
    with tab3:
        st.subheader("⚠️ Real-time Anomaly Detection")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="alert-warning">🚨 Active Alerts</div>', unsafe_allow_html=True)
            st.error("**Critical**: Energy spike detected in Downtown District")
            st.warning("**Medium**: Unusual water consumption pattern in Sector 7")
            st.info("**Low**: Minor air quality fluctuation in Industrial Zone")
        
        with col2:
            st.markdown('<div class="alert-info">📍 Alert Details</div>', unsafe_allow_html=True)
            st.write("**Location**: Downtown District")
            st.write("**Anomaly**: 340% above baseline")
            st.write("**Duration**: 2.5 hours")
            st.write("**Recommendation**: Deploy response team")
    
    with tab4:
        st.subheader("📋 Upload Custom KPI Data")
        uploaded_file = st.file_uploader(
            "Upload your KPI data (CSV format)",
            type=['csv'],
            help="Upload historical data for custom analysis"
        )
        
        if uploaded_file:
            st.success("🎉 File uploaded successfully!")
            st.balloons()
            
            # Mock processing
            with st.spinner('🔄 Processing your data...'):
                time.sleep(2)
            
            st.markdown('<div class="alert-success">✅ Analysis Complete!</div>', unsafe_allow_html=True)
            st.info("📊 Found 24 data points across 6 metrics")
            st.success("🎯 Identified 3 optimization opportunities")
            st.warning("⚠️ Detected 1 potential issue requiring attention")

if __name__ == "__main__":
    main()