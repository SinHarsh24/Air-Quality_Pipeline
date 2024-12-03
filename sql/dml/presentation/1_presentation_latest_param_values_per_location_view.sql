-- Create or replace a view named 'latest_param_values_per_location' in the 'presentation' schema.
-- This view provides the most recent parameter values for each location.

CREATE OR REPLACE VIEW presentation.latest_param_values_per_location AS
-- Use a Common Table Expression (CTE) to assign row numbers based on the latest datetime for each parameter at each location.
WITH ranked_data AS (
  SELECT
    location_id,             -- Unique identifier for the location
    location,                -- Name of the location
    lat,                     -- Latitude of the location
    lon,                     -- Longitude of the location
    parameter,               -- Type of measurement
    value,                   -- Measured value
    datetime,                -- Timestamp of the measurement
    ROW_NUMBER() OVER (
        PARTITION BY location_id, parameter  -- Partition by location and parameter
        ORDER BY datetime DESC               -- Order by the most recent datetime
    ) AS rn -- Assign row numbers to prioritize the latest records.
  FROM presentation.air_quality
)
-- Use PIVOT to transform the data and display the latest value for each parameter as columns for each location.
PIVOT (
	SELECT
		location_id,         -- Unique identifier for the location
	    location,            -- Name of the location
	    lat,                 -- Latitude of the location
	    lon,                 -- Longitude of the location
	    parameter,           -- Type of measurement
	    value,               -- Measured value
	    datetime             -- Timestamp of the measurement
	FROM ranked_data
	WHERE rn = 1             -- Include only the latest record for each parameter at each location
)
-- Specify the parameters to pivot into columns (e.g., PM10, PM2.5, SO2).
ON parameter IN ('pm10', 'pm25', 'so2')
-- Use the FIRST aggregate function to keep the most recent value for each parameter.
USING FIRST("value");
