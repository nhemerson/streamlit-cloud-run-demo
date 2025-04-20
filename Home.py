import streamlit as st
import os
import shutil

# Check if theme.toml exists and config.toml doesn't exist - copy theme to config
streamlit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.streamlit')
theme_path = os.path.join(streamlit_dir, 'theme.toml')
config_path = os.path.join(streamlit_dir, 'config.toml')

if os.path.exists(theme_path) and not os.path.exists(config_path):
    # Create the .streamlit directory if it doesn't exist
    os.makedirs(streamlit_dir, exist_ok=True)
    # Copy theme.toml to config.toml
    shutil.copyfile(theme_path, config_path)
    print("Copied theme settings from theme.toml to config.toml")

# Page config must be first Streamlit command
st.set_page_config(
    page_title="Streaming Cohort Analysis",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Add custom CSS to enforce light theme and disable theme switcher
st.markdown("""
<style>
    /* Force light theme */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }
    
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Hide dark mode toggle */
    [data-testid="stToolbar"] [data-testid="baseButton-headerNoPadding"] {
        display: none;
    }

    /* Additional styling for nicer appearance */
    .plot-container {
        border-radius: 5px;
        box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
        padding: 10px;
        margin-bottom: 15px;
    }

    .stButton button {
        border-radius: 4px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

import pandas as pd
import plotly.express as px
import json
from datetime import datetime, date

# Load data
@st.cache_data
def load_data():
    with open('data/streaming_data.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    # Convert dates to datetime
    df['created_date'] = pd.to_datetime(df['created_date'])
    
    # Calculate percentage watched
    df['percentage_watched'] = (df['user_watch_duration_seconds'] / df['show_duration_seconds'] * 100).round(0)
    
    # Create percentage categories
    df['percentage_category'] = pd.cut(
        df['percentage_watched'],
        bins=[0, 25, 50, 75, 100],
        labels=['0-25%', '26-50%', '51-75%', '76-100%'],
        include_lowest=True
    )
    
    # Convert durations to minutes for easier visualization
    df['watch_minutes'] = df['user_watch_duration_seconds'] / 60
    
    return df

# Load the data
df = load_data()

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
            min_date = df['created_date'].min().date()
            max_date = df['created_date'].max().date()
            with date_col1:
                start_date = st.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")
            with date_col2:
                end_date = st.date_input("End date", value=max_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")
        
        with col2:
            st.subheader("Timeframe")
            timeframe = st.selectbox("Timeframe", options=["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"], index=2, label_visibility="collapsed")
        
        # Second row - All dropdowns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("State")
            states = ["All States"] + sorted(df['state'].unique().tolist())
            state = st.selectbox("State", options=states, label_visibility="collapsed")
        
        with col2:
            st.subheader("Timezone")
            timezones = ["All Timezones"] + sorted(df['timezone'].unique().tolist())
            timezone = st.selectbox("Timezone", options=timezones, label_visibility="collapsed")
        
        with col3:
            st.subheader("Percentage Watched")
            percentages = ["All Percentages"] + sorted(df['percentage_category'].unique().tolist())
            percentage = st.selectbox("Percentage watched", options=percentages, label_visibility="collapsed")
        
        with col4:
            st.subheader("Genre")
            genres = ["All Genres"] + sorted(df['show_genre'].unique().tolist())
            genre = st.selectbox("Genre", options=genres, label_visibility="collapsed")
        
        # Third row - Rating and Apply button
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Rating")
            ratings = ["All Ratings"] + sorted(df['show_rating'].unique().tolist())
            rating = st.selectbox("Rating", options=ratings, label_visibility="collapsed")
        
        with col2:
            st.write("")
            st.write("")
            apply_btn = st.button("Apply Filters", type="primary", use_container_width=False)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Apply filters when button is clicked
if 'filtered' not in st.session_state:
    st.session_state.filtered = False
    st.session_state.filtered_data = df

if apply_btn:
    st.session_state.filtered = True
    
    # Create a copy of the original dataframe
    filtered_data = df.copy()
    
    # Apply date filter
    filtered_data = filtered_data[(filtered_data['created_date'].dt.date >= start_date) & 
                                 (filtered_data['created_date'].dt.date <= end_date)]
    
    # Apply state filter
    if state != "All States":
        filtered_data = filtered_data[filtered_data['state'] == state]
    
    # Apply timezone filter
    if timezone != "All Timezones":
        filtered_data = filtered_data[filtered_data['timezone'] == timezone]
    
    # Apply percentage watched filter
    if percentage != "All Percentages":
        filtered_data = filtered_data[filtered_data['percentage_category'] == percentage]
    
    # Apply genre filter
    if genre != "All Genres":
        filtered_data = filtered_data[filtered_data['show_genre'] == genre]
    
    # Apply rating filter
    if rating != "All Ratings":
        filtered_data = filtered_data[filtered_data['show_rating'] == rating]
    
    # Store the filtered data in session state
    st.session_state.filtered_data = filtered_data

# Function to create time period based on selected timeframe
def create_time_df(data, value_column, groupby_column=None):
    # Resample data based on the selected timeframe
    if groupby_column:
        # First group by the categorical column and time
        if timeframe == "Daily":
            # For daily data, we need to group by date and category
            result = data.groupby([pd.Grouper(key='created_date', freq='D'), groupby_column])[value_column].sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-%m-%d')
        elif timeframe == "Weekly":
            result = data.groupby([pd.Grouper(key='created_date', freq='W'), groupby_column])[value_column].sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-%U')
        elif timeframe == "Monthly":
            result = data.groupby([pd.Grouper(key='created_date', freq='ME'), groupby_column])[value_column].sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-%m')
        elif timeframe == "Quarterly":
            result = data.groupby([pd.Grouper(key='created_date', freq='Q'), groupby_column])[value_column].sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-Q%q')
        else:  # Yearly
            result = data.groupby([pd.Grouper(key='created_date', freq='Y'), groupby_column])[value_column].sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y')
    else:
        # Simple time-based aggregation
        if timeframe == "Daily":
            result = data.set_index('created_date')[value_column].resample('D').sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-%m-%d')
        elif timeframe == "Weekly":
            result = data.set_index('created_date')[value_column].resample('W').sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-%U')
        elif timeframe == "Monthly":
            result = data.set_index('created_date')[value_column].resample('ME').sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-%m')
        elif timeframe == "Quarterly":
            result = data.set_index('created_date')[value_column].resample('Q').sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-Q%q')
        else:  # Yearly
            result = data.set_index('created_date')[value_column].resample('Y').sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y')
            
    return result

# Define common plot styling for consistent look
def apply_light_theme_to_fig(fig):
    """Apply consistent light theme styling to Plotly figures"""
    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font_color="#262730",
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(
            bgcolor="#FFFFFF",
            bordercolor="#E5E5E5",
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor="#F0F0F0",
            zerolinecolor="#E5E5E5",
        ),
        yaxis=dict(
            gridcolor="#F0F0F0",
            zerolinecolor="#E5E5E5",
        ),
    )
    return fig

# Show visualization if filters are applied
if st.session_state.filtered:
    # Get the filtered data
    filtered_data = st.session_state.filtered_data
    
    # Display number of records after filtering
    st.write(f"Showing {len(filtered_data)} records after filtering")
    
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
            st.subheader("Total Watch Duration Over Time")
            
            time_df = create_time_df(filtered_data, 'watch_minutes')
            
            # Create and display the line chart
            if not time_df.empty:
                fig = px.line(
                    time_df, 
                    x="period", 
                    y="watch_minutes",
                    markers=True,
                    line_shape="linear",
                    color_discrete_sequence=["#20c997"],
                    labels={"watch_minutes": "Total Watch Duration (minutes)", "period": "Period"}
                )
                
                # Apply light theme styling
                apply_light_theme_to_fig(fig)
                
                # Use custom div for styling
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No data available for the selected filters.")
        
        # Tab 2 - Watch Duration by Timezone over time
        with tab2:
            st.subheader("Watch Duration by Timezone Over Time")
            
            timezone_df = create_time_df(filtered_data, 'watch_minutes', 'timezone')
            
            if not timezone_df.empty:
                # Create line chart with multiple lines for each timezone
                fig = px.line(
                    timezone_df, 
                    x="period", 
                    y="watch_minutes",
                    color="timezone",
                    markers=True,
                    line_shape="linear",
                    labels={"watch_minutes": "Watch Duration (minutes)", 
                            "period": "Period", 
                            "timezone": "Timezone"}
                )
                
                # Apply light theme styling
                apply_light_theme_to_fig(fig)
                fig.update_layout(legend_title="Timezone")
                
                # Use custom div for styling
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No data available for the selected filters.")
        
        # Tab 3 - Watch Duration by Type over time
        with tab3:
            st.subheader("Watch Duration by Show Type Over Time")
            
            type_df = create_time_df(filtered_data, 'watch_minutes', 'show_type')
            
            if not type_df.empty:
                # Create line chart with multiple lines for each show type
                fig = px.line(
                    type_df, 
                    x="period", 
                    y="watch_minutes",
                    color="show_type",
                    markers=True,
                    line_shape="linear",
                    labels={"watch_minutes": "Watch Duration (minutes)", 
                            "period": "Period", 
                            "show_type": "Show Type"}
                )
                
                # Apply light theme styling
                apply_light_theme_to_fig(fig)
                fig.update_layout(legend_title="Show Type")
                
                # Use custom div for styling
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add a stacked area chart for better visualization of proportions
                st.subheader("Stacked Area Chart by Show Type")
                fig2 = px.area(
                    type_df,
                    x="period",
                    y="watch_minutes",
                    color="show_type",
                    labels={"watch_minutes": "Watch Duration (minutes)", 
                            "period": "Period", 
                            "show_type": "Show Type"}
                )
                
                # Apply light theme styling
                apply_light_theme_to_fig(fig2)
                fig2.update_layout(legend_title="Show Type")
                
                # Use custom div for styling
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                st.plotly_chart(fig2, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No data available for the selected filters.")
        
        # Tab 4 - Watch Duration by Show over time
        with tab4:
            st.subheader("Watch Duration by Show Over Time")
            
            # Get top 5 shows by total watch time for better visualization
            top_shows = filtered_data.groupby('show_name')['watch_minutes'].sum().nlargest(5).index.tolist()
            top_shows_data = filtered_data[filtered_data['show_name'].isin(top_shows)]
            
            show_df = create_time_df(top_shows_data, 'watch_minutes', 'show_name')
            
            if not show_df.empty:
                # Create line chart with multiple lines for each show
                fig = px.line(
                    show_df, 
                    x="period", 
                    y="watch_minutes",
                    color="show_name",
                    markers=True,
                    line_shape="linear",
                    labels={"watch_minutes": "Watch Duration (minutes)", 
                            "period": "Period", 
                            "show_name": "Show Name"}
                )
                
                # Apply light theme styling
                apply_light_theme_to_fig(fig)
                fig.update_layout(legend_title="Show Name")
                
                # Use custom div for styling
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add a stacked area chart for the top shows
                st.subheader("Stacked Area Chart by Top Shows")
                fig2 = px.area(
                    show_df,
                    x="period",
                    y="watch_minutes",
                    color="show_name",
                    labels={"watch_minutes": "Watch Duration (minutes)", 
                            "period": "Period", 
                            "show_name": "Show Name"}
                )
                
                # Apply light theme styling
                apply_light_theme_to_fig(fig2)
                fig2.update_layout(legend_title="Show Name")
                
                # Use custom div for styling
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                st.plotly_chart(fig2, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No data available for the selected filters.")

