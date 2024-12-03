# Air Quality Dashboard

A dashboard for visualizing air quality monitoring data using Plotly, Dash, and DuckDB.

## Description

This project provides an interactive dashboard to visualize air quality parameters such as PM10, PM2.5, and SO2 across different sensor locations. The dashboard is built using Plotly for visualizations and Dash for the web interface. The backend is powered by DuckDB for data storage and querying.

## Features
- **Sensor Location Map**: Visualize the latest air quality values for each monitoring location on an interactive map.
- **Parameter Selection**: Choose from various air quality parameters (PM10, PM2.5, SO2) to view the data.
- **Date Range Filtering**: Select a custom date range for the plots.
- **Time Series Plot**: View air quality parameter trends over time.
- **Distribution Plot**: See the distribution of air quality levels for a specific parameter by weekday.

## Requirements
- **Python** 3.x
- **Dash**: For creating the interactive web app.
- **Plotly**: For creating interactive visualizations (line plot, box plot, scatter map).
- **DuckDB**: For querying air quality data stored in a local DuckDB database.
- **Pandas**: For data manipulation and handling.
---

## Tech and End Goal

1. **Tools and Technologies**: 
   - **Python**: For scripting (CLI apps), orchestration, and dashboard creation using Plotly Dash.
   - **DuckDB**: Lightweight, in-process database engine serving as the data warehouse.

2. **End Result**:
   - A functional data pipeline that extracts, transforms, and visualizes air quality data dynamically.

---

## Project Structure

- **`notebooks/`**: Scratchpads for experimenting with ideas and testing technologies.
- **`sql/`**: SQL scripts for data extraction and transformation, written in DuckDB’s query language.
- **`pipeline/`**: CLI applications for executing extraction, transformation, and database management tasks.
- **`dashboard/`**: Plotly Dash code for creating the live air quality dashboard.
- **`locations.json`**: Configuration file containing air quality sensor locations.
- **`secrets-example.json`**: Example configuration for OpenAQ API keys (**Note:** Do not commit actual secrets to version control).
- **`requirements.txt`**: List of Python libraries and dependencies.

---

## Database Structure

The DuckDB database includes the following schemas and tables:

1. **`raw` schema**:
   - Contains a single table with all extracted data.

2. **`presentation` schema**:
   - **`air_quality`**: The most recent version of each record per location.
   - **`daily_air_quality_stats`**: Daily averages for parameters at each location.
   - **`latest_param_values_per_location`**: Latest values for each parameter at each location.

---

## Running the Project

Follow these steps to set up and run the project:

1. **Set Up Python Environment**:
   - Create a virtual environment:
     ```bash
     $ python -m venv .venv
     ```
   - Activate the environment:
     - **Windows**: `$ . .venv/Scripts/activate`
     - **Linux/Mac**: `$ . .venv/bin/activate`
   - Install dependencies:
     ```bash
     $ pip install -r requirements.txt
     ```

2. **Initialize the Database**:
   - Navigate to the `pipeline` directory:
     ```bash
     $ cd pipeline
     ```
   - Run the database manager CLI to create the database:
     ```bash
     $ python database_manager.py --create
     ```

3. **Extract Data**:
   - Run the extraction CLI:
     ```bash
     $ python extraction.py [required arguments]
     ```

4. **Transform Data**:
   - Run the transformation CLI to create views in the presentation schema:
     ```bash
     $ python transformation.py
     ```

5. **Set Up the Dashboard**:
   - Navigate to the `dashboard` directory:
     ```bash
     $ cd dashboard
     ```
   - Start the dashboard application:
     ```bash
     $ python app.py
     ```

6. **Access the Results**:
   - The database will be stored as a `.db` file.
   - The dashboard will be accessible in your web browser.

---


