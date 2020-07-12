import os
from dotenv import load_dotenv
load_dotenv()
import requests

token = os.environ.get("TOKEN")
print(token)

url = 'http://127.0.0.1:3000/api/v1/db_url'
headers = {'token': token}
r = requests.get(url, headers=headers)
print(r.text)
