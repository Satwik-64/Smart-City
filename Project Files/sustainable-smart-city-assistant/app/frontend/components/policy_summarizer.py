# Placeholder for policy_summarizer.py
import streamlit as st
import requests
import json
from typing import Dict, Any
import tempfile
import os

def render_policy_summarizer():
    """Render the policy document summarizer interface"""
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .policy-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .upload-section {
        background: rgba(30, 60, 114, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #2a5298;
        margin-bottom: 1rem;
    }
    .summary-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    .search-container {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    .result-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #00f2fe;
    }
    .summary-type-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.8rem;
    }
    .metrics-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="policy-header">
        <h1>📋 Policy Document Summarizer</h1>
        <p>Transform complex policy documents into clear, actionable summaries using AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main interface tabs
    tab1, tab2, tab3 = st.tabs(["📄 Summarize Text", "📁 Upload Document", "🔍 Search Policies"])
    
    with tab1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        
        st.subheader("✍️ Text Input Summarization")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Text input for policy content
            policy_text = st.text_area(
                "📝 Enter Policy Text",
                placeholder="Paste your policy document text here...",
                height=300,
                help="Copy and paste the policy text you want to summarize"
            )
            
            # Summary type selection
            summary_type = st.selectbox(
                "🎯 Summary Type",
                ["citizen-friendly", "executive", "technical"],
                help="Choose the type of summary you need"
            )
            
            # Summary options
            col_a, col_b = st.columns(2)
            with col_a:
                include_key_points = st.checkbox("🔑 Include Key Points", value=True)
            with col_b:
                include_impacts = st.checkbox("📊 Include Impact Analysis", value=True)
        
        with col2:
            st.markdown("### 📋 Summary Types")
            
            type_descriptions = {
                "citizen-friendly": "👥 Easy to understand language for general public",
                "executive": "👔 Concise overview for decision makers", 
                "technical": "🔧 Detailed technical implementation focus"
            }
            
            for stype, desc in type_descriptions.items():
                st.markdown(f"**{stype}:** {desc}")
        
        # Summarize button
        if st.button("🚀 Generate Summary", key="text_summarize", use_container_width=True):
            if policy_text.strip():
                with st.spinner("🤖 AI is analyzing your policy document..."):
                    try:
                        # Prepare request data
                        request_data = {
                            "text": policy_text,
                            "summary_type": summary_type
                        }
                        
                        # Call backend API
                        response = requests.post(
                            "http://localhost:8000/api/policy/summarize",
                            json=request_data,
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Display summary
                            st.markdown(f"""
                            <div class="summary-container">
                                <h3>📋 Policy Summary ({summary_type})</h3>
                                <div class="metrics-container">
                                    <strong>Original Length:</strong> {result.get('original_length', 0):,} characters<br>
                                    <strong>Summary Length:</strong> {len(result.get('summary', '')):,} characters<br>
                                    <strong>Compression Ratio:</strong> {(len(result.get('summary', '')) / max(result.get('original_length', 1), 1) * 100):.1f}%
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Summary content
                            st.markdown("### 📄 Summary Content")
                            st.write(result.get('summary', 'No summary generated'))
                            
                            # Copy button
                            st.code(result.get('summary', ''), language='text')
                            
                            # Download option
                            st.download_button(
                                "📥 Download Summary",
                                result.get('summary', ''),
                                file_name=f"policy_summary_{summary_type}.txt",
                                mime="text/plain"
                            )
                            
                        else:
                            st.error(f"❌ Error: {response.status_code} - {response.text}")
                            
                    except requests.exceptions.RequestException as e:
                        st.error(f"🌐 Connection Error: {str(e)}")
                    except Exception as e:
                        st.error(f"⚠️ Unexpected Error: {str(e)}")
                        
            else:
                st.warning("⚠️ Please enter some policy text to summarize")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        
        st.subheader("📁 Document Upload & Summarization")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # File upload
            uploaded_file = st.file_uploader(
                "📎 Choose Policy Document",
                type=['txt', 'pdf', 'docx'],
                help="Upload a policy document to summarize"
            )
            
            if uploaded_file:
                # File info
                st.info(f"📄 **File:** {uploaded_file.name}")
                st.info(f"📊 **Size:** {uploaded_file.size:,} bytes")
                st.info(f"🔖 **Type:** {uploaded_file.type}")
                
                # Summary type for file
                file_summary_type = st.selectbox(
                    "🎯 Summary Type for File",
                    ["citizen-friendly", "executive", "technical"],
                    key="file_summary_type"
                )
                
                # Process file button
                if st.button("🔄 Process Document", key="file_process", use_container_width=True):
                    with st.spinner("📖 Processing document..."):
                        try:
                            # Prepare file for upload
                            files = {
                                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                            }
                            
                            data = {
                                "summary_type": file_summary_type
                            }
                            
                            # Call backend API
                            response = requests.post(
                                "http://localhost:8000/api/policy/summarize-file",
                                files=files,
                                data=data,
                                timeout=60
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                
                                # Display results
                                st.success("✅ Document processed successfully!")
                                
                                # Summary display
                                st.markdown(f"""
                                <div class="summary-container">
                                    <h3>📋 Document Summary ({file_summary_type})</h3>
                                    <div class="metrics-container">
                                        <strong>Original Length:</strong> {result.get('original_length', 0):,} characters<br>
                                        <strong>Summary Length:</strong> {len(result.get('summary', '')):,} characters
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown("### 📄 Summary Content")
                                st.write(result.get('summary', 'No summary generated'))
                                
                                # Download options
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.download_button(
                                        "📥 Download Summary",
                                        result.get('summary', ''),
                                        file_name=f"summary_{uploaded_file.name}_{file_summary_type}.txt",
                                        mime="text/plain"
                                    )
                                
                                with col_b:
                                    # Create full report
                                    full_report = f"""
POLICY DOCUMENT SUMMARY REPORT
===============================

Original Document: {uploaded_file.name}
Summary Type: {file_summary_type}
Generated: {st.session_state.get('current_time', 'Unknown')}

SUMMARY:
{result.get('summary', 'No summary available')}

DOCUMENT STATISTICS:
- Original Length: {result.get('original_length', 0):,} characters
- Summary Length: {len(result.get('summary', '')):,} characters
- Compression Ratio: {(len(result.get('summary', '')) / max(result.get('original_length', 1), 1) * 100):.1f}%
                                    """
                                    
                                    st.download_button(
                                        "📋 Download Full Report",
                                        full_report,
                                        file_name=f"policy_report_{uploaded_file.name}_{file_summary_type}.txt",
                                        mime="text/plain"
                                    )
                                
                            else:
                                st.error(f"❌ Error processing document: {response.status_code}")
                                
                        except requests.exceptions.RequestException as e:
                            st.error(f"🌐 Connection Error: {str(e)}")
                        except Exception as e:
                            st.error(f"⚠️ Processing Error: {str(e)}")
        
        with col2:
            st.markdown("### 📋 Supported Formats")
            st.markdown("""
            - **📄 Text Files (.txt)** - Plain text documents
            - **📄 PDF Files (.pdf)** - Portable Document Format
            - **📄 Word Files (.docx)** - Microsoft Word documents
            """)
            
            st.markdown("### 💡 Tips for Better Results")
            tips = [
                "📝 Use well-formatted documents",
                "🔍 Ensure text is readable/searchable",
                "📏 Optimal size: 1KB - 10MB",
                "🎯 Choose appropriate summary type",
                "📋 Review generated summaries"
            ]
            
            for tip in tips:
                st.markdown(f"• {tip}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        st.subheader("🔍 Policy Document Search")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Search interface
            search_query = st.text_input(
                "🔍 Search Policy Documents",
                placeholder="Enter keywords to search policies...",
                help="Search through uploaded policy documents"
            )
            
            # Search options
            col_a, col_b = st.columns(2)
            with col_a:
                include_summary = st.checkbox("📋 Include AI Summaries", value=True)
            with col_b:
                max_results = st.selectbox("📊 Max Results", [5, 10, 15, 20], index=0)
            
            # Search button
            if st.button("🔍 Search Policies", key="search_policies", use_container_width=True):
                if search_query.strip():
                    with st.spinner("🔍 Searching policy documents..."):
                        try:
                            # Prepare search request
                            search_data = {
                                "query": search_query,
                                "include_summary": include_summary
                            }
                            
                            # Call backend API
                            response = requests.post(
                                "http://localhost:8000/api/policy/search",
                                json=search_data,
                                timeout=30
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                results = result.get('results', [])
                                summaries = result.get('summaries', {})
                                
                                if results:
                                    st.success(f"✅ Found {len(results)} relevant policy documents")
                                    
                                    # Display results
                                    for i, doc in enumerate(results[:max_results]):
                                        with st.expander(f"📄 {doc.get('filename', f'Document {i+1}')} (Score: {doc.get('score', 0):.3f})"):
                                            
                                            # Document metadata
                                            col_x, col_y = st.columns([2, 1])
                                            
                                            with col_x:
                                                st.markdown(f"**Document ID:** {doc.get('document_id', 'N/A')}")
                                                st.markdown(f"**Relevance Score:** {doc.get('score', 0):.3f}")
                                                
                                                # Content preview
                                                content = doc.get('content', '')
                                                if content:
                                                    st.markdown("**Content Preview:**")
                                                    st.text(content[:500] + "..." if len(content) > 500 else content)
                                            
                                            with col_y:
                                                st.markdown(f"**Filename:** {doc.get('filename', 'N/A')}")
                                                metadata = doc.get('metadata', {})
                                                if metadata:
                                                    st.markdown("**Metadata:**")
                                                    for key, value in metadata.items():
                                                        if key not in ['content']:
                                                            st.text(f"{key}: {value}")
                                            
                                            # AI Summary if available
                                            doc_id = doc.get('id', '')
                                            if include_summary and doc_id in summaries:
                                                st.markdown("### 🤖 AI Summary")
                                                st.info(summaries[doc_id])
                                            
                                            # Action buttons
                                            col_btn1, col_btn2 = st.columns(2)
                                            with col_btn1:
                                                if st.button(f"📋 Summarize", key=f"summarize_{i}"):
                                                    # Trigger summarization for this document
                                                    pass
                                            with col_btn2:
                                                if st.button(f"📥 Download", key=f"download_{i}"):
                                                    # Download document content
                                                    pass
                                    
                                else:
                                    st.warning("❌ No policy documents found matching your search query")
                                    
                            else:
                                st.error(f"❌ Search Error: {response.status_code}")
                                
                        except requests.exceptions.RequestException as e:
                            st.error(f"🌐 Connection Error: {str(e)}")
                        except Exception as e:
                            st.error(f"⚠️ Search Error: {str(e)}")
                            
                else:
                    st.warning("⚠️ Please enter a search query")
        
        with col2:
            st.markdown("### 📊 Policy Categories")
            
            # Fetch policy categories
            try:
                response = requests.get("http://localhost:8000/api/policy/categories", timeout=5)
                if response.status_code == 200:
                    categories = response.json().get('categories', [])
                    
                    for category in categories:
                        if st.button(f"{category.get('icon', '📋')} {category.get('name', 'Unknown')}", 
                                   key=f"cat_{category.get('name', 'unknown')}", 
                                   help=category.get('description', '')):
                            # Set search query to category name
                            st.session_state.search_query = category.get('name', '')
                            st.rerun()
                else:
                    # Fallback categories
                    default_categories = [
                        "🌿 Environmental", "🚌 Transportation", "🏠 Housing",
                        "⚡ Energy", "♻️ Waste Management", "💧 Water Management"
                    ]
                    for cat in default_categories:
                        st.button(cat, key=f"default_{cat}")
                        
            except:
                st.info("📋 Categories loading...")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer section
    st.markdown("---")
    
    # Statistics and usage info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Documents Processed", "1,234", "↗️ 15%")
    
    with col2:
        st.metric("📋 Summaries Generated", "2,567", "↗️ 23%")
    
    with col3:
        st.metric("🔍 Searches Performed", "5,432", "↗️ 18%")
    
    with col4:
        st.metric("👥 Active Users", "456", "↗️ 8%")

if __name__ == "__main__":
    render_policy_summarizer()