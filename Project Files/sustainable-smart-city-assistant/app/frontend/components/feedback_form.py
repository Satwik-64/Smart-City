# Placeholder for feedback_form.py
import streamlit as st
import requests
from datetime import datetime
import json

def render_feedback_form():
    """Render the citizen feedback form"""
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .feedback-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    .feedback-form {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
    }
    .success-message {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .error-message {
        background: linear-gradient(135deg, #f44336, #da190b);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="feedback-container">
        <h1>🗣️ Citizen Feedback Portal</h1>
        <p>Share your thoughts and suggestions to help improve our city's sustainability initiatives</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main feedback form
    with st.container():
        st.markdown('<div class="feedback-form">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Submit Your Feedback")
            
            # Feedback form
            with st.form("feedback_form", clear_on_submit=True):
                # Personal Information
                name = st.text_input("👤 Your Name", placeholder="Enter your full name")
                email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
                
                # Feedback Category
                categories = [
                    "🌱 Environmental Issues",
                    "🚌 Public Transportation", 
                    "♻️ Waste Management",
                    "💧 Water Quality",
                    "⚡ Energy Efficiency",
                    "🏢 Urban Planning",
                    "🏥 Public Health",
                    "🎓 Education",
                    "💼 Economic Development",
                    "🔧 Other"
                ]
                category = st.selectbox("📋 Category", categories)
                
                # Priority Level
                priority = st.radio(
                    "⚡ Priority Level",
                    ["🟢 Low", "🟡 Medium", "🔴 High", "🚨 Critical"],
                    horizontal=True
                )
                
                # Feedback Message
                message = st.text_area(
                    "💬 Your Feedback",
                    placeholder="Please describe your feedback, suggestions, or concerns in detail...",
                    height=150
                )
                
                # Location (optional)
                location = st.text_input("📍 Location (Optional)", placeholder="e.g., Downtown, Park Avenue, etc.")
                
                # Submit button
                submitted = st.form_submit_button("🚀 Submit Feedback", use_container_width=True)
                
                if submitted:
                    if name and email and category and message:
                        # Prepare feedback data
                        feedback_data = {
                            "name": name,
                            "email": email,
                            "category": category.split(" ", 1)[1],  # Remove emoji
                            "priority": priority.split(" ", 1)[1],  # Remove emoji
                            "message": message,
                            "location": location if location else "Not specified",
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        # Submit to backend
                        try:
                            response = requests.post(
                                "http://localhost:8000/api/feedback/submit",
                                json=feedback_data,
                                timeout=10
                            )
                            
                            if response.status_code == 200:
                                st.markdown("""
                                <div class="success-message">
                                    ✅ <strong>Thank you!</strong> Your feedback has been submitted successfully. 
                                    We'll review it and take appropriate action.
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Show feedback ID
                                result = response.json()
                                if "feedback_id" in result:
                                    st.success(f"📋 Feedback ID: {result['feedback_id']}")
                                
                            else:
                                st.markdown("""
                                <div class="error-message">
                                    ❌ <strong>Error!</strong> There was a problem submitting your feedback. 
                                    Please try again later.
                                </div>
                                """, unsafe_allow_html=True)
                                
                        except requests.exceptions.RequestException as e:
                            st.markdown("""
                            <div class="error-message">
                                ❌ <strong>Connection Error!</strong> Unable to connect to the server. 
                                Please check your internet connection and try again.
                            </div>
                            """, unsafe_allow_html=True)
                            
                    else:
                        st.error("⚠️ Please fill in all required fields (Name, Email, Category, and Message)")
        
        with col2:
            st.subheader("📊 Feedback Statistics")
            
            # Mock statistics (in real app, fetch from backend)
            with st.container():
                st.metric("Total Feedback", "1,247", "↗️ 12%")
                st.metric("This Month", "89", "↗️ 23%")
                st.metric("Response Rate", "94%", "↗️ 2%")
            
            st.subheader("🔥 Popular Categories")
            popular_categories = [
                "Environmental Issues",
                "Public Transportation", 
                "Waste Management", 
                "Water Quality",
                "Urban Planning"
            ]
            
            for cat in popular_categories:
                st.markdown(f'<div class="category-badge">{cat}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Feedback Section
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📋 Recent Community Feedback")
        
        # Fetch recent feedback (mock data for demo)
        try:
            # In real app: response = requests.get("http://localhost:8000/feedback/recent")
            recent_feedback = [
                {
                    "id": "FB001",
                    "name": "John Doe",
                    "category": "Environmental Issues",
                    "message": "More recycling bins needed in downtown area...",
                    "priority": "Medium",
                    "timestamp": "2024-01-15T10:30:00",
                    "status": "Under Review"
                },
                {
                    "id": "FB002", 
                    "name": "Jane Smith",
                    "category": "Public Transportation",
                    "message": "Bus frequency should be increased during peak hours...",
                    "priority": "High",
                    "timestamp": "2024-01-14T15:45:00",
                    "status": "In Progress"
                },
                {
                    "id": "FB003",
                    "name": "Mike Johnson",
                    "category": "Water Quality",
                    "message": "Water pressure is low in residential areas...",
                    "priority": "High",
                    "timestamp": "2024-01-13T09:20:00",
                    "status": "Resolved"
                }
            ]
            
            for feedback in recent_feedback:
                with st.expander(f"💬 {feedback['category']} - {feedback['name']} ({feedback['id']})"):
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.write(f"**Message:** {feedback['message']}")
                        st.write(f"**Priority:** {feedback['priority']}")
                        st.write(f"**Date:** {feedback['timestamp'][:10]}")
                    
                    with col_b:
                        status_color = {
                            "Under Review": "🟡",
                            "In Progress": "🔵", 
                            "Resolved": "🟢",
                            "Closed": "⚫"
                        }
                        st.write(f"**Status:** {status_color.get(feedback['status'], '🔵')} {feedback['status']}")
                        
        except Exception as e:
            st.info("📝 No recent feedback available at the moment.")
    
    with col2:
        st.subheader("💡 Tips for Good Feedback")
        
        tips = [
            "🎯 Be specific about the issue",
            "📍 Include location details",
            "📸 Add photos if relevant",
            "🔍 Check if it's already reported",
            "📞 Use appropriate priority level"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")
        
        st.markdown("---")
        
        # Contact Information
        st.subheader("📞 Emergency Contacts")
        st.markdown("""
        **🚨 Emergency:** 911  
        **🏛️ City Hall:** (555) 123-4567  
        **🔧 Utilities:** (555) 987-6543  
        **♻️ Waste Mgmt:** (555) 456-7890
        """)

if __name__ == "__main__":
    render_feedback_form()