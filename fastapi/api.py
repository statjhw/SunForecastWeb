import requests
import configparser
import xml.etree.ElementTree as ET

config = configparser.ConfigParser()
config.read('fastapi/config.ini')

def smp_price() :
    api_key = config['smp_api']['api_key']

    url = 'https://openapi.kpx.or.kr/openapi/smp1hToday/getSmp1hToday'
    params ={'serviceKey' : f'{api_key}', 'areaCd' : '1' }

    response = requests.get(url, params=params)
    
    root = ET.fromstring(response)

    smp = [item.find('smp').text for item in root.findall('.//item')][0]

    return smp

def rec_price() :
    api_key = config['rec_api']['api_key']

    url = 'http://www.iwest.co.kr:8082/openapi-data/service/TradeList/Trade'
    params ={'serviceKey' : f'{api_key}', 'strDateE' : '202407', 'strDateS' : '202407' }

    response = requests.get(url, params=params)

    root = ET.fromstring(response)

    recprices = [item.find('recprice').text for item in root.findall('.//item')][-1]

    return recprices

