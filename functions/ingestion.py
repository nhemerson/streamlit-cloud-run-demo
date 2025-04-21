
import json
import pandas as pd
import streamlit as st

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

