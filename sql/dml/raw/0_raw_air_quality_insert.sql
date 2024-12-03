-- Insert new air quality data into the 'raw.air_quality' table.
INSERT INTO raw.air_quality
SELECT 
    location_id,                               -- Unique identifier for the location.
    sensors_id,                               -- Unique identifier for the sensor.
    "location",                               -- Name of the location.
    "datetime",                               -- Timestamp of the measurement.
    lat,                                      -- Latitude coordinate of the location.
    lon,                                      -- Longitude coordinate of the location.
    "parameter",                              -- Type of measurement (e.g., PM10, PM2.5).
    units,                                    -- Units of the measurement.
    "value",                                  -- Measured value.
    "month",                                  -- Month of the measurement.
    "year",                                   -- Year of the measurement.
    current_timestamp AS ingestion_datetime   -- Timestamp when the data was ingested.
FROM read_csv('{{ data_file_path }}');        -- Load data from a CSV file specified by the 'data_file_path' variable.
