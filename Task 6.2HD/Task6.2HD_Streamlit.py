# Import necessary packages
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import asyncio

######################################################################### UTILITIES #####################################################################################

# Function to handle navigation buttons (Previous, Next, Reset)
def handle_navigation(n_rows, dataset):
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Previous'):
            st.session_state.start_idx = max(0, st.session_state.start_idx - n_rows)
    with col2:
        if st.button('Next'):
            st.session_state.start_idx = min(len(dataset) - n_rows, st.session_state.start_idx + n_rows)
    with col3:
        if st.button('Restart'):
            st.session_state.start_idx = 0
            st.session_state.end_idx = n_rows
    return st.session_state.start_idx, st.session_state.end_idx

# Countdown timer for displaying data
async def start_countdown(seconds):
    countdown_placeholder = st.empty()
    for i in range(seconds, 0, -1):
        countdown_placeholder.text(f"Time remaining: {i} seconds")
        await asyncio.sleep(1)

# Function to display data in different chart types
def display_chart(data_subset, x_axis, y_axes, chart_kind):
    if chart_kind == 'Line Graph':
        st.line_chart(data_subset, x= "Timestamp", y=y_axes)
    elif chart_kind == 'Area Chart':
        st.area_chart(data_subset, x= "Timestamp", y=y_axes)
    elif chart_kind == 'Distribution Plot':
        fig = px.histogram(data_subset, x=y_axes, nbins=40, title='Distribution Plot')
        st.plotly_chart(fig)
    elif chart_kind == 'Scatter Plot' and len(y_axes) == 1:
        st.scatter_chart(data_subset, x=x_axis, y=y_axes)
    else:
        st.warning('Scatter plot requires exactly one y-axis variable.')

# Function to display data (existing or streaming)
def display_data(dataset, placeholder, countdown, x_axis, y_axes, chart_kind, n_rows, file_path, is_streaming=False):
    st.session_state.end_idx = st.session_state.start_idx + n_rows
    st.session_state.start_idx = max(0, min(st.session_state.start_idx, len(dataset) - n_rows))
    
    while st.session_state.end_idx <= len(dataset):
        data_subset = dataset.iloc[st.session_state.start_idx:st.session_state.end_idx]
        
        with placeholder.container():
            display_chart(data_subset, x_axis, y_axes, chart_kind)
            st.subheader('Data Summary')
            status = data_subset[y_axes].describe()
            st.table(status)
        
        data_subset.to_csv(file_path)
        
        if not is_streaming:
            asyncio.run(start_countdown(countdown))
            break
        else:
            time.sleep(1)
            st.session_state.start_idx += 1
            st.session_state.end_idx += 1

######################################################################## STREAMLIT APP #################################################################################

# Main app function to load and display data
def run_app():
    # Load the CSV file
    df = pd.read_csv('gyro_data.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Streamlit sidebar options
    st.title('Gyroscope Data Visualization')
    data_type = st.sidebar.selectbox("Select Displaying Method", ['Existing Data', 'Streaming Data'])
    chart_kind = st.sidebar.selectbox('Select chart type', ['Line Graph', 'Area Chart', 'Scatter Plot', 'Distribution Plot'], index=0)

    x_axis = st.sidebar.selectbox("Select variable for x-axis", ['Gyro_X', 'Gyro_Y', 'Gyro_Z'])  # Exclude 'Timestamp'
    y_axes = st.sidebar.multiselect("Select variable(s) for y-axis", ['Gyro_X', 'Gyro_Y', 'Gyro_Z'], default=['Gyro_X', 'Gyro_Y'])

    # Input fields
    n_rows = st.sidebar.number_input("Enter number of rows", min_value=1, max_value=len(df), value=10, key='n_rows')
    countdown = st.sidebar.number_input("Enter countdown time (seconds)", min_value=1, max_value=100, value=10, key='countdown')

    # Set session states
    if 'start_idx' not in st.session_state:
        st.session_state.start_idx = 0
    if 'end_idx' not in st.session_state:
        st.session_state.end_idx = n_rows
    if 'second' not in st.session_state:
        st.session_state.second = countdown

    handle_navigation(n_rows, df)

    # Placeholder for data display
    placeholder = st.empty()

    # Display data (existing or streaming)
    file_path = 'existing_data.csv' if data_type == 'Existing Data' else 'stream_data.csv'
    display_data(df, placeholder, countdown, x_axis, y_axes, chart_kind, n_rows, file_path, is_streaming=(data_type == 'Streaming Data'))

# Run the app
if __name__ == '__main__':
    run_app()
