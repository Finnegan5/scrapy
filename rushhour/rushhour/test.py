import os
from dotenv import load_dotenv
load_dotenv()
token = os.environ.get("api-token")
print(token)
