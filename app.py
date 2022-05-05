import requests, json
from chalice import Chalice

app = Chalice(app_name='tradingview-webhook-alerts')

API_KEY = ''
SECRET_KEY = ''
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ASSETS_URL = "{}/v2/assets".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

def accountInfo():
    result = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(result.content)


def setQuantity(account, price):
    return round(.5 * float(account['equity']) / price, None)


@app.route('/buy_long_position', methods=['POST'])
def buy_long_position():
    request = app.current_request
    webhook_message = request.json_body
    # Get Account Information
    account = accountInfo()
    # Determine Quantity
    quantity = setQuantity(account, webhook_message['close'])
    print(quantity)
    # Look For Current Open Postions
    result = requests.get(POSITIONS_URL, headers=HEADERS)
    positions = json.loads(result.content)
    print(positions)
    for position in positions:
        if position['symbol'] == webhook_message['ticker']:
            print(position['symbol'])
            print(position['qty'])
            pos_qty = int(position['qty'])
            if pos_qty < 1:
                quantity = abs(pos_qty) + quantity 
                print(quantity)
            else:
                quantity = 0
    # Build Order JSON
    if quantity != 0:
        data = {
            "symbol": webhook_message['ticker'],
            "qty": quantity,
            "side": "buy",
            "type": "market",
            # "limit_price": webhook_message['close'],
            "time_in_force": "fok",
            # "order_class": "bracket",
            # "take_profit": {
            #     "limit_price": round(webhook_message['close'] * 1.005, 2)
            # },
            # "stop_loss": {
            #     "stop_price": round(webhook_message['close'] * 0.995, 2),
            # }
        }
        # Post Order to Alpaca
        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
        response = json.loads(r.content) 
        # print(response.keys())
        # if response['code'] and response['message']:
        #     print(response['code'])
        #     print(response['message'])
        # Return Response
        return {
            'webhook_message': webhook_message,
            'id': response['id'],
            'client_order_id': response['client_order_id']
        }

@app.route('/sell_long_position', methods=['POST'])
def sell_long_position():
    quantity = 0
    request = app.current_request
    webhook_message = request.json_body

    response = requests.get(POSITIONS_URL, headers=HEADERS)
    positions = json.loads(response.content)
    print(positions)
    for position in positions:
        if position['symbol'] == webhook_message['ticker']:
            print(position['symbol'])
            print(position['qty'])
            pos_qty = int(position['qty'])
            if pos_qty > 0:
                quantity = pos_qty
                print(quantity)

    if quantity > 0:
        data = {
            "symbol": webhook_message['ticker'],
            "qty": quantity,
            "side": "sell",
            "type": "market",
            # "limit_price": webhook_message['close'],
            "time_in_force": "gtc",
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

@app.route('/sell_short_position', methods=['POST'])
def sell_short_position():
    quantity = 0
    request = app.current_request
    webhook_message = request.json_body

    response = requests.get(POSITIONS_URL, headers=HEADERS)
    positions = json.loads(response.content)
    print(positions)
    for position in positions:
        if position['symbol'] == webhook_message['ticker']:
            print(position['symbol'])
            print(position['qty'])
            pos_qty = int(position['qty'])
            if pos_qty < 0:
                quantity = abs(pos_qty) 
                print(quantity)

    if quantity != 0:
        data = {
            "symbol": webhook_message['ticker'],
            "qty": quantity,
            "side": "buy",
            "type": "market",
            # "limit_price": webhook_message['close'],
            "time_in_force": "gtc",
            # "order_class": "bracket",
            # "take_profit": {
            #     "limit_price": webhook_message['close'] * 0.95
            # },
            # "stop_loss": {
            #     "stop_price": webhook_message['close'] * 1.015,
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

@app.route('/buy_short_position', methods=['POST'])
def buy_short_position():
    request = app.current_request
    webhook_message = request.json_body
    # Get Account Information
    account = accountInfo()
    # Determine Quantity
    quantity = setQuantity(account, webhook_message['close'])
    print(quantity)
    # Look For Current Open Postions
    response = requests.get(POSITIONS_URL, headers=HEADERS)
    positions = json.loads(response.content)
    print(positions)
    for position in positions:
        if position['symbol'] == webhook_message['ticker']:
            print(position['symbol'])
            print(position['qty'])
            pos_qty = int(position['qty'])
            if pos_qty > 0:
                quantity = quantity + pos_qty # sell all long shares and add short shares
                print(quantity)
            else:
                quantity = 0

    if quantity != 0:
        data = {
            "symbol": webhook_message['ticker'],
            "qty": quantity,
            "side": "sell",
            "type": "market",
            # "limit_price": webhook_message['close'],
            "time_in_force": "fok",
            # "order_class": "bracket",
            # "take_profit": {
            #     "limit_price": webhook_message['close'] * 0.995
            # },
            # "stop_loss": {
            #     "stop_price": webhook_message['close'] * 1.005,
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
