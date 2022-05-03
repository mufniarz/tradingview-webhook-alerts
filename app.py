import requests, json
from chalice import Chalice

app = Chalice(app_name='tradingview-webhook-alerts')

API_KEY = 'PKKQEID7EDZ8SDVUFWSH'
SECRET_KEY = '5SwqCDGQ631JDFAqCJHfR3rvw06zm6wYCxER2Vkn'
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

qty = 1000

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    request = app.current_request
    webhook_message = request.json_body
    print('request')
    print(request)
    print('webhook_message')
    print(webhook_message)

    data = {
        "symbol": webhook_message['ticker'],
        "qty": qty,
        "side": "buy",
        "type": "market",
        # "limit_price": webhook_message['close'],
        # "time_in_force": "gtc",
        # "order_class": "bracket",
        # "take_profit": {
        #     "limit_price": webhook_message['close'] * 1.05
        # },
        # "stop_loss": {
        #     "stop_price": webhook_message['close'] * 0.98,
        # }
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content) 
    print(response)

    return {
        'webhook_message': webhook_message,
        'id': response['id'],
        'client_order_id': response['client_order_id']
    }

@app.route('/sell_stock', methods=['POST'])
def sell_stock():
    request = app.current_request
    webhook_message = request.json_body
    print('request')
    print(request)
    print('webhook_message')
    print(webhook_message)
    data = {
        "symbol": webhook_message['ticker'],
        "qty": qty,
        "side": "sell",
        "type": "market",
        # "limit_price": webhook_message['close'],
        # "time_in_force": "gtc",
        # "order_class": "bracket",
        # "take_profit": {
        #     "limit_price": webhook_message['close'] * 1.05
        # },
        # "stop_loss": {
        #     "stop_price": webhook_message['close'] * 0.98,
        # }
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content) 
    print(response)

    return {
        'webhook_message': webhook_message,
        'id': response['id'],
        'client_order_id': response['client_order_id']
    }

@app.route('/short_sell_stock', methods=['POST'])
def short_sell_stock():
    request = app.current_request
    webhook_message = request.json_body
    print('request')
    print(request)
    print('webhook_message')
    print(webhook_message)
    data = {
        "symbol": webhook_message['ticker'],
        "qty": qty,
        "side": "buy",
        "type": "market",
        # "limit_price": webhook_message['close'],
        # "time_in_force": "gtc",
        # "order_class": "bracket",
        # "take_profit": {
        #     "limit_price": webhook_message['close'] * 1.05
        # },
        # "stop_loss": {
        #     "stop_price": webhook_message['close'] * 0.98,
        # }
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content) 
    print(response)

    return {
        'webhook_message': webhook_message,
        'id': response['id'],
        'client_order_id': response['client_order_id']
    }

@app.route('/short_buy_stock', methods=['POST'])
def short_buy_stock():
    request = app.current_request
    webhook_message = request.json_body
    print('request')
    print(request)
    print('webhook_message')
    print(webhook_message)
    data = {
        "symbol": webhook_message['ticker'],
        "qty": qty,
        "side": "sell",
        "type": "market",
        # "limit_price": webhook_message['close'],
        # "time_in_force": "gtc",
        # "order_class": "bracket",
        # "take_profit": {
        #     "limit_price": webhook_message['close'] * 1.05
        # },
        # "stop_loss": {
        #     "stop_price": webhook_message['close'] * 0.98,
        # }
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content) 
    print(response)

    return {
        'webhook_message': webhook_message,
        'id': response['id'],
        'client_order_id': response['client_order_id']
    }
