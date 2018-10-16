import pandas as pd 
import numpy as np 
import requests
import time
import json
import time
import datetime
import urllib

chat = 


TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def main():
    text, id = get_last_chat_id_and_text(get_updates())

    if text == 'help':
        msg = 'Hello there !!\n This is a demo Bot to consult and request some crypto prices. \n\n'
        msg = msg + 'You only have to type the name of the cryptocurrencie you would like to know the last price and I will send it to you :D'
        msg = msg + 'Please type when you want ...'
        send_message(msg, chat)

    if text == 'btc':
        btc_price = binance_last_price('BTCUSDT')
        msg = 'The BTC/USDT last price is: ' + str(btc_price)
        send_message(msg, chat)
    if text == 'eth':
        eth_price = binance_last_price('ETHUSDT')
        msg = 'The ETH/USDT last price is: ' + str(eth_price)
        send_message(msg, chat)
    else:
        msg = "Sorry, I don't know that you are looking for. \n Try again ..."
        send_message(msg, chat)
    time.sleep(10)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)



def binance_last_price(symbol): 
    try: 
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
        # Get tick by tick data of last price from Binance
        binanceTick = requests.get('https://api.binance.com/api/v3/ticker/price?symbol='+symbol)
        return float(binanceTick.json()['price'])
    except:
        return 0

if __name__ == '__main__':
    msg = '\n' + 'Hello !!!!' + "\n"

    print(msg)
    print(URL)
    print(get_last_chat_id_and_text(get_updates()))
    #send_message(msg, chat)

    main()
