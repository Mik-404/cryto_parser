import requests
import pandas as pd
import datetime
import json

url1 = 'https://api.livecoinwatch.com/coins/list'
url2 = 'https://api.livecoinwatch.com/coins/single'

def parse_global_tab (json_l):
    ready_js = json.loads(json_l)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    list_cc = []
    for i in ready_js:
        nm = i['name']
        sh = i['code']
        cc = i['rate']
        list_cc.append({'name': nm, 'short': sh, 'course': cc})

    return [time, list_cc]

def parse_local_price (json_l):
    ready_js = json.loads(json_l)
    return {'time': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")], 'price': [ready_js["rate"]]}

def main ():
    headers = {'content-type': 'application/json', 'x-api-key': '97c34f82-2fef-4363-9ffa-a636b8116afa'}

    #bitcoin
    body = { 'currency': 'USD', 'code': 'BTC', 'meta': False}
    resp = requests.post(url2, headers = headers, json=body)
    helpd = pd.DataFrame.from_dict(parse_local_price(resp.text))
    try:
        dd = pd.read_csv('bitcoin.csv')
        dd = pd.concat([dd, helpd])
        dd.to_csv('bitcoin.csv', index=False)
    except:
        helpd.to_csv('bitcoin.csv', index=False)

    #ethereum
    body = { 'currency': 'USD', 'code': 'ETH', 'meta': False}
    resp = requests.post(url2, headers = headers, json=body)
    helpd = pd.DataFrame.from_dict(parse_local_price(resp.text))
    try:
        dd = pd.read_csv('ethereum.csv')
        dd = pd.concat([dd, helpd])
        dd.to_csv('ethereum.csv', index=False)
    except:
        helpd.to_csv('ethereum.csv', index=False)

    #top50
    body = { 'currency': 'USD', 'sort': 'rank', 'order': 'ascending', 'offset': 0, 'limit': 50, 'meta': True}
    resp = requests.post(url1, headers = headers, json=body)
    helpd = pd.DataFrame(parse_global_tab(resp.text)).T
    try:
        dd = pd.read_excel('top50.xlsx', engine='openpyxl')
        dd = pd.concat([dd, helpd])
        dd.to_excel('top50.xlsx', index=False, engine='openpyxl')
    except:
        helpd.to_excel('top50.xlsx', index=False, engine='openpyxl')


if (__name__ == "__main__"):
    main()