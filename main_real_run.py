from binance.client import Client
from time import sleep, time, asctime
from math import floor
from threading import Thread

import websocket, json, os

# from random import shuffle
# from trade import trade

with open('keys.txt', 'r') as file:
    api_key, api_secret = str(file.readline()).split(',')
client = Client(api_key, api_secret, {"timeout": 20})


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def update_balance():
    global dico_balance
    b = client.get_account()['balances']
    for asset in b:
        if float(asset['free']) != 0:
            if asset['asset'] in dico_balance.keys():
                dico_balance[asset['asset']] = float(asset['free'])
            else:
                dico_balance[asset['asset']] = float(asset['free'])


# clearConsole()

def init_dico():
    tickers = client.get_orderbook_tickers()
    dico = {}
    ban = False

    for i in range(len(tickers)):
        info = tickers[i]
        for bannedToken in ['BULL', 'UP', 'DOWN', 'BEAR', 'BNB', 'FTT', 'EUR', 'GBP', 'AUD', 'BRL', 'TRY', 'KZT', 'HKD',
                            'PEN', 'RUB', 'UAH', 'UGX', 'PHP',
                            'BKRW', 'NGN', 'BIDR', 'PAX', 'SUSD']:
            if bannedToken in info['symbol'][:len(bannedToken)] or bannedToken in info['symbol'][len(bannedToken):]:
                ban = True

        if not ban and float(info['askQty']) != 0:
            dico[info['symbol']] = {'b': float(info['bidPrice']), 'B': float(info['bidQty']),
                                    'a': float(info['askPrice']),
                                    'A': float(info['askQty'])}
        ban = False
    return dico


def get_dollar_path():
    # ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD']
    dico = {'TUSD': {'USDT': False, 'BUSD': False},
            'DAI': {'BUSD': True, 'USDT': True},
            'USDC': {'BUSD': False, 'USDT': False},
            'USDT': {'TUSD': True, 'DAI': False, 'USDC': True, 'USDP': True, 'UST': True, 'BUSD': True},
            'USDP': {'BUSD': False, 'USDT': False},
            'UST': {'BUSD': False, 'USDT': False},
            'BUSD': {'TUSD': False, 'DAI': False, 'USDC': True, 'USDT': False, 'USDP': True, 'UST': True}
            }

    return dico


def initOrderBookUSD():
    global lst_usd, dico_tickers

    dico_min_val = {}
    for i in client.get_exchange_info()['symbols']:
        min_step = i['filters'][2]['minQty']
        nb = int(min_step.find('1'))
        if nb > 0:
            dico_min_val[i['symbol']] = nb - 1
            # print('dico val', [i['symbol']], min_step, nb-1)

        elif nb <= 0:
            l = len(min_step.split('.')[0])
            dico_min_val[i['symbol']] = -l + 1
            # print('dico val', i['symbol'], min_step, -l + 1)
        # elif nb == 0:
        #    dico_min_val[i['symbol']] = -9990
        #    print('dico val', i['symbol'], min_step, -9990)
    TempOrderBook = {}
    for usd in lst_usd:
        for pair in dico_tickers.keys():
            if usd in pair:
                ban = False
                p = pair.replace(usd, '')
                for u in all_lst_usd:
                    if p in u:
                        ban = True
                if not ban:
                    if usd not in TempOrderBook.keys():
                        TempOrderBook[usd] = {}
                        TempOrderBook[usd][pair.replace(usd, '')] = dico_tickers[pair]  # can del symbol in dico
                        TempOrderBook[usd][pair.replace(usd, '')]['min_val'] = float(dico_min_val[pair])
                    else:
                        TempOrderBook[usd][pair.replace(usd, '')] = dico_tickers[pair]  # can del symbol in dico
                        TempOrderBook[usd][pair.replace(usd, '')]['min_val'] = float(dico_min_val[pair])
    # dico inverse for find out
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
    for Token in dico_tickers.keys():  # ETH/BTC
        for symbol in lst_token:  # BTC
            for other_token in lst_token:
                # for Token in dico_tickers.keys():  # ETH/BTC
                if symbol + other_token == Token:
                    # if other_token not in dico.keys():
                    dico[symbol][other_token] = {'a': float(dico_tickers[Token]['a']),
                                                 'A': float(dico_tickers[Token]['A']),
                                                 'b': float(dico_tickers[Token]['b']),
                                                 'B': float(dico_tickers[Token]['B']),
                                                 'min_val': int(dico_min_val[Token])}

    return dico


# print(client.futures_create_order(symbol='', quantity=str(0.001), side='BUY',
#                            type='MARKET'))
# print(client.futures_create_order(symbol='', quantity=str(0.001), side='SELL',
#                            type='MARKET'))
def get_min_val():
    dico = {}
    for i in client.get_exchange_info()['symbols']:
        min_step = i['filters'][2]['minQty']
        nb = int(min_step.find('1'))
        if nb == -1:
            dico[i['symbol']] = -9990
        elif nb <= 0:
            l = len(min_step.split('.')[0])
            dico[i['symbol']] = l - 1
        elif nb > 0:
            dico[i['symbol']] = nb - 1
    return dico


def min_pos(min_val):
    return 1 * 10 ** (-min_val)


def toNum(_val, p=-9990, for_trade=False):
    if p == -9990:
        if not for_trade:
            return floor(_val * (10 ** 8)) / (10 ** 8)
        else:
            return format(floor(_val * 10 ** 8) / 10 ** 8, '.8f')
    elif p >= 0:
        if not for_trade:
            return floor(_val * (10 ** p)) / (10 ** p)
        else:
            return format(floor(_val * (10 ** p)) / (10 ** p), f'.{p}f')
    else:
        if not for_trade:
            return floor(_val / (10 ** p)) * (10 ** p)
        else:
            return str(floor(_val / (10 ** p)) * (10 ** p))


def move_liquidity(usd, amount):
    global nb
    update_balance()
    amount_to_get = toNum(amount * 1.1 - dico_balance[usd], 0)
    for Kusd in dico_dollar[usd].keys():

        if dico_balance[Kusd] > 11:
            if not amount_to_get > 10:
                amount_to_get = toNum(11, 0)
            if dico_balance[Kusd] >= amount_to_get:
                if not dico_dollar[usd][Kusd]:
                    client.order_market_buy(symbol=usd + Kusd, quantity=amount_to_get)
                else:
                    client.order_market_sell(symbol=Kusd + usd, quantity=amount_to_get)
                update_balance()
                return True

            else:
                amount_to_get -= toNum(dico_balance[Kusd], 0)
                if not dico_dollar[usd][Kusd]:
                    client.order_market_buy(symbol=usd + Kusd, quantity=toNum(dico_balance[Kusd], 0))
                else:
                    client.order_market_sell(symbol=Kusd + usd, quantity=toNum(dico_balance[Kusd], 0))
                update_balance()

    return False


#  {'TUSD': {'BTC': {'b': 40576.93, 'B': 0.12317, 'a': 40605.32, 'A': 0.1232, 'min_val': 5.0}
#  {'amount': 100.01526211,
#  'usd': 'BUSD',
#  'token1': 'APE',
#  'token2': 'BTC',
#  'usdOut': 'BUSD',
#  'min_val_usd_token1': 2.0,
#  'min_val_token1_token2': 2,
#  'min_val_token2_usd': 5}
def trade(pos):
    global nb_, total_earn, dico_err, OrderBookUSD, OrderBookToken, def_max_asset

    assets = dico_balance[pos['usd']]
    # assets = 100
    # assets = 100
    # assets = float(client.get_asset_balance(asset=(pos['usd']))['free'])
    """if assets < 15:
        if pos['usd'] not in dico_err['balance'].keys():
            dico_err['balance'][pos['usd']] = 1
        else:
            dico_err['balance'][pos['usd']] += 1
        # print(f'OUT : balance to low ({assets}, {pos['usd']})')
        return False"""
    l_in = float(OrderBookUSD[pos['usd']][pos['token1']]['A'])  # BTC
    price_in = float(OrderBookUSD[pos['usd']][pos['token1']]['a'])

    price_out = float(OrderBookUSD[pos['usdOut']][pos['token2']]['b'])
    l_out = price_out * float(OrderBookUSD[pos['usdOut']][pos['token2']]['B'])  # USD

    if pos['token1'] in OrderBookToken and pos['token2'] in OrderBookToken[pos['token1']]:
        price_middle = float(OrderBookToken[pos['token1']][pos['token2']]['b'])
        inverse_pair = True
        l_middle = float(OrderBookToken[pos['token1']][pos['token2']]['B'])
    else:
        price_middle = float(OrderBookToken[pos['token2']][pos['token1']]['a'])
        inverse_pair = False
        l_middle = float(OrderBookToken[pos['token2']][pos['token1']]['A'])

    if not inverse_pair:
        l_middle = price_middle * l_middle

    # calc dollar liquidity
    if l_in < l_middle:
        min_liquidity = l_in * price_in
    else:
        min_liquidity = l_middle * price_in
    if min_liquidity > l_out:
        min_liquidity = l_out
    if min_liquidity <= 500:  # choisit arbitrairement
        # print('OUT : liquidity to low', min_liquidity)
        dico_err['low_liquidity'] += 1
        return False
    else:
        if assets >= min_liquidity * 0.7:
            assets = toNum(min_liquidity * 0.7)
        else:
            assets = toNum(assets * 0.9)
        # print('min_liquidity', min_liquidity)
    # print('asset f', assets)

    # #nb_token_m1 = toNum(assets / price_in, pos['min_val_usd_token1'])
    # assets = toNum(nb_token_m1 * price_in)
    # nb_token_m1 = toNum(assets / price_in, pos['min_val_usd_token1'])

    # -- -- -- --
    pos_available = False
    nb_max_token_in = int(toNum(def_max_asset / price_in, pos['min_val_usd_token1']) * 10 ** pos['min_val_usd_token1'])

    lst_in_usd = []
    if inverse_pair:
        min_val_t2 = pos['min_val_token2_usd']  # prend la val min pour le token2 pour calc le out
    else:  # pour not inverse pair
        if pos['min_val_token2_usd'] < pos['min_val_token1_token2']:
            min_val_t2 = pos['min_val_token2_usd']
        else:
            min_val_t2 = pos['min_val_token1_token2']

    for nb in (1, nb_max_token_in, 1):
        temp_m1 = toNum(nb * min_pos(pos['min_val_usd_token1']))
        temp_asset = toNum(temp_m1 * price_in)
        if inverse_pair:
            temp_m2 = toNum(temp_m1 * price_middle, min_val_t2)
        else:
            temp_m2 = toNum(temp_m1 / price_middle, min_val_t2)

        temp_asset_out = toNum(temp_m2 * price_out)

        if temp_asset < temp_asset_out and temp_asset < def_max_asset and temp_asset < min_liquidity:
            lst_in_usd.append([temp_asset, temp_m1, temp_m2, temp_asset_out])
            pos_available = True

    # print('--')
    # print('price_in', price_in, 'price_middle', price_middle, 'price_out', price_out)
    # print('price eth', price_in - p/100, 'amount eth', round(i * min_val_t1, 8), 'btc',
    #      round(i * min_val_t1 * price_mid, 10), 'usd', round(i * min_val_t1 * price_mid * price_out, 8))
    # elif round(i * min_pos(pos['min_val_usd_token1']) * price_middle * price_out, 8)>100:
    # nb_token_m1 = toNum(nb_token_m1, 8)
    # assets = toNum(nb_token_m1 * price_in, 8)

    if not pos_available:
        dico_err['not_pile'] += 1
        return False
    assets = lst_in_usd[0][0]
    nb_token_m1 = lst_in_usd[0][1]
    nb_token_m2 = lst_in_usd[0][2]
    result = lst_in_usd[0][3]

    # print('asset', assets, 'm1', nb_token_m1, 'm2', nb_token_m2, 'result', result, 'pos', pos)
    # print('false:', end=' ')
    if result - assets <= 0.005:
        dico_err['result'] += 1
        # print(f"assets : {pos['usd']} : {round(assets, 8)} : liquidity minimum, {round(min_liquidity, 3)} : estimate earning {round(result - assets, 8)}")
        return False

    if result - assets >= 0.0751 * result / 100:
        if dico_balance[pos['usd']] < assets:
            if not move_liquidity(pos['usd'], assets * 1.1):
                if pos['usd'] not in dico_err['balance'].keys():
                    dico_err['balance'][pos['usd']] = 1
                else:
                    dico_err['balance'][pos['usd']] += 1
                return False
            else:
                nb_ += 1
                # result -= 0.075

    elif result - assets < 0.0751 * result / 100:
        if assets < 15:
            dico_err['result'] += 1
            # print(f"assets : {pos['usd']} : {round(assets, 8)} : liquidity minimum, {round(min_liquidity, 3)} : estimate earning {round(result - assets, 8)}")
            return False
    if dico_balance[pos['usd']] < assets:
        if pos['usd'] not in dico_err['balance'].keys():
            dico_err['balance'][pos['usd']] = 1
        else:
            dico_err['balance'][pos['usd']] += 1
        return False
    # print(f"assets/result : {pos['usd']}: {assets}/{result}\nliquidity minimum {min_liquidity}\nestimate earning {result - assets}")

    # ordre buy order
    s = pos['token1'] + pos['usd']
    qty = nb_token_m1
    # print('1:buy', s, qty)
    client.order_market_buy(symbol=s, quantity=qty)
    qty_in = qty
    # sleep(0.001)
    update_balance()
    balance = dico_balance[pos['token1']]
    # while balance < 0.95 * qty:
    #    print('wait', pos['token1'], balance)
    #    sleep(0.0101)
    #    balance = float(client.get_asset_balance(asset=pos['token1'])['free'])
    if inverse_pair:
        # print('pair', pos['token1'] + pos['token2'], end=' ')
        qty = toNum(balance, pos['min_val_token1_token2'], True)
        # print('2:sell', qty)
        client.order_market_sell(symbol=pos['token1'] + pos['token2'], quantity=qty)
        qty_mid = qty
    else:
        # print('pair', pos['token2'] + pos['token1'], end=' ')
        # price_middle = float(client.get_(symbol=pos['token2'] + pos['token1'])['askPrice'])
        price_middle = dico_tickers[pos['token2'] + pos['token1']['a']]
        qty = toNum(balance / price_middle, min_val_t2, True)
        # ('2:buy', qty)
        client.order_market_buy(symbol=pos['token2'] + pos['token1'], quantity=qty, price=price_middle)
        qty_mid = qty

    # sleep(0.05)
    update_balance()
    balance = dico_balance[pos['token2']]
    balance_out = dico_balance[pos['usdOut']]
    # while balance < 0.95 * qty:
    #    print('wait2', s, balance)
    #    sleep(0.101)
    #    balance = float(client.get_asset_balance(asset=s)['free'])
    # sleep(0.05)
    qty = toNum(balance, pos['min_val_token2_usd'], True)
    # print('3:sell', qty)
    final_pos = client.order_market_sell(symbol=pos['token2'] + pos['usdOut'], quantity=qty)
    # print('earning', float(final_pos['cummulativeQuoteQty']) - assets)

    # total_earn += float(final_pos['cummulativeQuoteQty']) - assets
    update_balance()
    nb_ += 1
    total_earn += float(dico_balance[pos['usdOut']]) - assets
    # total_earn += result - assets
    print('COMPLETE')
    with open('log.txt', 'a') as fic:
        fic.write(f";asset:{assets}:m1:{nb_token_m1}:m2:{nb_token_m2}:result:{result}:pos:{pos}:price_in:{price_in}:price_middle:{price_middle}:price_out:{price_out}assets/result:{pos['usd']}:{assets}/{result}:liquidity minimum:{min_liquidity}:estimate earning:{result - assets}:qty_in:{qty_in}:qty_mid:{qty_mid}:qty_out{qty}")
    # sleep(999999999999999999)
    # -- -- -- --
    """
    actual_balance = client.get_asset_balance(asset=pos['usdOut'])['free']
    if final_pos['cummulativeQuoteQty'] - assets > actual_balance * 0.0750 / 100:
        print('estimate earning after replace liquidity: ',
              final_pos['cummulativeQuoteQty'] - assets - actual_balance * 0.0750 / 100)
        position = get_best_out(pos['usdOut'], actual_balance)

        if position[1]:
            print('pair', pos['usdOut'] + position[0])
            qty = round(balance, dico_all_symbol_min_val[pos['usdOut'] + position[0]])
            print('2:buy', qty)
            client.order_market_sell(symbol=pos['usdOut'] + position[0],
                                     quantity=qty)
        else:
            print('pair', position[0] + pos['usdOut'])
            for i in client.get_orderbook_ticker s():
                if i['symbol'] == position[0] + pos['usdOut']:
                    balance = balance / i['askPrice']
            qty = round(balance, dico_all_symbol_min_val[position[0] + pos['usdOut']])
            print('2:sell', qty)
            client.order_market_buy(symbol=position[0] + pos['usdOut'],
                                    quantity=qty)
        print('earning after replace liquidity: ', float(client.get_asset_balance(asset=pos[0])['free']))"""
    return True


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
                   'NGN', 'BIDR', 'PAX', 'SUSD']:
            if i2 in _nouv:
                _nouv = ''
        if _nouv != '' and len(_nouv) > 1:
            if _nouv not in lst_symbol:
                lst_symbol.append(_nouv)
            _nouv = ''

    return lst_symbol


# liste des usd compatible avec un token
def get_tickers_usd(_name, ticker=None):
    global dico_tickers
    _nouv = ''
    lst_symbol = []
    if ticker is None:
        lst_usd = ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD']
    else:
        lst_usd = ticker
    for keys in list(dico_tickers.keys()):
        if _name in keys:
            if keys[:len(_name)] == _name:
                _nouv = keys.replace(_name, '')
                for i2 in lst_usd:
                    if i2 == _nouv:
                        if _nouv != '' and len(_nouv) > 2:
                            if _nouv not in lst_symbol:
                                lst_symbol.append(_nouv)
        _nouv = ''
    return lst_symbol


"""
def get_best_out(_name, liquidity_out):
    global dico_tickers
    lst = []
    for i in get_tickers_usd_for_usd(_name):
        if not i[1]:
            f = 100 / dico_tickers[_name + i[0]]['askPrice']
            q = dico_tickers[_name + i[0]]['askQty']
            lst.append([f, q, i[1], dico_tickers[_name + i[0]]['symbol']])
        else:
            f = 100 * (dico_tickers[i[0] + _name[0]]['b'])
            q = dico_tickers[i[0] + _name[0]]['bidQty']
            lst.append([f, q, i[1], dico_tickers[_name + i[0]]['symbol']])

    lst = sorted(lst, key=lambda x: x[0], reverse=True)
    for i in lst:
        if i[1] > liquidity_out:
            return [i[3], i[2]]


# return [nb_token, inverse_or_not]


# [other_usd, inverse
def get_tickers_usd_for_usd(_name):
    _nouv = ''
    lst_symbol = []
    for i in tickers:
        if _name in i['symbol']:
            if i['symbol'][:len(_name)] == _name:
                _nouv = i['symbol'].replace(_name, '')
                for i2 in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD', 'SUSD']:
                    if i2 == _nouv:
                        if _nouv != '' and len(_nouv) > 2:
                            if _nouv not in lst_symbol:
                                lst_symbol.append([_nouv, False])

            elif i['symbol'][len(_name):] == _name:
                _nouv = i['symbol'].replace(_name, '')
                for i2 in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD', 'SUSD']:
                    if i2 == _nouv:
                        if _nouv != '' and len(_nouv) > 2:
                            if _nouv not in lst_symbol:
                                lst_symbol.append([_nouv, True])
        _nouv = ''
    return lst_symbol

"""


def get_other_token(_name):
    global dico_tickers
    _nouv = ''
    lst_symbol = []
    for keys in dico_tickers.keys():
        if _name in keys:
            if keys == 'RENBTC':
                if _nouv not in lst_symbol:
                    lst_symbol.append(_nouv)
            else:
                if 'W' + _name in keys:
                    _nouv = keys.replace(('W' + _name), '')
                else:
                    _nouv = keys.replace(_name, '')
                for i2 in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD', 'EUR', 'GBP', 'AUD', 'BRL', 'TRY',
                           'KZT', 'HKD', 'PEN', 'RUB', 'UAH', 'UGX', 'PHP', 'USD', 'BKRW', 'NGN', 'BIDR', 'PAX',
                           'SUSD']:
                    if i2 in _nouv:
                        _nouv = ''
                if _nouv != '' and len(_nouv) > 2 and _nouv != _name:
                    if _nouv not in lst_symbol:
                        lst_symbol.append(_nouv)
        _nouv = ''
    return lst_symbol


# t='XRP'
# print(get_token())
# print(get_other_token(t))
# print(get_tickers_usd(t))

# lst_symbol


# if 'USD' not in i['symbol']:
#    lst_pair.append(i['symbol'])
# print(len(lst_pair))
# chaque t
# ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'SUSD']

# {'s': 'ETHBTC', 'bidPrice': '0.06480600', 'bidQty': '3.51640000', 'askPrice': '0.06480700', 'askQty': '3.49380000'}

# def calc_benef(bidPriceBASE, bidQtyBASE, askPriceBASE, askQtyBASE, bidPrice, bidQty, askPrice, askQty, bidPriceBASE2, bidQtyBASE2, askPriceBASE2, askQtyBASE2):
# print(get_arbitrage_possibilit y('XRP'))


def calc_benef():
    global min_earn, nb_
    # bidPriceBASE, askPriceBASE, askPrice, bidPriceBASE2, askPriceBASE2
    # fait abstraction de la liquidité dispo
    buy_part = 100
    # t_ = time()
    lst_pos = []

    for usd in OrderBookUSD.keys():
        for token1 in OrderBookUSD[usd].keys():
            lst_pos.append(
                {'amount': toNum(buy_part / float(OrderBookUSD[usd][token1]['a'])),
                 'usd': usd,
                 'token1': token1,
                 'min_val_usd_token1': OrderBookUSD[usd][token1]['min_val'],
                 'min_val_token1_token2': 0,
                 'min_val_token2_usd': 0,
                 'token2': '',
                 'usdOut': ''})
    new_lst_pos = []
    for i in range(len(lst_pos)):
        # token1 pos['token1']
        for token2 in OrderBookToken[lst_pos[i]['token1']].keys():
            new_lst_pos.append(
                {'amount': toNum(lst_pos[i]['amount'] * float(OrderBookToken[lst_pos[i]['token1']][token2]['b'])),
                 'usd': lst_pos[i]['usd'],
                 'token1': lst_pos[i]['token1'],
                 'min_val_usd_token1': lst_pos[i]['min_val_usd_token1'],
                 'min_val_token1_token2': OrderBookToken[lst_pos[i]['token1']][token2]['min_val'],
                 'min_val_token2_usd': 0,
                 'token2': token2,
                 'usdOut': ''})

    lst_pos = new_lst_pos
    new_lst_pos = []
    for i in range(len(lst_pos)):
        # token1 pos['token1'] n
        for usd in InverseOrderBookUSD[lst_pos[i]['token2']]:
            new_lst_pos.append(
                {'amount': (toNum(
                    lst_pos[i]['amount'] * float(OrderBookUSD[usd][lst_pos[i]['token2']]['b'])) - (3 * 0.075 / 100 *
                                                                                                   toNum(lst_pos[i][
                                                                                                             'amount'] * float(
                                                                                                       OrderBookUSD[
                                                                                                           usd][
                                                                                                           lst_pos[i][
                                                                                                               'token2']][
                                                                                                           'b'])))),
                 'usd': lst_pos[i]['usd'],
                 'token1': lst_pos[i]['token1'],
                 'token2': lst_pos[i]['token2'],
                 'usdOut': usd,
                 'min_val_usd_token1': int(lst_pos[i]['min_val_usd_token1']),
                 'min_val_token1_token2': int(lst_pos[i]['min_val_token1_token2']),
                 'min_val_token2_usd': int(OrderBookUSD[usd][lst_pos[i]['token2']]['min_val'])})

    lst_pos = []
    # can be optimized
    for pos in new_lst_pos:
        if pos['amount'] > buy_part:
            lst_pos.append(pos)
    # lst_pos = sorted(lst_pos, key=lambda x: x['amount'], reverse=True)
    # print('time execution', round((time() - t_) / 60, 8))
    # print('nombre de position', len(lst_pos))
    # print('lst position', lst_pos, '\n', '--' * 50)

    # if cpt != 0:
    #    print('\nopportunity', cpt, end='')
    # f = 100 / askPriceBASE / askPrice * bidPriceBASE2
    # f2 = 100 / askPriceBASE2 / askPrice * bidPriceBASE

    return lst_pos

    # in_dollar = askPriceBASE*askQtyBASE
    # out_dollar = askPriceBASE2*askQtyBASE2
    # middle_dollar = ask
    # if askQty*askPriceBASE<askQty/askPrice*askPriceBASE2:
    #    m_dollar = askQty*askPriceBASE
    # else:
    #    m_dollar = askQty/askPrice*askPriceBASE2
    # if m_dollar < in_dollar and m_dollar < out_dollar:
    #
    # elif in_dollar<out_dollar:
    #    base_in = in_dollar
    #    base_out = (base_in/askPriceBASE/askPrice)*askPriceBASE2
    # else:
    #    base_in = out_dollar
    #    base_out = (base_in / askPriceBASE / askPrice) * askPriceBASE2
    # return base_in, base_out-base_in, base_out*100/base_in


def main():
    global nb_
    temp_nb = nb_
    out = calc_benef()
    print('nb out ', len(out))

    if out:
        for i in range(len(out)):
            if nb_ - temp_nb > 0:
                sleep(1.5)
            if trade(out[i]):
                update_balance()
        return out
    return


# VEN', 'NULS', 'VET', 'BCHSV', 'BNC', 'LINK', 'WAVES', 'BTT', 'ONG', 'HOT', 'ZIL', 'ZRX',
with open('lst_token.txt', 'r') as f:
    lst_token = str(f.readline()).split(',')


# shuffle(lst_token)


def launch_scan_trade():
    global dico_err, nb_

    # print('Start')
    # time_start = time()
    # cpt = 0
    # for i in lst_token:
    main()

    """if re:
            # print('\n', re)
            for data in re:
                if trade(data):
                    update_balance()
                    cpt += 1
                if cpt > 2:
                    break
        if cpt > 2:
            break"""
    # else:
    #    print(".", end='')
    clearConsole()
    print("nb d'opportunité saisi", nb_, 'list_dico_err ', dico_err)
    # print('time:', asctime())
    print('total earn', total_earn, 'rentabilité (estimé)', round(total_earn / ((time() - t_start) / 3600), 8), '$/hour',
          round(total_earn / ((time() - t_start) / 86400), 8), '$/day',
          round(total_earn / ((time() - t_start) / (86400 * 30)), 8), '$/mounth', 'temps de fonctionnement', round((time() - t_start) / 3600, 3), 'h')
    print('--' * 10)


def on_close(ws):
    print('disconnected from server at:', asctime())


def on_open(ws):
    print('connection established at:', asctime())


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
            # if json_m['s'] == 'ETHBTC':
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

    # sleep(0.001)


"""
def on_message(ws, message):
    global dico_tickers
    # print('received message')
    json_m = json.loads(message)
    del json_m['u']
    if json_m['s'] in dico_tickers.keys() and dico_tickers[json_m['s']] != json_m:
        dico_tickers[json_m['s']] = json_m
    # sleep(0.001)"""


class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global dico_err
        sleep(5)
        while True:
            launch_scan_trade()
            # print('erreur', dico_err)
            # print('wait')
            dico_err = {'balance': {}, 'low_liquidity': 0, 'result': 0, 'not_pile': 0}
            # update_balance()


if __name__ == "__main__":

    SOCKET = "wss://stream.binance.com:9443/ws/!bookTicker"

    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

    dico_balance = {}
    total_earn = 0
    dico_dollar = get_dollar_path()
    nb_ = 0

    """

    deux choix:

    soit on essaye de faire plein de trade à faible rendement

    soit ont attendants des des gros coef

    """
    min_earn = 1.001
    dico_tickers = init_dico()
    all_lst_usd = ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD']
    lst_usd = ['DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD']
    # lst_usd = ['USDT', 'UST', 'BUSD']
    # lst_usd = ['TUSD', 'USDT', 'UST', 'BUSD']
    # lst_usd = ['BUSD', 'USDT', 'TUSD']

    dico_err = {'balance': {}, 'low_liquidity': 0, 'result': 0, 'not_pile': 0}

    print('Orderbook load . . .')
    OrderBookUSD, InverseOrderBookUSD = initOrderBookUSD()
    OrderBookToken = initOrderBookToken()
    # print('orderUSD', OrderBookUSD)
    # print('order', OrderBookToken)
    # print('order', OrderBookToken['ETH'])
    # print('InverseOrderBookUSD', InverseOrderBookUSD)
    # print('orderToken', OrderBookToken)
    sleep(2)
    # launch_scan_trade()
    t_start = time()
    print('def your max amount asset:\n')
    def_max_asset = toNum(float(input('Amount: ')), 1)

    sleep(1)

    update_balance()

    print('-- -- -- -- -- -- -- -- -- --')
    print('lancement du websocket')
    print('-- -- -- -- -- -- -- -- -- --')
    print('bonne chance')
    sleep(2)
    clearConsole()
    thread = Server()
    thread.start()
    while True:
        try:
            ws.run_forever()
        except Exception as err:
            print('erreur:', err)
            sleep(2)
            client = Client(api_key, api_secret, {"timeout": 20})
            update_balance()
            OrderBookUSD, InverseOrderBookUSD = initOrderBookUSD()
            OrderBookToken = initOrderBookToken()
            sleep(2)
            print('fin erreur')
            pass
        sleep(2)
