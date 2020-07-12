import requests
import json
import os
import psycopg2
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("TOKEN")

url = 'http://127.0.0.1:3000/api/v1/db_url'
headers = {'token': token}
r = requests.get(url, headers=headers)
url = json.loads(r.text)['database_url']

result = urlparse(url)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

connection = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname
)
cursor = connection.cursor()

# copy_sql = """
#            COPY hhv_records("artist", "title", "price", "label", "release", "created_at", "updated_at") FROM stdin WITH CSV HEADER
#            DELIMITER as ','
#            QUOTE as '"'
#            """
sql = 'select * from hhv_records'

# with open('hhv.csv', 'r') as f:
#     # Notice that we don't need the `csv` module.
#     next(f) # Skip the header row.
#     cursor.copy_expert(sql=copy_sql, file=f)
cursor.execute(sql)
print(cursor.fetchall())

connection.commit()
cursor.close()
