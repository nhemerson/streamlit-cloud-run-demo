import streamlit as st
from datetime import date
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Streaming Cohort Analysis",
    layout="wide"
)

# Title
st.title("Streaming Cohort Analysis")

# Create form container with styling
with st.container():
    st.markdown("""
    <style>
    .filter-container {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        
        # First row - Date range and Timeframe
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Date Range")
            date_col1, date_col2 = st.columns(2)
            with date_col1:
                start_date = st.date_input("", value=date(2024, 10, 10), label_visibility="collapsed")
            with date_col2:
                end_date = st.date_input("", value=date(2025, 4, 8), label_visibility="collapsed")
        
        with col2:
            st.subheader("Timeframe")
            timeframe = st.selectbox("", options=["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"], index=2, label_visibility="collapsed")
        
        # Second row - All dropdowns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("State")
            state = st.selectbox("", options=["All States", "California", "New York", "Texas", "Florida"], label_visibility="collapsed")
        
        with col2:
            st.subheader("Timezone")
            timezone = st.selectbox("", options=["All Timezones", "EST", "CST", "MST", "PST"], label_visibility="collapsed")
        
        with col3:
            st.subheader("Percentage Watched")
            percentage = st.selectbox("", options=["All Percentages", "0-25%", "26-50%", "51-75%", "76-100%"], label_visibility="collapsed")
        
        with col4:
            st.subheader("Genre")
            genre = st.selectbox("", options=["All Genres", "Action", "Comedy", "Drama", "Horror"], label_visibility="collapsed")
        
        # Third row - Rating and Apply button
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Rating")
            rating = st.selectbox("", options=["All Ratings", "G", "PG", "PG-13", "R"], label_visibility="collapsed")
        
        with col2:
            st.write("")
            st.write("")
            apply_btn = st.button("Apply Filters", type="primary", use_container_width=False)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Placeholder for the actual analysis content that would appear after filters are applied
if 'filtered' not in st.session_state:
    st.session_state.filtered = False

if apply_btn:
    st.session_state.filtered = True

if st.session_state.filtered:
    # Create expander for graphs
    with st.expander("Watch Duration Analysis", expanded=True):
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "Total Watch Duration", 
            "Watch Duration by Timezone", 
            "Watch Duration by Type", 
            "Watch Duration by Show"
        ])
        
        # Tab 1 - Total Watch Duration
        with tab1:
            st.subheader("Total Watch Duration Over Time (Monthly)")
            
            # Create sample data for the graph
            months = ["2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04"]
            durations = [1700, 1800, 2100, 2100, 1900, 2050, 200]
            
            # Create DataFrame
            df = pd.DataFrame({
                "Date": months,
                "Total Watch Duration (minutes)": durations
            })
            
            # Create and display the line chart
            fig = px.line(
                df, 
                x="Date", 
                y="Total Watch Duration (minutes)",
                markers=True,
                line_shape="linear",
                color_discrete_sequence=["#20c997"]
            )
            
            fig.update_layout(
                yaxis_range=[0, 2500],
                plot_bgcolor="rgba(240, 255, 250, 0.5)",
                xaxis_title="Date",
                yaxis_title="Watch Duration (minutes)",
                margin=dict(l=20, r=20, t=30, b=20),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tab 2 - Watch Duration by Timezone
        with tab2:
            st.info("Watch Duration by Timezone visualization would appear here.")
        
        # Tab 3 - Watch Duration by Type
        with tab3:
            st.info("Watch Duration by Type visualization would appear here.")
        
        # Tab 4 - Watch Duration by Show
        with tab4:
            st.info("Watch Duration by Show visualization would appear here.")

