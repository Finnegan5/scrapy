import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json

token = os.environ.get("TOKEN")

url = 'http://127.0.0.1:3000/api/v1/db_url'
headers = {'token': token}
r = requests.get(url, headers=headers)
print(json.loads(r.text)['database_url'])
