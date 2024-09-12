# Import necessary packages
import pandas as pd
import numpy as np
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Div, TextInput, Button, DataTable, TableColumn
from bokeh.plotting import figure, curdoc
from bokeh.io import output_notebook
from bokeh.palettes import Category10
from bokeh.models.widgets import Paragraph
from tornado import gen

############################################################ CONFIGURE ######################################################################
# Initial setup
output_notebook()

# Load initial data
def load_data(file):
    data = pd.read_csv(file)
    return dict(Timestamp=pd.to_datetime(data["Timestamp"]),  # Convert to datetime for line chart
                Gyro_X=data["Gyro_X"], 
                Gyro_Y=data["Gyro_Y"], 
                Gyro_Z=data["Gyro_Z"])

# Load data
data = load_data("gyro_data.csv")
source = ColumnDataSource(data=data)

# Initialize figure with datetime x-axis (for line graph)
plot = figure(title="Gyroscope Data Visualization", x_axis_type='datetime')

# Dropdown for graph types (default is Line Chart)
select_graph_type = Select(title="Graph Type", options=["Scatter Plot", "Line Chart",
                            "Distribution Plot", "Area Plot"], value="Line Chart")

select_x = Select(title="X-Axis", options=["Gyro_X", "Gyro_Y", "Gyro_Z"], value="Gyro_X")

# Single selection for Y-axis (Gyroscope variables)
select_y = Select(title="Y-Axis", options=["Gyro_X", "Gyro_Y", "Gyro_Z", "All Variables"], value="Gyro_X")

data_summary = Div(text="Data Summary: ...")

# Number of samples input
num_samples_input = TextInput(title="Number of Samples", value="100", width=100)
current_start_index = 0

# Buttons for navigation
previous_button = Button(label="Previous", button_type="warning")
next_button = Button(label="Next", button_type="success")

# Countdown timer
countdown_display = Paragraph(text="Countdown: 10 seconds")
countdown = 11

colors = Category10[3]

################################################################## UPDATE STEP #############################################################################
def update_graph(attr, old, new):
    global current_start_index, countdown
    countdown = 10  # Reset the countdown when the graph is updated

    num_samples = int(num_samples_input.value)
    if num_samples <= 0:
        num_samples = 1
    max_index = len(source.data['Timestamp']) - 1
    end_index = min(current_start_index + num_samples, max_index + 1)
    
    # Slice data for current view
    sliced_data = {key: value[current_start_index:end_index] for key, value in source.data.items()}
    sliced_source = ColumnDataSource(data=sliced_data)
    
    plot.renderers = []  # Clear existing plot

    graph_type = select_graph_type.value
    x_var = select_x.value
    y_var = select_y.value
    
    # Different types of graph
    if graph_type == "Line Chart":
        if y_var == "All Variables":
            for i, var in enumerate(["Gyro_X", "Gyro_Y", "Gyro_Z"]):
                plot.line(x='Timestamp', y=var, source=sliced_source, legend_label=var, color=colors[i])
            plot.title.text = f"Line Chart: All Variables vs Timestamp"
            plot.xaxis.axis_label = 'Timestamp'
            plot.yaxis.axis_label = 'Gyroscope Value'
        else:
            plot.line(x='Timestamp', y=y_var, source=sliced_source, legend_label=y_var)
            plot.title.text = f"Line Chart: {y_var} vs Timestamp"
            plot.xaxis.axis_label = 'Timestamp'
            plot.yaxis.axis_label = y_var
            
        select_x.visible = False

    elif graph_type == "Distribution Plot":
        if y_var == "All Variables":
            variables = ["Gyro_X", "Gyro_Y", "Gyro_Z"]
            for i, var in enumerate(variables):
                hist, edges = np.histogram(sliced_data[var], bins=50)
                plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], color=colors[i], legend_label=var)
            plot.title.text = "Distribution Plot: All Variables"
            plot.xaxis.axis_label = "Gyroscope Value"
            plot.yaxis.axis_label = 'Frequency'
        else:
            hist, edges = np.histogram(sliced_data[y_var], bins=50)
            plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], color=colors[0], legend_label=y_var)
            plot.title.text = f"Distribution Plot of {y_var}"
            plot.xaxis.axis_label = y_var
            plot.yaxis.axis_label = 'Frequency'
        select_x.visible = False
        
    elif graph_type == "Area Plot" :
        if y_var == "All Variables":
            for i, var in enumerate(["Gyro_X", "Gyro_Y", "Gyro_Z"]):
                plot.varea(x='Timestamp', y1=0, y2=var, source=sliced_source, color=colors[i], legend_label=var, alpha=0.3)
            plot.title.text = "Area Plot: All Variables"
        else:
            plot.varea(x='Timestamp', y1=0, y2=y_var, source=sliced_source, color=colors[0], legend_label=y_var, alpha=0.3)
            plot.title.text = f"Area Plot of {y_var}"
        plot.xaxis.axis_label = 'Timestamp'
        plot.yaxis.axis_label = 'Gyroscope Value'
        select_x.visible = False
    else:
        select_x.visible = True
        if graph_type == "Scatter Plot":
            plot.scatter(x=x_var, y=y_var, source=sliced_source, legend_label=y_var)
            plot.title.text = f"Scatter Plot: {x_var} vs {y_var}"
            plot.xaxis.axis_label = x_var
            plot.yaxis.axis_label = y_var

    plot.legend.title = "Gyroscope Variables"
    plot.legend.location = "top_left"

    # Update data summary table
    update_summary_table(sliced_data)

def update_summary_table(sliced_data):
    variables = ["Gyro_X", "Gyro_Y", "Gyro_Z"] if select_y.value == "All Variables" else [select_y.value]
    summary_data = {
        "Variable": [],
        "Mean": [],
        "Median": [],
        "Min": [],
        "Max": [],
        "Std Dev": []
    }

    for var in variables:
        var_data = sliced_data[var]
         # Rounding to 2 digits
        summary_data["Variable"].append(var)
        summary_data["Mean"].append(round(np.mean(var_data), 2))   
        summary_data["Median"].append(round(np.median(var_data), 2)) 
        summary_data["Min"].append(round(np.min(var_data), 2))      
        summary_data["Max"].append(round(np.max(var_data), 2))      
        summary_data["Std Dev"].append(round(np.std(var_data), 2))

    # Update the data source for the table
    summary_source.data = summary_data

# Initialize DataTable for the summary
summary_source = ColumnDataSource(data={
    "Variable": [],
    "Mean": [],
    "Median": [],
    "Min": [],
    "Max": [],
    "Std Dev": []
})

columns = [
    TableColumn(field="Variable", title="Variable"),
    TableColumn(field="Mean", title="Mean"),
    TableColumn(field="Median", title="Median"),
    TableColumn(field="Min", title="Min"),
    TableColumn(field="Max", title="Max"),
    TableColumn(field="Std Dev", title="Std Dev"),
]

data_table = DataTable(source=summary_source, columns=columns, width=600, height=200)

def on_next_click():
    global current_start_index
    num_samples = int(num_samples_input.value)
    max_index = len(source.data['Timestamp']) - 1
    current_start_index = min(current_start_index + num_samples, max_index - num_samples + 1)
    update_graph(None, None, None)

def on_previous_click():
    global current_start_index
    num_samples = int(num_samples_input.value)
    current_start_index = max(current_start_index - num_samples, 0)
    update_graph(None, None, None)

@gen.coroutine
def update_countdown():
    global countdown
    if countdown > 0:
        countdown -= 1
    countdown_display.text = f"Countdown: {countdown} seconds"
    if countdown == 0:
        # Save the currently displayed data to a CSV file
        save_current_displayed_data()
        countdown = 10  # Reset countdown after saving

def save_current_displayed_data():
    num_samples = int(num_samples_input.value)
    if num_samples <= 0:
        num_samples = 1
    max_index = len(source.data['Timestamp']) - 1
    end_index = min(current_start_index + num_samples, max_index + 1)
    
    # Slice data for current view
    sliced_data = {key: value[current_start_index:end_index] for key, value in source.data.items()}
    sliced_df = pd.DataFrame(sliced_data)
    
    # Save to CSV
    file_name = "current_displayed_data.csv"
    sliced_df.to_csv(file_name, index=False)
    print(f"Saved {len(sliced_df)} samples to {file_name}")

# Attach event listeners
select_graph_type.on_change("value", update_graph)
select_x.on_change("value", update_graph)
select_y.on_change("value", update_graph)
num_samples_input.on_change("value", update_graph)
next_button.on_click(on_next_click)
previous_button.on_click(on_previous_click)

# Add components to the layout
layout = column(
    row(select_graph_type, select_x, select_y),
    num_samples_input,
    row(previous_button, next_button),
    countdown_display,
    plot,
    data_summary,
    data_table
)

# Add the layout to the current document
curdoc().add_root(layout)

# Setup periodic callback for countdown
curdoc().add_periodic_callback(update_countdown, 1000)  
