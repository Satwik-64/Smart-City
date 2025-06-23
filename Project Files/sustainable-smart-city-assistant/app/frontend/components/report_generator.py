# Placeholder for report_generator.py
import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64

# Backend API base URL
API_BASE_URL = "http://localhost:8000"

def report_generation_page():
    """Main report generation page component"""
    
    # Page header with styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; text-align: center; margin: 0;">
            🏙️ City Sustainability Report Generator
        </h1>
        <p style="color: white; text-align: center; margin-top: 10px; font-size: 1.1em;">
            Generate comprehensive AI-powered sustainability reports for smart cities
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different report types
    tab1, tab2, tab3 = st.tabs(["📊 City Dashboard Report", "📈 KPI Analysis Report", "🔄 Custom Report"])
    
    with tab1:
        city_dashboard_report()
    
    with tab2:
        kpi_analysis_report()
    
    with tab3:
        custom_report_generator()

def city_dashboard_report():
    """Generate reports based on city dashboard data"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🏙️ Select City for Report")
        
        # Fetch available cities
        try:
            response = requests.get(f"{API_BASE_URL}/api/dashboard/cities")
            if response.status_code == 200:
                cities_data = response.json()
                cities = cities_data.get("cities", [])
            else:
                cities = ["New York", "San Francisco", "Chicago"]  # Fallback
        except:
            cities = ["New York", "San Francisco", "Chicago"]  # Fallback
        
        selected_city = st.selectbox("Choose a city:", cities)
        
        # Report type selection
        report_type = st.selectbox(
            "Report Type:",
            ["Executive Summary", "Technical Analysis", "Citizen-Friendly", "Comprehensive"]
        )
        
        # Time period selection
        time_period = st.selectbox(
            "Time Period:",
            ["Current Status", "Last 30 Days", "Last Quarter", "Annual Report"]
        )
        
    with col2:
        st.subheader("📋 Report Options")
        
        include_charts = st.checkbox("Include Charts", value=True)
        include_recommendations = st.checkbox("Include AI Recommendations", value=True)
        include_comparisons = st.checkbox("Include City Comparisons", value=False)
        
        # Report format
        report_format = st.radio("Output Format:", ["View Online", "Download PDF", "Export CSV"])
    
    # Generate report button
    if st.button("🔥 Generate City Report", type="primary", use_container_width=True):
        with st.spinner("Generating comprehensive city report..."):
            generate_city_report(selected_city, report_type, time_period, 
                               include_charts, include_recommendations, include_comparisons, report_format)

def generate_city_report(city, report_type, time_period, include_charts, include_recommendations, include_comparisons, report_format):
    """Generate and display city sustainability report"""
    
    try:
        # Fetch city data
        response = requests.get(f"{API_BASE_URL}/api/dashboard/city/{city}")
        if response.status_code != 200:
            st.error("Failed to fetch city data")
            return
        
        city_data = response.json()
        
        # Create report data structure
        report_data = {
            "city_name": city,
            "report_type": report_type,
            "time_period": time_period,
            "kpis": city_data.get("kpis", []),
            "alerts": city_data.get("alerts", []),
            "generation_time": datetime.now().isoformat()
        }
        
        # Generate AI report content
        ai_report = generate_ai_report_content(report_data, include_recommendations)
        
        # Display report
        display_report(report_data, ai_report, include_charts, include_comparisons)
        
        # Handle different output formats
        if report_format == "Download PDF":
            generate_pdf_report(report_data, ai_report)
        elif report_format == "Export CSV":
            generate_csv_export(report_data)
            
    except Exception as e:
        st.error(f"Error generating report: {str(e)}")

def generate_ai_report_content(report_data, include_recommendations):
    """Generate AI-powered report content using Granite LLM"""
    
    try:
        # Prepare prompt for AI report generation
        prompt_data = {
            "city_name": report_data["city_name"],
            "kpis": report_data["kpis"],
            "alerts": report_data["alerts"],
            "report_type": report_data["report_type"],
            "include_recommendations": include_recommendations
        }
        
        response = requests.post(f"{API_BASE_URL}/reports/generate", json=prompt_data)
        
        if response.status_code == 200:
            return response.json().get("report_content", "")
        else:
            return generate_fallback_report(report_data)
            
    except Exception as e:
        st.warning(f"AI report generation failed: {str(e)}. Using fallback content.")
        return generate_fallback_report(report_data)

def generate_fallback_report(report_data):
    """Generate fallback report content when AI service is unavailable"""
    
    city = report_data["city_name"]
    kpis = report_data["kpis"]
    
    report_content = f"""
# Sustainability Report: {city}

## Executive Summary
This report provides an overview of {city}'s current sustainability performance across key indicators.

## Key Performance Indicators
"""
    
    for kpi in kpis:
        report_content += f"""
### {kpi.get('name', 'Unknown Metric')}
- **Current Value:** {kpi.get('value', 'N/A')} {kpi.get('unit', '')}
- **Trend:** {kpi.get('trend', 'No trend data')}
- **Category:** {kpi.get('category', 'General')}
"""
    
    report_content += """
## Recommendations
Based on the current data, the following actions are recommended:
- Continue monitoring key sustainability metrics
- Focus on areas showing negative trends
- Implement data-driven policy decisions
- Engage citizens in sustainability initiatives
"""
    
    return report_content

def display_report(report_data, ai_content, include_charts, include_comparisons):
    """Display the generated report with visualizations"""
    
    # Report header
    st.markdown("---")
    st.markdown(f"## 📄 Sustainability Report: {report_data['city_name']}")
    st.markdown(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    st.markdown(f"**Report Type:** {report_data['report_type']}")
    
    # AI-generated content
    st.markdown("### 🤖 AI Analysis")
    st.markdown(ai_content)
    
    # KPI Dashboard
    st.markdown("### 📊 Key Performance Indicators")
    
    if include_charts:
        display_kpi_charts(report_data["kpis"])
    else:
        display_kpi_table(report_data["kpis"])
    
    # Alerts section
    if report_data.get("alerts"):
        st.markdown("### 🚨 Current Alerts")
        display_alerts(report_data["alerts"])
    
    # City comparisons
    if include_comparisons:
        st.markdown("### 🏙️ City Comparisons")
        display_city_comparisons(report_data["city_name"])

def display_kpi_charts(kpis):
    """Display KPI data as interactive charts"""
    
    if not kpis:
        st.info("No KPI data available")
        return
    
    # Create columns for charts
    col1, col2 = st.columns(2)
    
    # Prepare data for charts
    kpi_names = [kpi.get('name', 'Unknown') for kpi in kpis]
    kpi_values = [kpi.get('value', 0) for kpi in kpis]
    kpi_categories = [kpi.get('category', 'General') for kpi in kpis]
    
    with col1:
        # Bar chart of KPI values
        fig_bar = px.bar(
            x=kpi_names,
            y=kpi_values,
            title="KPI Values",
            color=kpi_categories,
            labels={'x': 'Metrics', 'y': 'Values'}
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Pie chart of KPI categories
        category_counts = {}
        for category in kpi_categories:
            category_counts[category] = category_counts.get(category, 0) + 1
        
        fig_pie = px.pie(
            values=list(category_counts.values()),
            names=list(category_counts.keys()),
            title="KPI Categories Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Trend indicators
    st.markdown("#### 📈 Trend Analysis")
    trend_cols = st.columns(len(kpis))
    
    for i, kpi in enumerate(kpis):
        with trend_cols[i]:
            trend = kpi.get('trend', '0%')
            trend_value = trend.replace('%', '').replace('+', '').replace('-', '')
            
            if '+' in trend:
                st.metric(
                    label=kpi.get('name', 'Unknown'),
                    value=f"{kpi.get('value', 0)} {kpi.get('unit', '')}",
                    delta=trend,
                    delta_color="normal"
                )
            elif '-' in trend:
                st.metric(
                    label=kpi.get('name', 'Unknown'),
                    value=f"{kpi.get('value', 0)} {kpi.get('unit', '')}",
                    delta=trend,
                    delta_color="inverse"
                )
            else:
                st.metric(
                    label=kpi.get('name', 'Unknown'),
                    value=f"{kpi.get('value', 0)} {kpi.get('unit', '')}"
                )

def display_kpi_table(kpis):
    """Display KPI data as a formatted table"""
    
    if not kpis:
        st.info("No KPI data available")
        return
    
    # Convert to DataFrame for better display
    df = pd.DataFrame([
        {
            "Metric": kpi.get('name', 'Unknown'),
            "Value": kpi.get('value', 'N/A'),
            "Unit": kpi.get('unit', ''),
            "Trend": kpi.get('trend', 'No data'),
            "Category": kpi.get('category', 'General')
        }
        for kpi in kpis
    ])
    
    st.dataframe(df, use_container_width=True)

def display_alerts(alerts):
    """Display city alerts with appropriate styling"""
    
    for alert in alerts:
        alert_type = alert.get('type', 'info')
        message = alert.get('message', 'No message')
        
        if alert_type == 'warning':
            st.warning(f"⚠️ {message}")
        elif alert_type == 'success':
            st.success(f"✅ {message}")
        elif alert_type == 'error':
            st.error(f"❌ {message}")
        else:
            st.info(f"ℹ️ {message}")

def display_city_comparisons(current_city):
    """Display comparisons with other cities"""
    
    try:
        # Fetch data for all cities
        response = requests.get(f"{API_BASE_URL}/api/dashboard/cities")
        if response.status_code != 200:
            st.error("Failed to fetch city comparison data")
            return
        
        cities_data = response.json()
        cities = cities_data.get("cities", [])
        
        # Create comparison data
        comparison_data = []
        for city in cities[:3]:  # Limit to 3 cities for comparison
            try:
                city_response = requests.get(f"{API_BASE_URL}/api/dashboard/city/{city}")
                if city_response.status_code == 200:
                    city_data = city_response.json()
                    comparison_data.append({
                        "city": city,
                        "data": city_data.get("kpis", [])
                    })
            except:
                continue
        
        if comparison_data:
            # Create comparison chart
            create_comparison_chart(comparison_data, current_city)
        else:
            st.info("Comparison data not available")
            
    except Exception as e:
        st.error(f"Error generating city comparisons: {str(e)}")

def create_comparison_chart(comparison_data, current_city):
    """Create comparison charts between cities"""
    
    # Extract common metrics
    common_metrics = ["Air Quality", "Energy Consumption", "Waste Recycled"]
    
    for metric in common_metrics:
        st.markdown(f"#### {metric} Comparison")
        
        cities = []
        values = []
        
        for city_data in comparison_data:
            city_name = city_data["city"]
            kpis = city_data["data"]
            
            # Find matching metric
            for kpi in kpis:
                if metric.lower() in kpi.get('name', '').lower():
                    cities.append(city_name)
                    values.append(kpi.get('value', 0))
                    break
        
        if cities and values:
            # Create bar chart
            colors = ['#ff6b6b' if city == current_city else '#4ecdc4' for city in cities]
            
            fig = go.Figure(data=[
                go.Bar(x=cities, y=values, marker_color=colors)
            ])
            
            fig.update_layout(
                title=f"{metric} by City",
                xaxis_title="Cities",
                yaxis_title="Value"
            )
            
            st.plotly_chart(fig, use_container_width=True)

def kpi_analysis_report():
    """Generate reports from uploaded KPI files"""
    
    st.subheader("📈 KPI File Analysis Report")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload
        uploaded_file = st.file_uploader(
            "Upload KPI Data File",
            type=['csv'],
            help="Upload a CSV file with KPI data for analysis"
        )
        
        if uploaded_file:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Analysis options
            forecast_periods = st.slider("Forecast Periods", 1, 24, 12)
            city_name = st.text_input("City Name", value="Smart City")
    
    with col2:
        st.subheader("📊 Analysis Options")
        
        include_forecast = st.checkbox("Include Forecasting", value=True)
        include_anomalies = st.checkbox("Anomaly Detection", value=True)
        include_trends = st.checkbox("Trend Analysis", value=True)
    
    # Generate analysis
    if uploaded_file and st.button("🔬 Analyze KPI Data", type="primary"):
        with st.spinner("Analyzing KPI data..."):
            analyze_kpi_file(uploaded_file, forecast_periods, city_name, 
                           include_forecast, include_anomalies, include_trends)

def analyze_kpi_file(uploaded_file, forecast_periods, city_name, include_forecast, include_anomalies, include_trends):
    """Analyze uploaded KPI file and generate report"""
    
    try:
        # Prepare file for upload
        files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
        data = {
            "forecast_periods": forecast_periods,
            "city_name": city_name
        }
        
        # Send to backend for analysis
        response = requests.post(
            f"{API_BASE_URL}/api/kpi/upload-analyze",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            analysis_result = response.json()
            display_kpi_analysis(analysis_result, include_forecast, include_anomalies, include_trends)
        else:
            st.error("Failed to analyze KPI file")
            
    except Exception as e:
        st.error(f"Error analyzing KPI file: {str(e)}")

def display_kpi_analysis(analysis_result, include_forecast, include_anomalies, include_trends):
    """Display KPI analysis results"""
    
    st.markdown("---")
    st.markdown("## 📊 KPI Analysis Results")
    
    # Summary statistics
    summary_stats = analysis_result.get("summary_stats", {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", summary_stats.get("total_records", "N/A"))
    
    with col2:
        st.metric("Data Columns", len(summary_stats.get("columns", [])))
    
    with col3:
        date_range = summary_stats.get("date_range", {})
        start_date = date_range.get("start", "N/A")
        st.metric("Start Date", start_date)
    
    with col4:
        end_date = date_range.get("end", "N/A")
        st.metric("End Date", end_date)
    
    # Forecast results
    if include_forecast:
        st.markdown("### 📈 Forecasting Results")
        forecast_results = analysis_result.get("forecast_results", {})
        
        if forecast_results:
            st.json(forecast_results)
        else:
            st.info("No forecast data available")
    
    # Anomaly detection
    if include_anomalies:
        st.markdown("### 🔍 Anomaly Detection")
        anomaly_results = analysis_result.get("anomaly_results", {})
        
        if anomaly_results:
            st.json(anomaly_results)
        else:
            st.info("No anomalies detected")

def custom_report_generator():
    """Custom report generator with user-defined parameters"""
    
    st.subheader("🔧 Custom Report Builder")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Report Configuration")
        
        report_title = st.text_input("Report Title", value="Custom Sustainability Report")
        report_description = st.text_area("Report Description", 
                                        value="Custom analysis of sustainability metrics")
        
        # Data sources
        st.markdown("#### Data Sources")
        use_dashboard_data = st.checkbox("Include City Dashboard Data", value=True)
        use_uploaded_data = st.checkbox("Include Uploaded Files", value=False)
        use_policy_data = st.checkbox("Include Policy Documents", value=False)
    
    with col2:
        st.markdown("#### Content Options")
        
        sections = st.multiselect(
            "Report Sections",
            ["Executive Summary", "KPI Analysis", "Trend Analysis", "Recommendations", 
             "Comparisons", "Forecasting", "Policy Impact"],
            default=["Executive Summary", "KPI Analysis", "Recommendations"]
        )
        
        output_format = st.selectbox("Output Format", ["Markdown", "HTML", "PDF"])
        
        # AI enhancement options
        ai_enhancement = st.checkbox("AI-Enhanced Content", value=True)
        if ai_enhancement:
            tone = st.selectbox("Report Tone", ["Professional", "Technical", "Citizen-Friendly"])
    
    # Generate custom report
    if st.button("🎯 Generate Custom Report", type="primary", use_container_width=True):
        with st.spinner("Building your custom report..."):
            generate_custom_report(report_title, report_description, sections, 
                                 use_dashboard_data, ai_enhancement, output_format)

def generate_custom_report(title, description, sections, use_dashboard_data, ai_enhancement, output_format):
    """Generate custom report based on user specifications"""
    
    st.markdown("---")
    st.markdown(f"# {title}")
    st.markdown(f"*{description}*")
    st.markdown(f"**Generated:** {datetime.now().strftime('%B %d, %Y')}")
    
    for section in sections:
        st.markdown(f"## {section}")
        
        if section == "Executive Summary":
            if ai_enhancement:
                st.markdown("*AI-generated executive summary based on current data trends...*")
            st.markdown("This section provides a high-level overview of key findings and recommendations.")
            
        elif section == "KPI Analysis":
            if use_dashboard_data:
                st.markdown("Analyzing current city dashboard metrics...")
                # Add KPI analysis here
            else:
                st.markdown("KPI analysis would be based on uploaded data files.")
                
        elif section == "Recommendations":
            st.markdown("Based on the analysis, the following recommendations are provided:")
            st.markdown("- Implement data-driven policy decisions")
            st.markdown("- Focus on improving metrics with negative trends")
            st.markdown("- Engage stakeholders in sustainability initiatives")
            
        # Add more sections as needed
        
    st.success(f"Custom report generated successfully! Format: {output_format}")

def generate_pdf_report(report_data, ai_content):
    """Generate downloadable PDF report"""
    
    # This is a placeholder for PDF generation
    # In a real implementation, you would use libraries like reportlab or weasyprint
    
    st.info("PDF generation feature - Implementation needed")
    st.markdown("To implement PDF generation, you can use:")
    st.code("""
# Install: pip install reportlab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf_report(report_data, content):
    # PDF generation logic here
    pass
    """)

def generate_csv_export(report_data):
    """Generate CSV export of report data"""
    
    try:
        # Convert KPI data to DataFrame
        kpis = report_data.get("kpis", [])
        if kpis:
            df = pd.DataFrame(kpis)
            
            # Create download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV Report",
                data=csv,
                file_name=f"{report_data['city_name']}_sustainability_report.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data available for CSV export")
            
    except Exception as e:
        st.error(f"Error generating CSV export: {str(e)}")

# Utility functions for styling
def apply_report_styling():
    """Apply custom CSS styling for reports"""
    
    st.markdown("""
    <style>
    .report-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply styling when module is imported
apply_report_styling()