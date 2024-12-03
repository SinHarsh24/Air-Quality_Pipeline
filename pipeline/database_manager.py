# Import necessary modules
from typing import List  # For type hinting
import os  # For file and directory operations
import argparse  # For command-line argument parsing
import logging  # For logging information

from duckdb import DuckDBPyConnection  # Type for DuckDB connection
import duckdb as ddb  # DuckDB library

# Function to connect to the DuckDB database
def connect_to_database(path: str) -> DuckDBPyConnection:
    """
    Connect to the DuckDB database at the given path.
    
    Args:
        path (str): Path to the DuckDB database file.
    
    Returns:
        DuckDBPyConnection: A connection object to interact with the database.
    """
    logging.info(f"Connecting to database at {path}")  # Log the connection attempt
    con = ddb.connect(path)  # Establish the connection
    con.sql("""
        SET s3_access_key_id='';   -- Set S3 credentials (currently empty for security reasons)
        SET s3_secret_access_key='';
        SET s3_region='';
        """)  # Configure S3 settings for DuckDB (optional)
    return con

# Function to close the DuckDB database connection
def close_database_connection(con: DuckDBPyConnection) -> None:
    """
    Close the database connection.
    
    Args:
        con (DuckDBPyConnection): Connection object to close.
    """
    logging.info(f"Closing database connection")  # Log the closure
    con.close()  # Close the connection

# Function to collect paths of SQL scripts from a directory
def collect_query_paths(parent_dir: str) -> List[str]:
    """
    Collect paths of all SQL files within a directory (recursively).
    
    Args:
        parent_dir (str): Path to the parent directory to search for SQL files.
    
    Returns:
        List[str]: A sorted list of file paths to SQL files.
    """
    sql_files = []  # List to store SQL file paths

    # Traverse the directory and find files ending with '.sql'
    for root, _, files in os.walk(parent_dir):
        for file in files:
            if file.endswith(".sql"):  # Check for SQL files
                file_path = os.path.join(root, file)  # Get the full path
                sql_files.append(file_path)
    
    logging.info(f"Found {len(sql_files)} SQL scripts at location {parent_dir}")  # Log the number of scripts found
    return sorted(sql_files)  # Return the sorted list of SQL file paths

# Function to read a query from a file
def read_query(path: str) -> str:
    """
    Read the contents of an SQL file.
    
    Args:
        path (str): Path to the SQL file.
    
    Returns:
        str: The SQL query as a string.
    """
    with open(path, "r") as f:
        query = f.read()  # Read the file content
        f.close()  # Close the file
    return query

# Function to execute a query on the database
def execute_query(con: DuckDBPyConnection, query: str) -> None:
    """
    Execute an SQL query on the connected DuckDB database.
    
    Args:
        con (DuckDBPyConnection): The database connection object.
        query (str): The SQL query to execute.
    """
    con.execute(query)  # Execute the query

# Function to set up the database with DDL scripts
def setup_database(database_path: str, ddl_query_parent_dir: str) -> None:
    """
    Set up the DuckDB database using DDL queries from a specified directory.
    
    Args:
        database_path (str): Path to the DuckDB database file.
        ddl_query_parent_dir (str): Path to the directory containing DDL SQL scripts.
    """
    query_paths = collect_query_paths(ddl_query_parent_dir)  # Get paths to all DDL scripts
    con = connect_to_database(database_path)  # Connect to the database

    # Execute each query in the collected DDL scripts
    for query_path in query_paths:
        query = read_query(query_path)  # Read the query from the file
        execute_query(con, query)  # Execute the query
        logging.info(f"Executed query from {query_path}")  # Log the execution

    close_database_connection(con)  # Close the connection after execution

# Function to destroy (delete) the database file
def destroy_database(database_path: str) -> None:
    """
    Delete the DuckDB database file if it exists.
    
    Args:
        database_path (str): Path to the DuckDB database file.
    """
    if os.path.exists(database_path):  # Check if the file exists
        os.remove(database_path)  # Delete the file
        logging.info(f"Database at {database_path} has been destroyed.")  # Log the deletion

# Main function to parse CLI arguments and perform database setup or destruction
def main():
    """
    Main function to provide a CLI interface for setting up or destroying the database.
    """
    logging.getLogger().setLevel(logging.INFO)  # Set logging level to INFO
    
    # Define command-line arguments
    parser = argparse.ArgumentParser(description="CLI tool to setup or destroy a database.")

    # Mutually exclusive group to ensure either create or destroy is selected
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--create", action="store_true", help="Create the database")  # Option to create the database
    group.add_argument("--destroy", action="store_true", help="Destroy the database")  # Option to destroy the database

    # Additional arguments for database path and DDL script directory
    parser.add_argument("--database-path", type=str, help="Path to the database")
    parser.add_argument("--ddl-query-parent-dir", type=str, help="Path to the parent directory of the DDL queries")

    # Parse the arguments
    args = parser.parse_args()

    # Perform the appropriate action based on the arguments
    if args.create:
        setup_database(database_path=args.database_path, ddl_query_parent_dir=args.ddl_query_parent_dir)
    elif args.destroy:
        destroy_database(database_path=args.database_path)

# Entry point for the script
if __name__ == "__main__":
    main()
