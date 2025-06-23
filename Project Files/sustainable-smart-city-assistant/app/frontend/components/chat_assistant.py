# Placeholder for chat_assistant.py
import streamlit as st
import requests
from app.core.config import settings

def show_chat_assistant():
    """Chat assistant interface"""
    st.header("💬 Smart City Chat Assistant")
    st.write("Ask me anything about urban sustainability, city governance, or smart city technologies!")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat input
    user_message = st.text_input(
        "Your question:",
        placeholder="e.g., How can my city reduce carbon emissions?",
        key="chat_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("Send 🚀", type="primary")
    with col2:
        if st.button("Clear Chat 🗑️"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Send message
    if send_button and user_message:
        with st.spinner("Thinking..."):
            try:
                # Call API
                response = requests.post(
                    f"http://{settings.api_host}:{settings.api_port}/api/chat/ask",
                    json={"message": user_message},
                    timeout=30
                )
                
                if response.status_code == 200:
                    ai_response = response.json()["response"]
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "user": user_message,
                        "assistant": ai_response
                    })
                else:
                    st.error("Sorry, I couldn't process your request. Please try again.")
            
            except requests.exceptions.RequestException:
                st.error("🔌 Unable to connect to the AI service. Please check if the backend is running.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💬 Conversation")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            # User message
            st.markdown(f"""
            <div style="
                background: #e3f2fd;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                border-left: 4px solid #2196f3;
            ">
                <strong>🙋 You:</strong> {chat['user']}
            </div>
            """, unsafe_allow_html=True)
            
            # Assistant response
            st.markdown(f"""
            <div style="
                background: #f3e5f5;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                border-left: 4px solid #9c27b0;
            ">
                <strong>🤖 Assistant:</strong> {chat['assistant']}
            </div>
            """, unsafe_allow_html=True)
            
            if i < len(st.session_state.chat_history) - 1:
                st.divider()
