"""lst = ['a', 'b', 'c']

if 'a' in lst:
    print('in')"""
# print('azerty'[:5])
"""def get_tickers_usd_for_usd(_name):
    _nouv = ''
    lst_symbol = []
    for i in tickers:
        if _name in i['symbol']:
            if i['symbol'][:len(_name)] == _name:
                _nouv = i['symbol'].replace(_name, '')
                for i2 in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD']:
                    if i2 == _nouv:
                        if _nouv != '' and len(_nouv) > 2:
                            if _nouv not in lst_symbol:
                                lst_symbol.append([_nouv, False])

            elif i['symbol'][len(_name):] == _name:
                _nouv = i['symbol'].replace(_name, '')
                for i2 in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD']:
                    if i2 == _nouv:
                        if _nouv != '' and len(_nouv) > 2:
                            if _nouv not in lst_symbol:
                                lst_symbol.append([_nouv, True])
        _nouv = ''
    return lst_symbol
"""

# lst_to_sort = [[0, 2], [2, 2], [5, 5], [10, 1]]
# sorted_list = sorted(lst_to_sort, key=lambda x: x[0], reverse=True)
#
# print(sorted_list)
"""from math import floor
print((floor(2646*10**0)/10**0) // 0.00000241)

from binance.client import Client
#import asyncio
#from binance.websockets import BinanceSocketManager
#import websocket,json
with open('keys.txt', 'r') as file:
    api_key, api_secret = str(file.readline()).split(',')
client = Client(api_key, api_secret, {"timeout": 20})


print(client.get_orderbook_tickers())"""

"""import websocket, json

SOCKET = f"wss://stream.binance.com:9443/ws/!bookTicker"


def on_close(ws):
    print('disconnected from server')


def on_open(ws):
    print('connection established')

from time import sleep
def on_message(ws, message):
    # print('received message')
    json_message = json.loads(message)
    print('msg', json_message)
    sleep(2)

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
# ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
# ws.run_forever() #ping_timeout=60
# mettre dans un def pr lancer async
if __name__ == "__main__":
    print('-- -- -- -- -- -- -- -- -- -')
    print('lancement du websocket')
    print('-- -- -- -- -- -- -- -- -- --')
    while True:
        try:
            ws.run_forever()
        except:
            pass

    print('fin')
    print('-- -- -- -- -- -- -- -- -- --')
"""

"""
from pickle import dump, load
from binance.client import Client
from time import sleep

with open('keys.txt', 'r') as file:
    api_key, api_secret = str(file.readline()).split(',')
client = Client(api_key, api_secret, {"timeout": 20})

print(client.get_orderbook_tickers()
#print(client.get_account()['balances'])
"""

"""

il faut que je créer une structure claire des chaque interaction possible entre les token

tokens: {}

usd: {tokens(y compris usd): {askPrice: 0, askQty: 0, min_val: 0}, token: min_val}

token: {token(y compris usd): min_val
"""

from binance.client import Client
from time import time, sleep
from threading import Thread

import websocket, json, os

from main import toNum

with open('keys.txt', 'r') as file:
    api_key, api_secret = str(file.readline()).split(',')
client = Client(api_key, api_secret, {"timeout": 20})
SOCKET = "wss://stream.binance.com:9443/ws/!bookTicker"


def get_token():
    global dico_tickers
    _nouv = ''
    lst_symbol = []
    for keys in dico_tickers.keys():
        for i2 in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD', 'USDS']:
            if i2 in keys:
                # print(i['symbol'][len(i2):])
                # if i['symbol'][len(i2):] == i:
                # the light <-> bug
                _nouv = keys.replace(i2, '')

                # else:
                #    _nouv = ''
                if _nouv in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD', 'USDS']:
                    _nouv = ''
        for i2 in ['EUR', 'GBP', 'AUD', 'BRL', 'TRY', 'KZT', 'HKD', 'PEN', 'RUB', 'UAH', 'UGX', 'PHP', 'USD', 'BKRW',
                   'NGN', 'BIDR', 'PAX']:
            if i2 in _nouv:
                _nouv = keys.replace(i2, '')
        if _nouv != '' and 6 > len(_nouv) > 2:
            if _nouv not in lst_symbol:
                lst_symbol.append(_nouv)
            _nouv = ''
    return lst_symbol


def init_dico():
    tickers = client.get_orderbook_tickers()
    dico = {}
    ban = False

    for i in range(len(tickers)):
        info = tickers[i]
        for bannedToken in ['BULL', 'UP', 'DOWN', 'BEAR', 'BNB', 'FTT', 'EUR', 'GBP', 'AUD', 'BRL', 'TRY', 'KZT', 'HKD',
                            'PEN', 'RUB', 'UAH', 'UGX', 'PHP',
                            'BKRW', 'NGN', 'BIDR', 'PAX']:
            if bannedToken in info['symbol']:
                ban = True

        if not ban and float(info['askQty']) != 0:
            dico[info['symbol']] = {'b': info['bidPrice'], 'B': info['bidQty'], 'a': info['askPrice'],
                                    'A': info['askQty']}
        ban = False
    return dico


# lst_token

# dico[symbol] = {
#            {'tokens': {'askPrice': 0, 'askQty': 0, 'bidPrice': 0, 'bidQty': 0, 'min_val': 0, 'liquidity': 0,
#                        'inverse': False}}}

def initOrderBookUSD():
    global lst_usd, dico_tickers

    dico_min_val = {}
    for i in client.get_exchange_info()['symbols']:
        min_step = i['filters'][2]['minQty']
        nb = int(min_step.find('1'))
        if nb == -1:
            dico_min_val[i['symbol']] = -9990
        elif nb <= 0:
            l = len(min_step.split('.')[0])
            dico_min_val[i['symbol']] = l - 1
        elif nb > 0:
            dico_min_val[i['symbol']] = nb - 1

    TempOrderBook = {}
    for usd in lst_usd:
        for pair in dico_tickers:
            if usd in pair:
                if usd not in TempOrderBook.keys():
                    TempOrderBook[usd] = {}
                else:
                    TempOrderBook[usd][pair.replace(usd, '')] = dico_tickers[pair]  # can del symbol in dico
                    TempOrderBook[usd][pair.replace(usd, '')]['min_val'] = float(dico_min_val[pair])
    TempInverseOrderBookUSD = {}
    for usd in TempOrderBook:
        for token in TempOrderBook[usd]:
            if token not in TempInverseOrderBookUSD:
                TempInverseOrderBookUSD[token] = []
            if usd not in TempInverseOrderBookUSD[token]:
                TempInverseOrderBookUSD[token].append(usd)

    return TempOrderBook, TempInverseOrderBookUSD


def initOrderBookToken():
    global dico_tickers
    dico = {}
    # BTC/USDT #BTC/ETH

    dico_min_val = {}
    for i in client.get_exchange_info()['symbols']:
        min_step = i['filters'][2]['minQty']
        nb = int(min_step.find('1'))
        if nb == -1:
            dico_min_val[i['symbol']] = -9990
        elif nb <= 0:
            l = len(min_step.split('.')[0])
            dico_min_val[i['symbol']] = l - 1
        elif nb > 0:
            dico_min_val[i['symbol']] = nb - 1
    lst_token = get_token()
    # print(lst_token)
    for t in lst_token:
        dico[t] = {}
    for symbol in lst_token:  # BTC
        for other_token in lst_token:  # ETH/BTC
            if symbol != other_token:
                for Token in dico_tickers.keys():
                    if symbol + other_token == Token:
                        # if other_token not in dico.keys():
                        dico[symbol][other_token] = {'a': float(dico_tickers[Token]['a']),
                                                     'A': float(dico_tickers[Token]['A']),
                                                     'b': float(dico_tickers[Token]['b']),
                                                     'B': float(dico_tickers[Token]['B']),
                                                     'min_val': dico_min_val[Token]}  # , 'inverse': False}
                    elif other_token + symbol == Token:
                        # if other_token not in dico.keys():
                        dico[other_token][symbol] = {'a': float(dico_tickers[Token]['a']),
                                                     'A': float(dico_tickers[Token]['A']),
                                                     'b': float(dico_tickers[Token]['b']),
                                                     'B': float(dico_tickers[Token]['B']),
                                                     'min_val': dico_min_val[Token]}  # , 'inverse': False}

    return dico



"""
print('orderUSD', OrderBookUSD)
print('orderToken', OrderBookToken)
"""



def on_close(ws):
    print('disconnected from server at:', time())


def on_open(ws):
    print('connection established at:', time())


def on_message(ws, message):
    global dico_tickers, OrderBookUSD, OrderBookToken
    # print('received message')
    json_m = json.loads(message)
    del json_m['u']
    for usd in OrderBookUSD.keys():
        if usd in json_m['s']:
            otherT = json_m['s'].replace(usd, '')
            # voir la methode optimale OrderBookUSD[usd][json_m['s'].replace(usd)]['b'] = {json_m['s'], json_m['s'], json_m['s'], json_m['s'], json_m['s']}
            OrderBookUSD[usd][otherT]['a'] = json_m['a']
            OrderBookUSD[usd][otherT]['A'] = json_m['A']
            OrderBookUSD[usd][otherT]['b'] = json_m['b']
            OrderBookUSD[usd][otherT]['B'] = json_m['B']
            return

    for Token in OrderBookToken.keys():
        if Token in json_m['s']:
            otherT = json_m['s'].replace(Token, '')
            #if json_m['s'] == 'ETHBTC':
            #    print(json_m)
            #    print(otherT, Token, json_m['s'][:len(Token)])
            if Token in json_m['s'][:len(Token)]:
                # voir la methode optimale OrderBookUSD[usd][json_m['s'].replace(usd)]['b'] = {json_m['s'], json_m['s'], json_m['s'], json_m['s'], json_m['s']}
                OrderBookToken[Token][otherT]['a'] = json_m['a']
                OrderBookToken[Token][otherT]['A'] = json_m['A']
                OrderBookToken[Token][otherT]['b'] = json_m['b']
                OrderBookToken[Token][otherT]['B'] = json_m['B']
                return
            else:
                # voir la methode optimale OrderBookToken[usd][json_m['s'].replace(usd)]['b'] = {json_m['s'], json_m['s'], json_m['s'], json_m['s'], json_m['s']}
                OrderBookToken[otherT][Token]['a'] = json_m['a']
                OrderBookToken[otherT][Token]['A'] = json_m['A']
                OrderBookToken[otherT][Token]['b'] = json_m['b']
                OrderBookToken[otherT][Token]['B'] = json_m['B']
                return

    print('orderbook', initOrderBookUSD())
    # sleep(0.001)

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

dico_err = {'balance': {}, 'low_liquidity': 0, 'result': 0}

lst_usd = ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD']
dico_tickers = init_dico()

print('Orderbook load . . .')
OrderBookUSD, InverseOrderBookUSD = initOrderBookUSD()
OrderBookToken = initOrderBookToken()
print('orderUSD', OrderBookUSD)
print('InverseorderUSD', InverseOrderBookUSD)
print('orderToken', OrderBookToken)
sleep(2)
# launch_scan_trade()

print('Start websocket')
t_start = time()
if __name__ == "__main__":
    print('-- -- -- -- -- -- -- -- -- --')
    print('lancement du websocket')
    print('-- -- -- -- -- -- -- -- -- --')
    while True:
        try:
            ws.run_forever()
        except:
            pass
        sleep(5)

#{'TUSD':
# {'ETH':
# {'b': '2791.17000000',
# 'B': '1.09360000',
# 'a': '2795.86000000',
# 'A': '2.94010000',
# 'min_val': 4.0}
# }

# {'TUSD': {'ETH': {'b': '2791.17000000', 'B': '1.09360000', 'a': '2795.86000000', 'A': '2.94010000', 'min_val': 4.0}

lst_pos = []
for usd in OrderBookUSD.keys():
    for token1 in OrderBookUSD[usd].keys():
        lst_pos.append({'amount': toNum(100/OrderBookUSD[usd][token1]['b']), 'usd': usd, 'token1': token1, 'min_val_usd_token1': OrderBookUSD[usd][token1]['min_val'], 'min_val_token1_token2': 0, 'min_val_token2_usd': 0, 'token2': '', 'usdOut': ''})

new_lst_pos = []
for i in range(len(lst_pos)):
    #token1 pos['token1']
    for token2 in OrderBookToken[lst_pos[i]['token1']].keys():
        new_lst_pos.append(lst_pos[i])
        new_lst_pos[-1]['amount'] = toNum(new_lst_pos[-1]['amount']*OrderBookToken[lst_pos[i]['token1']][token2])
        new_lst_pos[-1]['token2'] = token2
        new_lst_pos[-1]['min_val_token1_token2'] = OrderBookToken[lst_pos[i]['token']][token2]['min_val']

lst_pos = new_lst_pos
new_lst_pos = []
for i in range(len(lst_pos)):
    #token1 pos['token1']

    for usd in InverseOrderBookUSD[lst_pos[i]['token2']]:
        new_lst_pos.append(lst_pos[i])
        new_lst_pos[-1]['amount'] = toNum(new_lst_pos[-1]['amount'] * OrderBookToken[usd][lst_pos[i]['token2']]['b'])  # lst_pos[i]['amount']
        new_lst_pos[-1]['usdOut'] = usd
        new_lst_pos[-1]['min_val_usd_token2'] = OrderBookToken[usd][lst_pos[i]['token2']]['min_val']
lst_pos = new_lst_pos
del new_lst_pos
print('lst position', lst_pos)


"""def calc_benef(_token_name, lst_usd, lst_token_tokens, lst_out):
    global min_earn
    # bidPriceBASE, askPriceBASE, askPrice, bidPriceBASE2, askPriceBASE2
    # fait abstraction de la liquidité dispo
    buy_part = 100
    lst_entry = []
    lst_result = []"""

"""

    pour chaque token prendre la liquidité diponible est trouver combien je peux mettre en buy_part

    """
"""cpt = 0
    for i in lst_usd:
        if float(i[0]) != 0 and float(i[1]) != 0:
            lst_entry.append([buy_part / float(i[0]), float(i[0]), float(i[1]), i[-1]])

    for i in lst_entry:
        for i2 in lst_token_tokens:"""
"""print('in')
            print(lst_usd[cpt], i, i2, lst_out[i2[2]])
            print('out')
"""
# print(i[-1], lst_out[i2[2]].keys(), lst_out[i2[2]])
# check if usd out = usd in and !=0
"""if float(i2[0]) > 0 and float(i2[1]) > 0:
                for key in lst_out[i2[2]].keys():
                    if float(lst_out[i2[2]][key][0]) > 0 and float(lst_out[i2[2]][key][0]) > 0:
                        # for USD in lst_out[i2[2]]:
                        if i2[-1]:
                            result = (float(i[0]) / float(i2[0]) * float(lst_out[i2[2]][key][0])) - (
                                    buy_part * 0.075 / 100) * 3
                        else:
                            result = (float(i[0]) * float(i2[0]) * float(lst_out[i2[2]][key][0])) - (
                                    buy_part * 0.075 / 100) * 3
                        # print('result', result)
                        if result - buy_part * min_earn > 0:
"""
"""print('result', result)
                            print('in')
                            print(lst_usd[cpt])
                            print(i)
                            print(i2)
                            print(lst_out[i2[2]])
                            print('out')"""
# print(result)
"""
                            calc
                            """
# print(i[2], i2[1], float(lst_out[i2[2]][i[-1]][0]))
# liquidity2 = float(lst_out[i2[2]][i[-1]][1])*float(lst_out[i2[2]][i[-1]][0])
# get liquidity of Ftoken
# print('b', float(lst_usd[cpt][0])*i[2])
# ticker BTC/ETH - ETH/BTC
"""if i2[-1]:  # ETH/BTC
                                liquidity2 = float(i2[0]) * float(i2[1])
                            else:  # BTC/ETH
                                liquidity2 = float(i2[1])
                            # calc dollar liquidity
                            if i[2] < liquidity2:
                                main_liquidity = i[2] * float(i[1])
                            else:
                                main_liquidity = liquidity2 * float(i[1])
                            # prendre la liquidité la plus faible
                            if main_liquidity > float(lst_out[i2[2]][key][0]) * float(lst_out[i2[2]][key][1]):
                                main_liquidity = float(lst_out[i2[2]][key][0]) * float(lst_out[i2[2]][key][1])

                            # print('liquidity', i[2]*float(lst_usd[cpt][0]), liquidity2)
                            if main_liquidity > 100:
                                # cpt += 1
                                lst_result.append([round(result, 4), main_liquidity, i[-1], _token_name, i2[2], key])
    # if cpt != 0:
    #    print('\nopportunity', cpt, end='')
    # f = 100 / askPriceBASE / askPrice * bidPriceBASE2
    # f2 = 100 / askPriceBASE2 / askPrice * bidPriceBASE

    return lst_result"""

"""
from binance.client import Client
import math

with open('keys.txt', 'r') as file:
    api_key, api_secret = str(file.readline()).split(',')
client = Client(api_key, api_secret, {"timeout": 20})
min_step = client.get_symbol_info(symbol='ETHBTC')['filters'][2]['minQty']
print(min_step)
nb = min_step.find('1')
if nb >= 0:
    nb=len(min_step)
    pass#print('nb', nb)
else:
    pass#print('nb', nb-1)

#print('r', round(12.34, 0))

min_step = client.get_exchange_info()['symbols'][0]['filters'][2]['minQty']
dico_all_symbol_min_value = {}
for i in client.get_exchange_info()['symbols']:
    min_step = i['filters'][2]['minQty']
    nb = min_step.find('1')
    if nb <= 0:
        nb = int(float(min_step))
        dico_all_symbol_min_value[i['symbol']] = nb
    else:
        dico_all_symbol_min_value[i['symbol']] = nb - 1
#print(dico_all_symbol_min_value)

"""