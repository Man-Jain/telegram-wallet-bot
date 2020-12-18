import json
import requests
import datetime

covalenthq = 'ckey_39b2f5f693634dc5a87849e3cd5'

url = 'https://api.covalenthq.com/v1/1/address/'

def get_user_balances(query):
    userid = query.message.chat.id
    print(userid)
    address = get_user_address(userid)
    print(address)
    param = '/balances_v2/?&key=' + covalenthq
    resp = requests.get(url+address+param)
    items = resp.json()
    items = items['data']['items']
    for item in items:
        if len(item['balance']) > 18:
            item['balance'] = str(int(item["balance"]) / 10 ** 18)
        else:
            item['balance'] = f'{int(item["balance"]) / 10 ** 18:.{20 - len(item["balance"])}f}'
    return items

def get_user_transactions(query):
    userid = query.message.chat.id
    address = get_user_address(userid)
    param = '/transactions_v2/?page-size=10&key=' + covalenthq
    resp = requests.get(url+address+param)
    items = resp.json()
    items = items['data']['items']
    for item in items:
        if len(item['value']) > 18:
            item['value'] = str(int(item["value"]) / 10 ** 18)
        else:
            item['value'] = f'{int(item["value"]) / 10 ** 18:.{20 - len(item["value"])}f}'

        item["block_signed_at"] = datetime.datetime.strptime(item["block_signed_at"], '%Y-%m-%dT%H:%M:%SZ').strftime("%b %d %Y %H:%M:%S")

    return items

def get_user_address(userid):
    address = ''
    with open('data.json') as file:
        data = file.read()
        users = json.loads(data)['users']
        for user in users:
            if user['user'] == userid:
                address = user['address']

    return address

def set_user_address(userid, address):
    users = []
    try:
        with open('data.json', 'r') as file:
            data = file.read()
            print(data)
            users = json.loads(data)['users']
            print(users)

        finduser = get_user_address(userid)
        if finduser:
            for user in users:
                if user['user'] == userid:
                    user['address'] = address
        else:
            users.append({
                'user': userid,
                'address': address
            })
        print(users)
        
        with open('data.json', 'w') as file:
            file.write(json.dumps({'users': users}))
    except:
        users.append({
                'user': userid,
                'address': address
            })
        
        with open('data.json', 'w') as file:
            file.write(json.dumps({'users': users}))

    return address