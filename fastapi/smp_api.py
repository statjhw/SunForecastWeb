import requests
import configparser

config = configparser.ConfigParser()
config.read('fastapi/config.ini')


api_key = config['api']['api_key']

url = 'https://openapi.kpx.or.kr/openapi/smp1hToday/getSmp1hToday'
params ={'serviceKey' : f'{api_key}', 'areaCd' : '1' }

response = requests.get(url, params=params)
print(response.content)