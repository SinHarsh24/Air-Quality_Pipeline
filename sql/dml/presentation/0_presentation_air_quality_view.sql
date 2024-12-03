-- Create or replace a view named 'air_quality' in the 'presentation' schema.
-- This view processes raw air quality data to ensure data quality by keeping only the latest record for each sensor parameter per datetime.

CREATE OR REPLACE VIEW presentation.air_quality AS (
    -- Use a Common Table Expression (CTE) to add a row number for each record based on specific criteria.
    WITH ranked_data AS (
        SELECT
            *,  -- Select all columns from the raw data.
            ROW_NUMBER() OVER (
                PARTITION BY location_id, sensors_id, "datetime", "parameter" 
                ORDER BY ingestion_datetime DESC
            ) AS rn -- Assign a row number, prioritizing the most recent ingestion time.
        FROM raw.air_quality
        WHERE parameter IN ('pm10', 'pm25', 'so2')  -- Filter for specific parameters.
        AND "value" >= 0                            -- Exclude records with negative values.
    )
    SELECT
        location_id,
        sensors_id,
        "location",
        "datetime",
        lat,
        lon,
        "parameter",
        units,
        "value",
        "month",
        "year",
        ingestion_datetime
    FROM ranked_data
    WHERE rn = 1  -- Keep only the latest record for each group (row number 1).
);
