-- Create a table named 'air_quality' in the 'raw' schema if it does not already exist.
-- This table stores detailed air quality data with various columns for metadata and measurements.
CREATE TABLE IF NOT EXISTS raw.air_quality (
    location_id BIGINT,                -- Unique identifier for the location
    sensors_id BIGINT,                 -- Unique identifier for the sensor
    "location" VARCHAR,                -- Name of the location
    "datetime" TIMESTAMP,              -- Timestamp when the measurement was recorded
    lat DOUBLE,                        -- Latitude coordinate of the location
    lon DOUBLE,                        -- Longitude coordinate of the location
    "parameter" VARCHAR,               -- Type of measurement (e.g., PM10, PM2.5, SO2)
    units VARCHAR,                     -- Units of the measurement
    "value" DOUBLE,                    -- Measured value
    "month" VARCHAR,                   -- Month when the measurement was recorded
    "year" BIGINT,                     -- Year when the measurement was recorded
    ingestion_datetime TIMESTAMP       -- Timestamp when the data was ingested into the database
);
