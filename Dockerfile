# docker run -it ubuntu bash
# docker run -t python:3.11
# docker run -it --entrypoint=bash python:3.11
# docker run -it test:pandas 2023-09-25

FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2-binary pyarrow

WORKDIR /app

COPY insert_data.py insert_data.py

ENTRYPOINT [ "python", "insert_data.py" ]