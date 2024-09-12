import pandas as pd
import streamlit as st
import plotly.express as px
import time
import asyncio
# Load data
@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Convert to datetime
    return data

# Function to save current data to CSV
def save_current_data(df, start_idx):
    new_file_name = f"gyro_data_Streamlit.csv"
    df.to_csv(new_file_name, index=False)
    st.write(f"Data saved to {new_file_name}")

# Function to display the dashboard
def display_dashboard():
    # Initialize session state attributes if they are not already present
    if 'start_idx' not in st.session_state:
        st.session_state.start_idx = 0
    if 'reset_timer' not in st.session_state:
        st.session_state.reset_timer = False

    # Load the data
    df = load_data("gyro_data.csv")

    # Sidebar options
    st.sidebar.header('Options')
    graph_type = st.sidebar.selectbox('Select Graph Type', ['Scatter Plot', 'Line Chart', 'Distribution Plot', 'Area Plot'])
    variables = st.sidebar.multiselect('Select Variables', ['Gyro_X', 'Gyro_Y', 'Gyro_Z'], default=['Gyro_X', 'Gyro_Y', 'Gyro_Z'])

    # Number of data samples to display
    num_samples = st.sidebar.number_input('Number of Samples', min_value=1, max_value=len(df), value=100)
    
    # Determine the range of samples to display
    end_idx = st.session_state.start_idx + num_samples
    global data_to_plot
    data_to_plot = df.iloc[st.session_state.start_idx:end_idx]
    
    # Display plot
    st.subheader('Interactive Visualization')
    if graph_type == 'Scatter Plot':
        if len(variables) == 2:
            fig = px.scatter(data_to_plot, x=variables[0], y=variables[1], title=f'Scatter Plot: {variables[0]} vs {variables[1]}')
            st.plotly_chart(fig)
        else:
            st.warning("Please select exactly 2 variables for Scatter Plot.")
    elif graph_type == 'Line Chart':
        if len(variables) > 0:
            fig = px.line(data_to_plot, x='Timestamp', y=variables, title='Line Chart')
            st.plotly_chart(fig)
        else:
            st.warning("Please select at least 1 variable for Line Chart.")
    elif graph_type == 'Distribution Plot':
        if len(variables) > 0:
            fig = px.histogram(data_to_plot, x=variables, nbins=40, title=f'Distribution Plot')
            st.plotly_chart(fig)
        else:
            st.warning("Please select at least 1 variable for Distribution Plot.")
    elif graph_type == 'Area Plot':
        if len(variables) > 0:
            fig = px.area(data_to_plot, x='Timestamp', y=variables, title='Area Plot')
            st.plotly_chart(fig)
        else:
            st.warning("Please select at least 1 variable for Area Plot.")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Previous'):
            st.session_state.start_idx = max(0, st.session_state.start_idx - num_samples)  # Decrement start index
            st.session_state.reset_timer = True
    with col2:
        if st.button('Next'):
            st.session_state.start_idx = min(len(df) - num_samples, st.session_state.start_idx + num_samples)  # Increment start index
            st.session_state.reset_timer = True

    # Display summary table
    st.subheader('Data Summary')
    if len(variables) > 0:
        summary_df = data_to_plot[variables].describe()  # Filter only selected variables
        st.write(summary_df)
    else:
        st.warning("Please select at least 1 variable to display the summary.")

# Run the dashboard
display_dashboard()

# Load the CSV file when the count down threshold reaches
async def countdown_timer(seconds):
    countdown_placeholder = st.empty()
    for i in range(seconds, 0, -1):
        countdown_placeholder.text(f"Time remaining: {i} seconds")
        await asyncio.sleep(1)
asyncio.run(countdown_timer(10))       
data_to_plot.to_csv('streamlit_data_file.csv')
