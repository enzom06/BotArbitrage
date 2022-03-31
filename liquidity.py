from binance.client import Client

from time import sleep, time

# from trade import trade

with open('keys.txt', 'r') as file:
    api_key, api_secret = str(file.readline()).split(',')
client = Client(api_key, api_secret, {"timeout": 20})


# print(client.futures_create_order(symbol='MKRUSDT', quantity=str(0.001), side='BUY',
#                            type='MARKET'))
# print(client.futures_create_order(symbol='MKRUSDT', quantity=str(0.001), side='SELL',
#                            type='MARKET'))

def get_min_val():
    dico = {}
    for i in client.get_exchange_info()['symbols']:
        min_step = i['filters'][2]['minQty']
        nb = min_step.find('1')
        if nb == 0:
            dico[i['symbol']] = 0
        elif nb < 0:
            nb = len(str(int(min_step)))
            dico[i['symbol']] = nb
        elif nb > 0:
            dico[i['symbol']] = nb - 1
    return dico


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


# liste des usd compatible avec un token
def get_tickers_usd(_name, t=True):
    _nouv = ''
    lst_symbol = []
    lst_usd = []
    if not t:
        lst_usd = ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD']
    else:
        lst_usd = ['USDT']
    for i in tickers:
        if _name in i['symbol']:
            if i['symbol'][:len(_name)] == _name:
                _nouv = i['symbol'].replace(_name, '')
                for i2 in lst_usd:
                    if i2 == _nouv:
                        if _nouv != '' and len(_nouv) > 2:
                            if _nouv not in lst_symbol:
                                lst_symbol.append(_nouv)
        _nouv = ''
    return lst_symbol

def get_other_token(_name):
    _nouv = ''
    lst_symbol = []
    for i in tickers:
        if _name in i['symbol']:
            if i['symbol'] == 'RENBTC':
                if _nouv not in lst_symbol:
                    lst_symbol.append(_nouv)
            else:
                if 'W' + _name in i['symbol']:
                    _nouv = i['symbol'].replace(('W' + _name), '')
                else:
                    _nouv = i['symbol'].replace(_name, '')
                for i2 in ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST', 'BUSD', 'EUR', 'GBP', 'AUD', 'BRL', 'TRY',
                           'KZT', 'HKD', 'PEN', 'RUB', 'UAH', 'UGX', 'PHP', 'USD', 'BKRW', 'NGN', 'BIDR', 'PAX']:
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

def get_arbitrage_possibility(_token):
    global dico_tickers
    usd_token = get_tickers_usd(_token, False)
    usd_token_rate = []
    # i
    for i in usd_token:
        usd_token_rate.append([dico_tickers[_token + i]['askPrice'], dico_tickers[_token + i]['askQty'], i])
    # ------------------------------------------------------------------------------------------------------------------
    tokens = get_other_token(_token)
    token_token_rate = []
    dico_tokens_usd_rate = {}
    # ------------------------------------------------------------------------------------------------------------------
    for token in tokens:
        t = _token + token  # BTC/ETH
        if t in dico_tickers:
            token_token_rate.append(
                [dico_tickers[t]['bidPrice'], dico_tickers[t]['bidQty'], token,
                 False])

        t = token + _token  # ETH/BTC
        # i2
        if t in dico_tickers:
            token_token_rate.append(
                [dico_tickers[t]['askPrice'], dico_tickers[t]['askQty'], token,
                 True])
        # Can check btc in reverse pair

        # --------------------------------------------------------------------------------------------------------------
        _usds = get_tickers_usd(token, False)
        tokens_usd_rate = {}
        for u in _usds:
            tokens_usd_rate[u] = [dico_tickers[token + u]['bidPrice'], dico_tickers[token + u]['bidQty']]

        dico_tokens_usd_rate[token] = tokens_usd_rate

    return usd_token_rate, token_token_rate, dico_tokens_usd_rate


# lst_symbol


# if 'USD' not in i['symbol']:
#    lst_pair.append(i['symbol'])
# print(len(lst_pair))
# chaque t
# ['TUSD', 'DAI', 'USDC', 'USDT', 'USDP', 'UST']

# {'symbol': 'ETHBTC', 'bidPrice': '0.06480600', 'bidQty': '3.51640000', 'askPrice': '0.06480700', 'askQty': '3.49380000'}

# def calc_benef(bidPriceBASE, bidQtyBASE, askPriceBASE, askQtyBASE, bidPrice, bidQty, askPrice, askQty, bidPriceBASE2, bidQtyBASE2, askPriceBASE2, askQtyBASE2):
# print(get_arbitrage_possibility('XRP'))
def calc_benef(_token_name, lst_usd, lst_token_tokens, lst_out):
    # bidPriceBASE, askPriceBASE, askPrice, bidPriceBASE2, askPriceBASE2
    # fait abstraction de la liquidité dispo
    buy_part = 100
    lst_entry = []
    lst_result = []

    """

    pour chaque token prendre la liquidité diponible est trouver combien je peux mettre en buy_part

    """
    cpt = 0
    for i in lst_usd:
        if float(i[0]) != 0 and float(i[1]) != 0:
            lst_entry.append([buy_part / float(i[0]), float(i[0]), float(i[1]), i[-1]])

    for i in lst_entry:
        for i2 in lst_token_tokens:
            """print('in')
            print(lst_usd[cpt])
            print(i)
            print(i2)
            print(lst_out[i2[2]])
            print('out')"""
            # print(i[-1], lst_out[i2[2]].keys(), lst_out[i2[2]])
            # check if usd out = usd in and !=0
            if float(i2[0]) > 0:
                for key in lst_out[i2[2]].keys():
                    if key in lst_out[i2[2]] and float(lst_out[i2[2]][key][0]) > 0:
                        # for USD in lst_out[i2[2]]:
                        if i2[-1]:
                            result = float(i[0]) / float(i2[0]) * float(lst_out[i2[2]][key][0]) - (
                                    buy_part * 0.0751 / 100) * 3
                        else:
                            result = float(i[0]) * float(i2[0]) * float(lst_out[i2[2]][key][0]) - (
                                    buy_part * 0.0751 / 100) * 3
                        # print('result', result)
                        if result > buy_part * 1.000:
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
                            if i2[-1]:
                                liquidity2 = float(i2[0]) * float(i2[1])
                            else:
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
                            lst_result.append([round(result, 4), main_liquidity, i[-1], _token_name, i2[2], key])
        cpt += 1
    # f = 100 / askPriceBASE / askPrice * bidPriceBASE2
    # f2 = 100 / askPriceBASE2 / askPrice * bidPriceBASE

    return lst_result

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


def main(_name):
    global token
    global tickers
    global dico_tickers
    token = _name
    tickers = client.get_orderbook_tickers()
    dico_tickers = {}
    # lst_pair = []
    # print(tickers)
    # print(tickers[0])
    for i in range(len(tickers)):
        if 'BEAR' in tickers[i]['symbol'] or 'BULL' in tickers[i]['symbol'] or 'DOWN' in tickers[i]['symbol'] or 'UP' in \
                tickers[i]['symbol'] or 'BNB' in tickers[i]['symbol']:
            tickers[i] = {'symbol': ''}
        else:
            dico_tickers[tickers[i]['symbol']] = tickers[i]

    save_data = get_arbitrage_possibility(token)
    # print(usd_token_rate)
    # print(token_token_rate)
    # print(dico_tokens_usd_rate)
    out = calc_benef(token, save_data[0], save_data[1], save_data[2])
    best = [0]
    for pos in out:
        if pos[0] > best[0] and pos[1] > 20:
            best = pos
    if best != [0]:
        return best, out
    return None


# VEN', 'NULS', 'VET', 'BCHSV', 'BNC', 'LINK', 'WAVES', 'BTT', 'ONG', 'HOT', 'ZIL', 'ZRX',

with open('lst_token.txt', 'r') as f:
    lst_token = str(f.readline()).split(',')

# print(get_token())

print(lst_token)
final_return = []
print('Start')
t_start = time()
for i in lst_token:
    re = main(i)
    if re:
        print('\n', time() - t_start, re)
    else:
        print('.', end='')
print('\ntemps: ', round(time() - t_start, 3), 'S ')


#print(client.get_exchange_info())
#print(len('0.1000'.split('.')[0]))
