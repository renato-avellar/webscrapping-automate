import requests
import base64
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

current_datetime = datetime.now()
load_dotenv()

myuser = os.environ['myuser']
mypassword = os.environ['mypassword']
credentials = f"{myuser}:{mypassword}"
credentials_base64 = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
headers = {'Authorization': f'Basic {credentials_base64}',}

url = os.environ(url)
response = requests.get(url, headers=headers)
file = open('job_histories.xml', 'w') 
file.write(response.text) 
file.close() 

tree = ET.parse('job_histories.xml')
root = tree.getroot()
result = root.find('result')
root.remove(result)

data = []
filtro = "*"
for child in root.iter(filtro):
  row = {}
  for field in child:
    row[field.tag] = field.text
    data.append(row)


df = pd.DataFrame.from_dict(data)
df.drop(['records', 'record'], axis=1, inplace=True)
df = df.drop(df.index[:101])
df = df.drop_duplicates()
df = df.reset_index(drop=True)

file_name = current_datetime.strftime('%Y-%m-%d_%H-%M') + '.xlsx'
df.to_excel(file_name, index=False)