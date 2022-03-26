import websocket, json
from time import sleep, time

SOCKET = f"wss://stream.binance.com:9443/ws/!bookTicker"


def on_close(ws):
    print('disconnected from server at:', time())


def on_open(ws):
    print('connection established at:', time())


def on_message(ws, message):
    global dico_tickers
    # print('received message')
    json_m = json.loads(message)
    del json_m['u']
    if json_m['s'] in dico_tickers.keys() and dico_tickers[json_m['s']] != json_m:
        dico_tickers[json_m['s']] = json_m

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
