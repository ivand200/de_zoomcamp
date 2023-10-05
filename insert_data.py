#!/usr/bin/env python
# coding: utf-8
import os
from time import time
import argparse

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    if url.endswith(".csv.gz"):
        csv_name = "output.csv.gz"
    elif url.endswith(".parquet"):
        csv_name = "output.parquet"
    else:
        csv_name = "output.csv"

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{int(port)}/{db}")

    if csv_name.endswith(".parquet"):  # .parquet
        df = pd.read_parquet(csv_name)
        df.to_csv(f"{csv_name[:-8]}.csv")
        csv_name = f"{csv_name[:-8]}.csv"

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)  # encoding="utf-8", on_bad_lines="skip"

    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    df.to_sql(name=table_name, con=engine, if_exists="append")

    while True:
        try:
            t_start = time()
        
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists="append")

            t_end = time()

            print(f"Time: {t_end - t_start}")

        except StopIteration:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load data from csv, parquet to Postgres")

    parser.add_argument("--user", help="user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument("--table_name", help="name of the table where we will write the results to")
    parser.add_argument("--url", help="url of the csv file")

    args = parser.parse_args()

    main(args)



    

    

# df = pd.read_csv("yellow_tripdata.csv", nrows=100)

# engine = create_engine("postgresql://root:root@localhost:5432/ny_taxy")

# df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
# df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

# print(pd.io.sql.get_schema(df, name="yellow_taxi_data", con=engine))

# df_iter = pd.read_csv("yellow_tripdata.csv", iterator=True, chunksize=100000)

# df.to_sql(name="yellow_taxi_data", con=engine, if_exists="replace")

# df.head(n=0).to_sql(name="yellow_taxi_data", con=engine, if_exists="replace")

# while True:
#     t_start = time()
#     df = next(df_iter)
#     df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
#     df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
#     df.to_sql(name="yellow_taxi_data", con=engine, if_exists="append")
#     t_end = time()
#     print(f"Time: {t_end - t_start}")
