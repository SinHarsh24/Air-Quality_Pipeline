# Import necessary modules
import argparse  # For command-line argument parsing
import json  # For reading and parsing JSON files
import logging  # For logging information
from datetime import datetime  # For working with date and time
from dateutil.relativedelta import relativedelta  # For adding or subtracting months
from typing import List  # For type hinting

from duckdb import IOException  # Exception handling for DuckDB
from jinja2 import Template  # For templating dynamic strings

# Import custom database manager functions
from database_manager import (
    connect_to_database,  # To connect to the database
    close_database_connection,  # To close the database connection
    execute_query,  # To execute SQL queries
    read_query  # To read SQL queries from files
)


# Function to read location IDs from a JSON file
def read_location_ids(file_path: str) -> List[str]:
    """
    Read location IDs from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing location data.
    
    Returns:
        List[str]: A list of location IDs as strings.
    """
    with open(file_path, "r") as f:
        locations = json.load(f)  # Load JSON data into a dictionary
        f.close()

    # Convert keys (location IDs) to strings and return as a list
    location_ids = [str(id) for id in locations.keys()]
    return location_ids


# Function to compile data file paths for each location and date range
def compile_data_file_paths(
    data_file_path_template: str, location_ids: List[str], start_date: str, end_date: str
) -> List[str]:
    """
    Generate a list of data file paths using location IDs and date range.
    
    Args:
        data_file_path_template (str): Template for constructing file paths.
        location_ids (List[str]): List of location IDs.
        start_date (str): Start date in "YYYY-MM" format.
        end_date (str): End date in "YYYY-MM" format.
    
    Returns:
        List[str]: A list of file paths for each location and date.
    """
    # Parse start and end dates as datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m")
    end_date = datetime.strptime(end_date, "%Y-%m")

    data_file_paths = []  # Initialize an empty list for file paths

    # Generate paths for each location ID and date in the range
    for location_id in location_ids:
        index_date = start_date
        while index_date <= end_date:  # Iterate through months in the date range
            data_file_path = Template(data_file_path_template).render(
                location_id=location_id,
                year=str(index_date.year),
                month=str(index_date.month).zfill(2)  # Ensure month is two digits
            )
            data_file_paths.append(data_file_path)  # Add the generated path to the list
            index_date += relativedelta(months=1)  # Increment date by one month

    return data_file_paths


# Function to compile an SQL query for extracting data
def compile_data_file_query(
    base_path: str, data_file_path: str, extract_query_template: str
) -> str:
    """
    Generate an SQL query to extract data from a file.
    
    Args:
        base_path (str): Base path for data files.
        data_file_path (str): Path to the specific data file.
        extract_query_template (str): Template for the SQL query.
    
    Returns:
        str: The rendered SQL query.
    """
    # Render the SQL query template with the provided file path
    extract_query = Template(extract_query_template).render(
        data_file_path=f"{base_path}/{data_file_path}"
    )
    return extract_query


# Main function for extracting data
def extract_data(args):
    """
    Extract data for specified locations and date range using provided templates.
    
    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    """
    # Read location IDs from the specified JSON file
    location_ids = read_location_ids(args.locations_file_path)

    # Template for constructing file paths
    data_file_path_template = "locationid={{location_id}}/year={{year}}/month={{month}}/*"

    # Generate file paths for the given date range and locations
    data_file_paths = compile_data_file_paths(
        data_file_path_template=data_file_path_template,
        location_ids=location_ids,
        start_date=args.start_date,
        end_date=args.end_date
    )

    # Read the SQL query template for data extraction
    extract_query_template = read_query(path=args.extract_query_template_path)

    # Connect to the DuckDB database
    con = connect_to_database(path=args.database_path)

    # Process each data file path
    for data_file_path in data_file_paths:
        logging.info(f"Extracting data from {data_file_path}")  # Log the extraction attempt

        # Compile the SQL query for the current file path
        query = compile_data_file_query(
            base_path=args.source_base_path,
            data_file_path=data_file_path,
            extract_query_template=extract_query_template
        )

        # Execute the query and handle potential exceptions
        try:
            execute_query(con, query)
            logging.info(f"Extracted data from {data_file_path}!")  # Log success
        except IOException as e:
            logging.warning(f"Could not find data from {data_file_path}: {e}")  # Log failure
    
    # Close the database connection after processing
    close_database_connection(con)


# Main function to set up argument parsing and invoke the extraction process
def main():
    """
    Main entry point for the CLI tool. Parses arguments and triggers the extraction process.
    """
    logging.getLogger().setLevel(logging.INFO)  # Set logging level to INFO

    # Set up argument parser
    parser = argparse.ArgumentParser(description="CLI for ELT Extraction")
    
    # Define required arguments
    parser.add_argument(
        "--locations_file_path",
        type=str,
        required=True,
        help="Path to the locations JSON file",
    )
    parser.add_argument(
        "--start_date", type=str, required=True, help="Start date in YYYY-MM format"
    )
    parser.add_argument(
        "--end_date", type=str, required=True, help="End date in YYYY-MM format"
    )
    parser.add_argument(
        "--extract_query_template_path",
        type=str,
        required=True,
        help="Path to the SQL extraction query template",
    )
    parser.add_argument(
        "--database_path", type=str, required=True, help="Path to the database"
    )
    parser.add_argument(
        "--source_base_path",
        type=str,
        required=True,
        help="Base path for the remote data files",
    )

    # Parse arguments
    args = parser.parse_args()
    # Trigger the data extraction process
    extract_data(args)


# Entry point for the script
if __name__ == "__main__":
    main()
