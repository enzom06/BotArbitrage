from pickle import dump, load
from binance.client import Client
from time import sleep

with open('keys.txt', 'r') as file:
    api_key, api_secret = str(file.readline()).split(',')
client = Client(api_key, api_secret, {"timeout": 20})

"""

#save token in file

tickers = client.get_orderbook_tickers()
def get_token():
    _nouv = ''
    lst_symbol = []
    for i in tickers:
        for i2 in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD', 'USDS']:
            if i2 in i['symbol']:
                # print(i['symbol'][len(i2):])
                # if i['symbol'][len(i2):] == i:
                # the light <-> bug
                _nouv = i['symbol'].replace(i2, '')

                # else:
                #    _nouv = ''
                if _nouv in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD', 'USDS']:
                    _nouv = ''
        for i2 in ['EUR', 'GBP', 'AUD', 'BRL', 'TRY', 'KZT', 'HKD', 'PEN', 'RUB', 'UAH', 'UGX', 'PHP', 'USD', 'BKRW',
                   'NGN', 'BIDR', 'PAX']:
            if i2 in _nouv:
                _nouv = ''
        if _nouv != '' and 6 > len(_nouv) > 2:
            if _nouv not in lst_symbol:
                lst_symbol.append(_nouv)
            _nouv = ''
    return lst_symbol

lst_token = get_token()

with open('lst_token.txt', 'w') as fic:
    fic.write(','.join(lst_token))"""


# print(client.futures_create_order(symbol='MKRUSDT', quantity=str(0.001), side='BUY',
#                            type='MARKET'))
# print(client.futures_create_order(symbol='MKRUSDT', quantity=str(0.001), side='SELL',
#                            type='MARKET'))

#           0             1           2        3        4          5           6
# [estimation sortie, max devise, TOKEN_IN, TOKEN_1, TOKEN_2, TOKEN_OUT, invers_token]
def trade(pos):
    asset = client.get_asset_balance(asset=pos[2])['free']
    print('asset: ', asset)
    if asset < 20:
        return False

    l_in = 0
    price_in = 0
    l_middle = 0
    l_ask_middle = 0
    price_middle = 0
    l_out = 0
    price_out = 0
    min_liquidity = 0
    inverse_pair = False

    nb_token_m1 = 0
    nb_token_m2 = 0
    for i in client.get_orderbook_tickers():
        if i['symbol'] == pos[3] + pos[2]:
            l_in = float(i['askQty'])  # BTC
            price_in = float(i['askPrice'])
        elif i['symbol'] == pos[4] + pos[5]:
            price_out = float(i['askPrice'])
            l_out = price_out * float(i['bidQty'])  # USD

        elif i['symbol'] == pos[3] + pos[4] or i['symbol'] == pos[4] + pos[3]:
            price_middle = float(i['askPrice'])
            inverse_pair = pos[-1]
            l_ask_middle = float(i['askQty'])
            l_middle = float(i['bidQty'])

    if inverse_pair:
        l_middle = price_middle * l_ask_middle
    else:
        l_middle = l_middle

    # calc dollar liquidity
    if l_in < l_middle:
        min_liquidity = l_in * price_in
    else:
        min_liquidity = l_middle * price_in

    if min_liquidity > l_out:
        min_liquidity = l_out

    if min_liquidity <= 20:  # choisit arbitrairement
        return False
    else:
        if asset > min_liquidity * 0.8:
            asset = min_liquidity * 0.8
    nb_token_m1 = asset / price_in
    if inverse_pair:
        nb_token_m2 = nb_token_m1 / price_middle
        result = nb_token_m1 * price_out - (asset * 0.0751 / 100) * 3
    else:
        nb_token_m2 = nb_token_m1 * price_middle
        result = nb_token_m2 * price_out - (asset * 0.0751 / 100) * 3

    if result <= asset:
        return False

    # ordre buy order
    order = client.order_market_buy(symbol=pos[3] + pos[2], quantity=nb_token_m1)
    print(order)
    sleep(0.1)
    while float(client.get_asset_balance(asset=pos[3] + pos[2])['asset']['free']) >= 0.9 * nb_token_m1:
        print('wait')
        sleep(0.1)
    if inverse_pair:
        s = pos[4] + pos[3]
        print(client.order_market_buy(symbol=s, quantity=nb_token_m2))
    else:
        s = pos[3] + pos[4]
        print(client.order_market_sell(symbol=s, quantity=nb_token_m1))
    sleep(0.1)
    while float(client.get_asset_balance(asset=s)['asset']['free']) >= 0.9 * nb_token_m2:
        sleep(0.1)
    print(client.order_market_sell(symbol=pos[4] + pos[5], quantity=nb_token_m2))
    return True


#print(client.get_asset_balance(asset='BTC')['free'])
