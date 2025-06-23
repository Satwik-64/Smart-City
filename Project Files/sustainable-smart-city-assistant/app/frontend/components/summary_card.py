# Placeholder for summary_card.py
import streamlit as st

def create_kpi_card(title: str, value: str, unit: str, trend: str, color: str = "blue"):
    """Create a styled KPI card"""
    
    # Color mapping
    colors = {
        "blue": "#3498db",
        "green": "#2ecc71", 
        "orange": "#f39c12",
        "red": "#e74c3c",
        "purple": "#9b59b6"
    }
    
    card_color = colors.get(color, "#3498db")
    
    # Determine trend color
    trend_color = "#2ecc71" if trend.startswith("+") else "#e74c3c"
    
    card_html = f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid {card_color};
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        ">
            <h4 style="
                margin: 0;
                color: #2c3e50;
                font-size: 0.9rem;
                font-weight: 600;
            ">{title}</h4>
            <span style="
                color: {trend_color};
                font-size: 0.8rem;
                font-weight: bold;
            ">{trend}</span>
        </div>
        <div style="
            display: flex;
            align-items: baseline;
            gap: 0.5rem;
        ">
            <span style="
                font-size: 2rem;
                font-weight: bold;
                color: {card_color};
            ">{value}</span>
            <span style="
                font-size: 0.9rem;
                color: #7f8c8d;
            ">{unit}</span>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
