-- Create a schema named 'raw' if it does not already exist.
-- The 'raw' schema is used to store unprocessed or raw data directly loaded into the database.
CREATE SCHEMA IF NOT EXISTS 'raw';

-- Create a schema named 'presentation' if it does not already exist.
-- The 'presentation' schema is used for processed or cleaned data, often used in reporting or analysis.
CREATE SCHEMA IF NOT EXISTS 'presentation';
