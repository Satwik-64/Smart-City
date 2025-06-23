# Placeholder for eco_tips.py
"""
Eco Tips Component for Sustainable Smart City Assistant
"""
import streamlit as st
import requests
from typing import Dict, List
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.helpers import APIHelper, ConfigHelper, TextProcessor

def render_eco_tips():
    """Render the eco tips page"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #2E8B57; font-size: 2.5rem; margin-bottom: 0.5rem;'>
            🌱 Eco-Friendly Tips
        </h1>
        <p style='color: #666; font-size: 1.2rem;'>
            Get personalized sustainability advice powered by AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Topic selection
        st.markdown("### 🎯 Choose Your Topic")
        
        # Get eco tip categories
        categories = ConfigHelper.get_eco_tip_categories()
        
        # Create two columns for category selection
        cat_col1, cat_col2 = st.columns(2)
        
        with cat_col1:
            selected_category = st.selectbox(
                "Select Category",
                options=categories,
                index=0,
                help="Choose a sustainability topic to get personalized tips"
            )
        
        with cat_col2:
            # Custom topic input
            custom_topic = st.text_input(
                "Or Enter Custom Topic",
                placeholder="e.g., solar panels, composting...",
                help="Enter any sustainability topic you're interested in"
            )
        
        # Use custom topic if provided, otherwise use selected category
        topic = custom_topic.strip() if custom_topic.strip() else selected_category
        
        # Tip generation section
        st.markdown("### 💡 Get Your Eco Tip")
        
        # Generate tip button
        if st.button("🌿 Generate Eco Tip", type="primary", use_container_width=True):
            if topic:
                generate_eco_tip(topic)
            else:
                st.warning("Please select a category or enter a custom topic.")
        
        # Display saved tips
        display_saved_tips()
        
        # Quick action buttons
        st.markdown("### 🚀 Quick Tips")
        quick_tips_section()

def generate_eco_tip(topic: str):
    """Generate and display eco tip for given topic"""
    with st.spinner(f"Generating eco tip for '{topic}'..."):
        try:
            # Make API request
            response = APIHelper.make_api_request(
    endpoint="/api/eco-tips/generate",
    method="GET",
    data={"topic": topic}
)

            
            if "error" in response:
                st.error(f"Error generating tip: {response['error']}")
                return
            
            # Display the tip
            display_eco_tip(response, topic)
            
            # Save to session state
            save_tip_to_session(response, topic)
            
        except Exception as e:
            st.error(f"Failed to generate eco tip: {str(e)}")
            st.info("💡 Here's a general tip while we fix the connection:")
            display_fallback_tip(topic)

def display_eco_tip(response: Dict, topic: str):
    """Display the generated eco tip in a styled container"""
    tip_text = response.get('tip', response.get('response', 'No tip generated'))
    
    # Format the response text
    formatted_tip = TextProcessor.format_response_text(tip_text)
    
    # Create styled container
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
        border-left: 5px solid #2E8B57;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    '>
        <h4 style='color: #2E8B57; margin-bottom: 1rem; display: flex; align-items: center;'>
            🌱 Eco Tip for "{topic}"
        </h4>
        <p style='color: #444; line-height: 1.6; font-size: 1.1rem; margin-bottom: 0;'>
            {formatted_tip}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Tip", key=f"save_{topic}"):
            st.success("Tip saved to your collection!")
    
    with col2:
        if st.button("🔄 Generate Another", key=f"regenerate_{topic}"):
            generate_eco_tip(topic)
    
    with col3:
        if st.button("📋 Copy Tip", key=f"copy_{topic}"):
            st.success("Tip copied to clipboard!")

def display_fallback_tip(topic: str):
    """Display fallback tip when API is unavailable"""
    fallback_tips = {
        "Energy Conservation": "💡 Switch to LED bulbs - they use 75% less energy and last 25 times longer than incandescent bulbs!",
        "Water Saving": "💧 Fix leaky faucets promptly - a single drip per second can waste over 3,000 gallons per year!",
        "Waste Reduction": "♻️ Start composting kitchen scraps - it reduces waste by 30% and creates nutrient-rich soil!",
        "Sustainable Transport": "🚲 Try bike commuting once a week - it reduces carbon emissions and improves your health!",
        "Green Living": "🌿 Add indoor plants to your home - they purify air and reduce stress levels naturally!",
        "Renewable Energy": "☀️ Consider solar panels - they can reduce electricity bills by 70-90% over their lifetime!",
        "Air Quality": "🌬️ Use natural air fresheners like baking soda and essential oils instead of chemical sprays!",
        "Climate Action": "🌍 Reduce meat consumption by one day per week - it can save 1,900 lbs of CO2 annually!"
    }
    
    # Find the best matching tip
    tip = fallback_tips.get(topic, "🌱 Start small - every eco-friendly action counts towards a sustainable future!")
    
    st.info(tip)

def save_tip_to_session(response: Dict, topic: str):
    """Save tip to session state for later viewing"""
    if 'saved_tips' not in st.session_state:
        st.session_state.saved_tips = []
    
    tip_data = {
        'topic': topic,
        'tip': response.get('tip', response.get('response', '')),
        'timestamp': APIHelper().get_current_timestamp() if hasattr(APIHelper, 'get_current_timestamp') else "Recent"
    }
    
    # Add to beginning of list and limit to 10 tips
    st.session_state.saved_tips.insert(0, tip_data)
    st.session_state.saved_tips = st.session_state.saved_tips[:10]

def display_saved_tips():
    """Display previously saved tips"""
    if 'saved_tips' in st.session_state and st.session_state.saved_tips:
        st.markdown("### 📚 Your Recent Tips")
        
        with st.expander(f"View {len(st.session_state.saved_tips)} Saved Tips"):
            for i, tip_data in enumerate(st.session_state.saved_tips):
                st.markdown(f"""
                <div style='
                    background: #f8f9fa;
                    border-radius: 8px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-left: 3px solid #28a745;
                '>
                    <strong style='color: #28a745;'>🏷️ {tip_data['topic']}</strong><br>
                    <span style='color: #666; font-size: 0.9rem;'>{tip_data.get('timestamp', 'Recent')}</span><br>
                    <p style='margin: 0.5rem 0 0 0; color: #444;'>{tip_data['tip'][:150]}...</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Clear saved tips button
            if st.button("🗑️ Clear All Saved Tips"):
                st.session_state.saved_tips = []
                st.success("All saved tips cleared!")
                st.rerun()

def quick_tips_section():
    """Display quick action buttons for common eco topics"""
    st.markdown("Get instant tips for popular topics:")
    
    # Create quick tip buttons in a grid
    quick_topics = [
        ("💡", "Energy", "Energy Conservation"),
        ("💧", "Water", "Water Saving"),
        ("♻️", "Waste", "Waste Reduction"),
        ("🚲", "Transport", "Sustainable Transport"),
        ("🌿", "Green Living", "Green Living"),
        ("☀️", "Solar", "Renewable Energy")
    ]
    
    cols = st.columns(3)
    for i, (icon, label, topic) in enumerate(quick_topics):
        with cols[i % 3]:
            if st.button(f"{icon} {label}", key=f"quick_{topic}", use_container_width=True):
                generate_eco_tip(topic)

def render_eco_tips_sidebar():
    """Render eco tips information in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌱 Eco Tips Features")
    st.sidebar.markdown("""
    • **AI-Powered Advice**: Get personalized sustainability tips
    • **Multiple Categories**: Energy, water, waste, transport & more
    • **Custom Topics**: Ask about any eco-friendly topic
    • **Save & Review**: Keep track of your favorite tips
    • **Quick Access**: Instant tips for popular topics
    """)
    
    # Add sustainability facts
    st.sidebar.markdown("### 📊 Did You Know?")
    facts = [
        "🌍 Recycling one aluminum can saves enough energy to power a TV for 3 hours",
        "💧 A 5-minute shower uses 25 gallons of water",
        "🚗 Walking or biking for 2 miles prevents 2 lbs of CO2 emissions",
        "🌱 One tree produces enough oxygen for 2 people per day"
    ]
    
    import random
    daily_fact = random.choice(facts)
    st.sidebar.info(daily_fact)

# Additional utility functions for eco tips
def get_eco_tip_analytics():
    """Get analytics about eco tip usage"""
    if 'saved_tips' not in st.session_state:
        return {}
    
    tips = st.session_state.saved_tips
    topics = [tip['topic'] for tip in tips]
    
    from collections import Counter
    topic_counts = Counter(topics)
    
    return {
        'total_tips': len(tips),
        'unique_topics': len(set(topics)),
        'most_popular_topic': topic_counts.most_common(1)[0] if topic_counts else None
    }

def export_saved_tips():
    """Export saved tips to text format"""
    if 'saved_tips' not in st.session_state or not st.session_state.saved_tips:
        return "No saved tips to export."
    
    export_text = "# My Eco Tips Collection\n\n"
    
    for i, tip_data in enumerate(st.session_state.saved_tips, 1):
        export_text += f"## {i}. {tip_data['topic']}\n"
        export_text += f"**Date:** {tip_data.get('timestamp', 'Recent')}\n\n"
        export_text += f"{tip_data['tip']}\n\n"
        export_text += "---\n\n"
    
    return export_text

# Main function to run the component
if __name__ == "__main__":
    render_eco_tips()