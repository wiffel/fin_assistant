
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('/Users/wif/projects/fin_assistant/fetched_data/nvda_monthly_20240821.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

# Set up the Streamlit page
st.title('NVIDIA (NVDA) Stock Price - Last 5 Years')

# Calculate the date 5 years ago from the most recent date in the dataset
latest_date = df['timestamp'].max()
five_years_ago = latest_date - timedelta(days=5*365)

# Filter the dataframe for the last 5 years
df_filtered = df[df['timestamp'] >= five_years_ago]

# Create a range slider for date selection
date_range = st.slider(
    "Select Date Range",
    min_value=five_years_ago.date(),
    max_value=latest_date.date(),
    value=(five_years_ago.date(), latest_date.date())
)

# Filter the dataframe based on the selected date range
mask = (df_filtered['timestamp'].dt.date >= date_range[0]) & (df_filtered['timestamp'].dt.date <= date_range[1])
df_selected = df_filtered.loc[mask]

# Create the candlestick chart
fig = go.Figure(data=[go.Candlestick(
    x=df_selected['timestamp'],
    open=df_selected['open'],
    high=df_selected['high'],
    low=df_selected['low'],
    close=df_selected['close']
)])

# Update the layout
fig.update_layout(
    title='NVIDIA (NVDA) Stock Price',
    yaxis_title='Price (USD)',
    xaxis_title='Date',
    xaxis_rangeslider_visible=False,
    height=600,
    template='plotly_dark'
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Display additional information
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Latest Close", f"${df_selected['close'].iloc[-1]:.2f}")
with col2:
    st.metric("Highest Price", f"${df_selected['high'].max():.2f}")
with col3:
    st.metric("Lowest Price", f"${df_selected['low'].min():.2f}")

# Add a volume chart
volume_chart = go.Figure(data=[go.Bar(x=df_selected['timestamp'], y=df_selected['volume'])])
volume_chart.update_layout(
    title='Trading Volume',
    yaxis_title='Volume',
    xaxis_title='Date',
    height=400,
    template='plotly_dark'
)
st.plotly_chart(volume_chart, use_container_width=True)

# Add some explanatory text
st.write("""
This visualization shows the stock price movement of NVIDIA (NVDA) over the last 5 years. 
The main chart is a candlestick chart, where each candlestick represents one month of trading:
- The body of the candlestick shows the opening and closing prices.
- The wick (thin line) shows the highest and lowest prices reached during the month.
- Green candlesticks indicate the closing price was higher than the opening price (price increased).
- Red candlesticks indicate the closing price was lower than the opening price (price decreased).

You can use the date range slider to zoom in on specific periods. The volume chart below shows the trading volume for each month.
""")
