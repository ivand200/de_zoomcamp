services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airlow
      POSTGRES_PASSWORD: airlow
      POSTGRES_DB: airlow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airlow"]
      interval: 5s
      retries: 5
    restart: always

  -v $(pwd)/my_taxy_postgres_data:/var/lib/postgresql/data \
pgcli -h localhost -p 5432 -u root -d ny_taxy

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxy" \
  -p 5432:5432 \
  -v ./my_taxy_postgres_data:/var/lib/postgresql/data \
  postgres:13


docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="ivand1988@outlook.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4



docker pull dpage/pgadmin4


https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf


### Network 

docker network create pg-network

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxy" \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  -v ./my_taxy_postgres_data:/var/lib/postgresql/data \
  postgres:13


docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="ivand1988@outlook.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4


python3 insert_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --db=ny_taxy \
  --port=5432 \
  --table_name=yellow_taxi_data \
  --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet



docker build -t taxi_insert .

docker run -it \
  --network=pg-network \
  taxi_insert \
  --user=root \
  --password=root \
  --host=pg-database \
  --db=ny_taxy \
  --port=5432 \
  --table_name=yellow_taxi_data \
  --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet