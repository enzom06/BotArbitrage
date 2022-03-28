# l = [{"key": 1}, {"key": 5}]
# l = sorted(l, key=lambda x: x['key'], reverse=True)

# print('l', l)


from binance.client import Client
from time import sleep, time, asctime
from math import floor
from threading import Thread

import websocket, json, os

# print('key1' in dico and 'key2' in dico['key1'])

#  'token2': 'BTC',
#  'usdOut': 'BUSD',
#  'min_val_usd_token1': 2.0,
#  'min_val_token1_token2': 2,
#  'min_val_token2_usd': 5}
"""
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
dico_balance = {}
print(client.get_order_book(symbol='ETHBTC'))
"""
"""
#print(client.get_exchange_info()['symbols'])
for i in client.get_orderbook_tickers()['symbols']:
    if 'BUSDUSDT' in i['symbol']:
        print(i)
"""
"""print('azerty'[:len('azert')])"""
"""from math import floor


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

for i in range(1, 8):
    print(toNum(123465 * 10**(-i)))"""

# from random import shuffle
# from trade import trade


"""with open('keys.txt', 'r') as file:
    api_key, api_secret = str(file.readline()).split(',')
client = Client(api_key, api_secret, {"timeout": 20})
dico_balance = {}
"""

"""for p in client.get_exchange_info()['symbols']:
    if p['symbol'] =='ETHBTC' or p['symbol'] == 'BTCUSDT' or p['symbol'] == 'ETHUSDT':
        print(p)
"""

"""
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


def decomp(n):
    L = dict()
    k = 2
    while n != 1:
        exp = 0
        while n % k == 0:
            n = n // k
            exp += 1
        if exp != 0:
            L[k] = exp
        k = k + 1

    return L


def _ppcm(a, b):
    Da = decomp(a)
    Db = decomp(b)
    p = 1
    for facteur, exposant in Da.items():
        if facteur in Db:
            exp = max(exposant, Db[facteur])
        else:
            exp = exposant

        p *= facteur ** exp

    for facteur, exposant in Db.items():
        if facteur not in Da:
            p *= facteur ** exposant

    return p


def ppcm(*args):
    L = list(args)
    if len(L) == 2:
        return _ppcm(L[0], L[1])
    else:
        n = len(L)
        i = 0
        A = []
        while i <= n - 2:
            A.append(_ppcm(L[i], L[i + 1]))
            i += 2
        if n % 2 != 0:
            A.append(L[n - 1])

        return ppcm(*A)
"""

"""
exemple:
ETH -> ETH/BTC -> BTC
"""

"""
def get_min_val(nb):
    min_step = str(nb)
    l = len(min_step.split('.')[1])
    return l
"""
"""
price_in = 2991.75
min_val_t1 = 0.0001
price_out = 42293.04
min_val_t2 = 0.00001
price_mid = floor((price_in / price_out) * 10 ** 6) / 10 ** 6  # ratio"""

"""
AmountMid1 = round((price_in * min_val_t1), 8)
AmountMid2 = round((price_out * min_val_t2), 8)

lenMid = get_min_val(AmountMid1)
lenMid2 = get_min_val(AmountMid2)

#print('len', lenMid)
#print('len2', lenMid2)
AmountMid1 = round(AmountMid1 * 10 ** lenMid)
AmountMid2 = round(AmountMid2 * 10 ** lenMid2)
AmountIn = ppcm(AmountMid1, AmountMid2)# * 10 ** (-lenMid if lenMid > lenMid2 else -lenMid2)

"""
# 10**(-4) mid1 0.0001
# 10**(-4) mid2 0.0001
"""print('min amount for in', min_val_t1)
print('min amount for out 0.00001', min_val_t2)
print('price_mid', price_mid)
print('btc', round(price_mid * min_val_t1, 8), 'usd',
      round(price_mid * min_val_t1 * price_out, 8))  # , round(min_val_t2*price_out, 8), round(min_val_t1*price_in, 8))
s = 0
for p in range(1, 1):
    price_mid = floor(((price_in + (p / 100)) / price_out) * 10 ** 6) / 10 ** 6
    nb = 0
    for i in range(1000, 1, -1):
        if '.' in str(round(i * min_val_t1 * price_mid, 8)) and len(
                str(round(i * min_val_t1 * price_mid, 8)).split('.')[1]) < 6 and round(
                i * min_val_t1 * price_mid * price_out, 8) < 100:
            # nb += 1
            print('nb ', str(round(i * min_val_t1 * price_mid, 8)).split('.')[1], len(str(round(i * min_val_t1 * price_mid, 8)).split('.')[1]))
            print('price eth', price_in - p / 100, 'amount eth', round(i * min_val_t1, 8), 'btc',
                  round(i * min_val_t1 * price_mid, 10), 'usd', round(i * min_val_t1 * price_mid * price_out, 8))
        # elif round(i * min_val_t1 * price_mid * price_out, 8) > 100:
        #    break
    s += nb
    # print('eth', price_in + (p / 100), 'nombre d\'opportunités', nb, 'moyenne', s / p)"""
# print('AmountMid', AmountMid1, 'AmountMid2', AmountMid2)

# print('ppcm', ppcm(AmountMid1, AmountMid2))

# print('invest amount ', round(ppcm(AmountMid1, AmountMid2) * 10 ** (-lenMid if lenMid > lenMid2 else -lenMid2), 8))


"""AmountIn = 20
while AmountIn < 20:
    AmountIn = AmountIn * 2
while AmountIn > 100:
    AmountIn = AmountIn"""

# AmountIn = 100

# AmountOut = min_val_t2*(price_out*10**(get_min_val(min_val_t2)))
# AmountMid = min_val_t2/price_mid
# AmountIn = AmountMid*price_in

# print('in', AmountIn)
# print('middle', AmountMid)
# print('out', AmountOut)
"""AmountMid = toNum(AmountIn / price_in, 8)
AmountMid2 = toNum(AmountMid * price_mid, 8)
AmountOut = toNum(AmountMid2 * price_out, 8)
print('sans restriction')
print(AmountIn, price_in)
print(AmountIn / price_in)
print((AmountIn / price_in) * price_mid)
print('fin')
print("--" * 25)
print('avec restrictions 8')
print('in', AmountIn)
print('mid', AmountMid)
print('mid2', AmountMid2)
print('out', AmountOut)

print("--" * 25)
print('avec toutes les restrictions')
print('in', AmountIn)
eth = floor((AmountIn / price_in) * (10 ** get_min_val(min_val_t1))) / (10 ** get_min_val(min_val_t1))
btc = floor((eth * price_mid) * (10 ** get_min_val(min_val_t2))) / (10 ** get_min_val(min_val_t2))
print('mid')
print(round(eth, 8))
print(round(AmountIn / price_in, 8))
print('mid2')
print(round(btc, 8))
print(round(round(AmountIn / price_in, 8) * price_mid, 8))
print('out', floor((btc * price_out) * (10 ** 8)) / (10 ** 8))
print("--" * 25)

print('delta', AmountOut-floor((btc * price_out) * (10 ** 8)) / (10 ** 8))
"""
# print('result simple', 'in', AmountIn, 'eth', AmountIn/price_in, 'out', AmountIn/price_in*price_in, 'btc', AmountIn/price_out)

"""


Méthode force brute stupide
Ne fonctionne pas

ModAmountMid = floor((AmountIn/price_in) * (10 ** 4)) / (10 ** 4) #restriction normal
ModAmountMid2 = floor((ModAmountMid*price_mid) * (10 ** 4)) / (10 ** 4)
ModAmountOut = floor((ModAmountMid2*price_out) * (10 ** 8)) / (10 ** 8)

for i in range(10):
    ModAmountMid2 = floor((ModAmountOut / price_out) * (10 ** 4)) / (10 ** 4)
    ModAmountMid = floor((ModAmountMid2/price_mid) * (10 ** 4)) / (10 ** 4)
    AmountIn = floor((ModAmountMid*price_in) * (10 ** 8)) / (10 ** 8)

    ModAmountMid = floor((AmountIn/price_in) * (10 ** 4)) / (10 ** 4) #restriction normal
    ModAmountMid2 = floor((ModAmountMid*price_mid) * (10 ** 4)) / (10 ** 4)
    ModAmountOut = floor((ModAmountMid2*price_out) * (10 ** 8)) / (10 ** 8)


AmountMid = AmountIn/price_in
AmountMid2 = AmountMid*price_mid
AmountOut = AmountMid2*price_out

"""
"""

t_ = time()
for i in range(11, 200, 1):
    AmountIn = 11 + i/2
    ModAmountMid = floor((AmountIn/price_in) * (10 ** 4)) / (10 ** 4) #restriction normal
    ModAmountMid2 = floor((ModAmountMid*price_mid) * (10 ** 4)) / (10 ** 4)
    ModAmountOut = floor((ModAmountMid2*price_out) * (10 ** 8)) / (10 ** 8)


    AmountMid = AmountIn/price_in
    AmountMid2 = AmountMid*price_mid
    AmountOut = AmountMid2*price_out

    if AmountOut - ModAmountOut < 0.2:
        print()
        print('Amount_In', AmountIn, '\namount_out', AmountOut, '\nmod_amount_out', ModAmountOut, '\ndelta', AmountOut-ModAmountOut, '\n earn (without restriction)', AmountOut-AmountIn, '\n earn', ModAmountOut-AmountIn)  # , '\n reality earn', ModAmountOut-AmountIn - (AmountOut-ModAmountOut))
"""
"""
print(f"Without decimal restriction\namount_in {AmountIn} $\namount_mid {(AmountMid)}\n amount mid_2 {AmountMid2}\n amount_out {AmountOut}")
print()
print(f"With decimal restriction\namount_in {AmountIn} $\namount_mid {(ModAmountMid)}\n amount mid_2 {ModAmountMid2}\n amount_out {ModAmountOut}")
print()
print('delta', AmountOut-ModAmountOut)"""
"""AmountIn = 100
ModAmountMid = floor((AmountIn / price_in) * (10 ** 4)) / (10 ** 4)  # restriction normal
ModAmountMid2 = floor((ModAmountMid * price_mid) * (10 ** 4)) / (10 ** 4)
ModAmountOut = floor((ModAmountMid2 * price_out) * (10 ** 8)) / (10 ** 8)

AmountMid = AmountIn / price_in
AmountMid2 = AmountMid * price_mid
AmountOut = AmountMid2 * price_out

if AmountOut - ModAmountOut < 0.2:
    print()
    print('Amount_In', AmountIn, '\namount_out', AmountOut, '\nmod_amount_out', ModAmountOut, '\ndelta',
          AmountOut - ModAmountOut, '\n earn (without restriction)', AmountOut - AmountIn, '\n earn',
          ModAmountOut - AmountIn)  # , '\n reality earn', ModAmountOut-AmountIn - (AmountOut-ModAmountOut))"""
"""

chépaquoifaireavecça

num, deno = 2923.79.as_integer_ratio()
num2, deno2 = 0.70984.as_integer_ratio()
num3, deno3 = 41200.0.as_integer_ratio()
print(num, deno)
print(num2, deno2)
print(num3, deno3)"""
"""p_in = price_in*10**(-4) #min que je peux buy
p_mid = 0.70984 * 10**(-4) # min d'ETH que je peut SELL
p_out = 41200.0 * 10**(-4) # min que je peut SELL

ModAmountMid = floor((AmountIn / price_in) * (10 ** 4)) / (10 ** 4)  # restriction normal
ModAmountMid2 = floor((ModAmountMid * price_mid) * (10 ** 4)) / (10 ** 4)
ModAmountOut = floor((ModAmountMid2 * price_out) * (10 ** 8)) / (10 ** 8)

print(p_in, '$')
print(p_mid, '$')
print(p_out, '$')

print('départ', AmountIn)
print('out', AmountIn/price_in*price_mid*price_out)

print('départ', AmountIn)
print('out', ModAmountOut)

print('delta', abs(AmountIn/price_in*price_mid*price_out - ModAmountOut))"""

"""



"""

"""
def min_val():
    min_step = str(0.001)
    nb = int(min_step.find('1'))
    if nb == -1:
        return -9990
    elif nb <= 0:
        l = len(min_step.split('.')[0])
        return l - 1
    elif nb > 0:
        return nb - 1
"""
"""
print('')
print(min_val())
"""
"""
with open('log.txt', 'a') as fic:
    fic.write('b:')
"""



print('LOOMBTC'[3:])
print('LOOMBTC'[:3])




