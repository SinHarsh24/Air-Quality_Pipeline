-- Create or replace a view named 'daily_air_quality_stats' in the 'presentation' schema.
-- This view calculates average daily air quality values for each parameter at each location.

CREATE OR REPLACE VIEW presentation.daily_air_quality_stats AS
-- Use a Common Table Expression (CTE) to preprocess air quality data for daily statistics.
WITH air_quality_cte AS (
    SELECT
        location_id,                           -- Unique identifier for the location.
        location,                              -- Name of the location.
        CAST("datetime" AS DATE) AS measurement_date, -- Extract the date portion from the timestamp for daily grouping.
        lat,                                   -- Latitude of the location.
        lon,                                   -- Longitude of the location.
        parameter,                             -- Type of measurement (e.g., PM10, PM2.5).
        units,                                 -- Units of the measurement.
        value,                                 -- Measured value.
        dayofweek("datetime") AS weekday_number, -- Day of the week as a number (e.g., 1 for Monday, 7 for Sunday).
        dayname("datetime") AS weekday,        -- Name of the day of the week (e.g., 'Monday', 'Sunday').
        CASE
            WHEN dayname("datetime") = 'Saturday' OR dayname("datetime") = 'Sunday'
            THEN 1                              -- Mark as 1 if the day is a weekend (Saturday or Sunday).
            ELSE 0                              -- Mark as 0 if the day is a weekday.
        END AS is_weekend                      -- Flag indicating whether the day is a weekend.
    FROM presentation.air_quality              -- Use preprocessed air quality data from the presentation schema.
)
-- Select the processed data and compute daily average air quality statistics.
SELECT
    location_id,                               -- Unique identifier for the location.
    location,                                  -- Name of the location.
    measurement_date,                          -- Date of the measurement.
    weekday_number,                            -- Day of the week as a number.
    weekday,                                   -- Name of the day of the week.
    is_weekend,                                -- Flag indicating whether the day is a weekend.
    lat,                                       -- Latitude of the location.
    lon,                                       -- Longitude of the location.
    parameter,                                 -- Type of measurement.
    units,                                     -- Units of the measurement.
    AVG(value) AS average_value                -- Calculate the average value of the measurements for the day.
FROM air_quality_cte
GROUP BY                                       -- Group data by all relevant fields for daily statistics.
    location_id,
    location,
    measurement_date,
    weekday_number,
    weekday,
    is_weekend,
    lat,
    lon,
    parameter,
    units;
