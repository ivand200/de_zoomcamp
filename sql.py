"""
SELECT *
FROM
  yellow_taxi_data taxi,
  zones pick_up,
  zones drop_off
WHERE
  taxi."PULocationID" = pick_up."LocationID" AND
  taxi."DOLocationID" = drop_off."LocationID"
LIMIT 100;


SELECT
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  total_amount,
  CONCAT(pick_up."Borough", ' / ', pick_up."Zone") AS "pickup_loc",
  CONCAT(drop_off."Borough", ' / ', drop_off."Zone") AS "dropoff_loc"
FROM
  yellow_taxi_data taxi,
  zones pick_up,
  zones drop_off
WHERE
  taxi."PULocationID" = pick_up."LocationID" AND
  taxi."DOLocationID" = drop_off."LocationID"
LIMIT 100;


SELECT
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  total_amount,
  CONCAT(pick_up."Borough", ' / ', pick_up."Zone") AS "pickup_loc",
  CONCAT(drop_off."Borough", ' / ', drop_off."Zone") AS "dropoff_loc"
FROM
  yellow_taxi_data taxi 
    JOIN zones pick_up ON taxi."PULocationID" = pick_up."LocationID"
	JOIN zones drop_off ON taxi."DOLocationID" = drop_off."LocationID"  
LIMIT 100;


SELECT
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  total_amount,
  "PULocationID",
  "DOLocationID"
FROM 
  yellow_taxi_data taxi
WHERE 
  "PULocationID" NOT IN (SELECT "LocationID" FROM zones)
LIMIT 100;


SELECT
  CAST(tpep_dropoff_datetime AS DATE) as "day",
  total_amount
FROM
  yellow_taxi_data taxi 
    JOIN zones pick_up ON taxi."PULocationID" = pick_up."LocationID"
	JOIN zones drop_off ON taxi."DOLocationID" = drop_off."LocationID"  
LIMIT 100;


SELECT
  CAST(tpep_dropoff_datetime AS DATE) as "day",
  COUNT(*)
FROM
  yellow_taxi_data taxi 
GROUP BY
  CAST(tpep_dropoff_datetime AS DATE)
ORDER BY "day" ASC;


SELECT
  CAST(tpep_dropoff_datetime AS DATE) as "day",
  COUNT(*) as "count"
FROM
  yellow_taxi_data taxi 
GROUP BY
  CAST(tpep_dropoff_datetime AS DATE)
ORDER BY "count" DESC;


SELECT
  CAST(tpep_dropoff_datetime AS DATE) as "day",
  COUNT(*) as "count",
  MAX(total_amount),
  MAX(passenger_count)
FROM
  yellow_taxi_data taxi 
GROUP BY
  CAST(tpep_dropoff_datetime AS DATE)
ORDER BY "count" DESC;


SELECT
  CAST(tpep_dropoff_datetime AS DATE) as "day",
  "DOLocationID",
  COUNT(*) as "count",
  MAX(total_amount),
  MAX(passenger_count)
FROM
  yellow_taxi_data taxi 
GROUP BY
  1, 2
ORDER BY
  "day" ASC,
  "DOLocationID" ASC;
"""