import requests
import json 
import os

from django.http import response

API_V1_STR = os.environ.get('API_V1_STR')
print (API_V1_STR)
url="http://127.0.0.1:8080/api/v1/charts/pie"
_text='{"x": "red.keyword","y": {"value": "metrics.clicks","calculate": "sum"},"dataset": "daily"}'
_json=json.loads(_text)
token=""
_headers={'Content-Type':'application/json', 'Autorization':token}
response=requests.post(url, data=json.dumps(_json), headers=_headers)

print(json.loads(response.content))