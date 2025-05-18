import pandas as pd


# Function to create time period based on selected timeframe
def create_time_df(data, timeframe, value_column, groupby_column=None):
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
            result = data.groupby([pd.Grouper(key='created_date', freq='M'), groupby_column])[value_column].sum().reset_index()
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
            result = data.set_index('created_date')[value_column].resample('M').sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-%m')
        elif timeframe == "Quarterly":
            result = data.set_index('created_date')[value_column].resample('Q').sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y-Q%q')
        else:  # Yearly
            result = data.set_index('created_date')[value_column].resample('Y').sum().reset_index()
            result['period'] = result['created_date'].dt.strftime('%Y')
            
    return result