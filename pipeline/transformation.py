# Import required modules
import argparse  # For parsing command-line arguments
import logging  # For logging information and errors

# Importing utility functions from the database_manager module
from database_manager import (
    connect_to_database,  # Function to establish a connection to the database
    close_database_connection,  # Function to close the database connection
    execute_query,  # Function to execute a SQL query
    collect_query_paths,  # Function to collect all SQL file paths from a directory
    read_query,  # Function to read a SQL query from a file
)

# Function to perform data transformation
def transform_data(args) -> None:
    """
    Execute SQL transformation queries on the database.
    
    Args:
        args: Parsed command-line arguments containing the database path
              and the directory of SQL transformation queries.
    """
    # Get the path to the database from arguments
    database_path = args.database_path

    # Establish a connection to the database
    con = connect_to_database(path=database_path)

    # Collect paths to all SQL files in the provided query directory
    query_paths = collect_query_paths(args.query_directory)

    # Execute each SQL query in the collected file paths
    for query_path in query_paths:
        # Read the SQL query from the file
        query = read_query(query_path)
        # Execute the query using the database connection
        execute_query(con, query)

        # Log the successful execution of the query
        logging.info(f"Executed query from {query_path}")

    # Close the database connection after all queries have been executed
    close_database_connection(con)


# Main function to handle command-line argument parsing and trigger the transformation process
def main():
    """
    Main entry point for the script. Parses command-line arguments
    and triggers the data transformation process.
    """
    # Set logging level to INFO for detailed logs
    logging.getLogger().setLevel(logging.INFO)

    # Initialize argument parser for command-line interface
    parser = argparse.ArgumentParser(description="CLI for Data Transformation")

    # Add argument for specifying the path to the DuckDB database
    parser.add_argument(
        "--database_path",
        type=str,
        required=True,
        help="Path to the DuckDB database",
    )

    # Add argument for specifying the directory containing SQL transformation queries
    parser.add_argument(
        "--query_directory",
        type=str,
        required=True,
        help="Directory containing SQL transformation queries",
    )

    # Parse the arguments passed via the command line
    args = parser.parse_args()

    # Trigger the data transformation process with the parsed arguments
    transform_data(args)


# Entry point for the script execution
if __name__ == "__main__":
    main()
