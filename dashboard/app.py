# Import Required Libraies
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import duckdb
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Tabs([  # Create tabs for the dashboard
        dcc.Tab(
            label="Sensor Locations",  # First tab showing sensor locations on a map
            children=[dcc.Graph(id="map-view")]  # Map to display sensor locations
        ),
        dcc.Tab(
            label="Parameter Plots",  # Second tab for plotting air quality parameters
            children=[
                dcc.Dropdown(
                    id="location-dropdown",  # Dropdown to select a location
                    clearable=False,
                    multi=False,
                    searchable=True
                ),
                dcc.Dropdown(
                    id="parameter-dropdown",  # Dropdown to select a parameter (pm10, pm25, so2)
                    clearable=False,
                    multi=False,
                    searchable=True
                ),
                dcc.DatePickerRange(
                    id="date-picker-range",  # Date picker for filtering by date range
                    display_format="YYYY-MM-DD"
                ),
                dcc.Graph(id="line-plot"),  # Line plot for parameter trends over time
                dcc.Graph(id="box-plot")    # Box plot for distribution of parameter values by weekday
            ]
        )
    ])
])

# Callback to update the map view with the sensor locations
@app.callback(
    Output("map-view", "figure"),
    Input("map-view", "id")  # Triggered when the map view component is loaded
)
def update_map(_):
    with duckdb.connect("../air_quality.db", read_only=True) as db_connection:
        latest_values_df = db_connection.execute(
            "SELECT * FROM presentation.latest_param_values_per_location"
        ).fetchdf()  # Fetch the latest air quality data for map view

    # Fill NaN values with 0 for plotting
    latest_values_df.fillna(0, inplace=True)
    
    # Create a scatter mapbox plot for sensor locations
    map_fig = px.scatter_mapbox(
        latest_values_df,
        lat="lat",
        lon="lon",
        hover_name="location",
        hover_data={
            "lat": False,
            "lon": False,
            "datetime": True,
            "pm10": True,
            "pm25": True,
            "so2": True
        },
        zoom=6.0
    )

    # Update the layout of the map
    map_fig.update_layout(
        mapbox_style="open-street-map",
        height=800,
        title="Air Quality Monitoring Locations"
    )

    return map_fig  # Return the map figure to be displayed

# Callback to update dropdown options and date range based on data
@app.callback(
    [
        Output("location-dropdown", "options"),
        Output("location-dropdown", "value"),
        Output("parameter-dropdown", "options"),
        Output("parameter-dropdown", "value"),
        Output("date-picker-range", "start_date"),
        Output("date-picker-range", "end_date"),
    ],
    Input("location-dropdown", "id")  # Triggered when the location dropdown is loaded
)
def update_dropdowns(_):
    with duckdb.connect("../air_quality.db", read_only=True) as db_connection:
        df = db_connection.execute(
            "SELECT * FROM presentation.daily_air_quality_stats"
        ).fetchdf()  # Fetch daily air quality stats to populate the dropdowns

    # Prepare location dropdown options
    location_options = [
        {"label": location, "value": location} for location in df["location"].unique()
    ]
    # Prepare parameter dropdown options
    parameter_options = [
        {"label": parameter, "value": parameter}
        for parameter in df["parameter"].unique()
    ]
    # Set the start and end date based on available data
    start_date = df["measurement_date"].min()
    end_date = df["measurement_date"].max()

    return (
        location_options,  # Set location options
        df["location"].unique()[0],  # Default location selection
        parameter_options,  # Set parameter options
        df["parameter"].unique()[0],  # Default parameter selection
        start_date,  # Start date for the date picker
        end_date,  # End date for the date picker
    )

# Callback to update the plots (line plot and box plot)
@app.callback(
    [Output("line-plot", "figure"), Output("box-plot", "figure")],
    [
        Input("location-dropdown", "value"),
        Input("parameter-dropdown", "value"),
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date")
    ]  # Triggered when user selects location, parameter, or date range
)
def update_plots(selected_location, selected_parameter, start_date, end_date):
    with duckdb.connect("../air_quality.db", read_only=True) as db_connection:
        daily_stats_df = db_connection.execute(
            "SELECT * FROM presentation.daily_air_quality_stats"
        ).fetchdf()  # Fetch daily air quality stats for the selected parameter and location

    # Filter the data based on the selected location, parameter, and date range
    filtered_df = daily_stats_df[daily_stats_df["location"] == selected_location]
    filtered_df = filtered_df[filtered_df["parameter"] == selected_parameter]
    filtered_df = filtered_df[
        (filtered_df["measurement_date"] >= pd.to_datetime(start_date))
        & (filtered_df["measurement_date"] <= pd.to_datetime(end_date))
    ]

    # Label for the plot
    labels = {
        "average_value": filtered_df["units"].unique()[0],
        "measurement_date": "Date"
    }

    # Create a line plot for parameter values over time
    line_fig = px.line(
        filtered_df.sort_values(by="measurement_date"),
        x="measurement_date",
        y="average_value",
        labels=labels,
        title=f"Plot Over Time of {selected_parameter} Levels"
    )

    # Create a box plot for distribution of parameter values by weekday
    box_fig = px.box(
        filtered_df.sort_values(by="weekday_number"),
        x="weekday",
        y="average_value",
        labels=labels,
        title=f"Distribution of {selected_parameter} Levels by Weekday"
    )

    return line_fig, box_fig  # Return the generated plots

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
