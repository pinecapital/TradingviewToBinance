from flask import Flask, request
from binance.client import Client
import os

app = Flask(__name__)

binance_client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))
TRADINGVIEW_IP_ADDRESSES = ['52.89.214.238', '34.212.75.30', '54.218.53.128','52.32.178.7','127.0.0.1']  # Replace with actual TradingView IPs

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.remote_addr not in TRADINGVIEW_IP_ADDRESSES:
        return 'Unauthorized', 401

    data = request.get_json()
    for order in data:
        symbol = order['symbol']
        quantity = order['lot']
        side = order['side'].upper()  # Convert to uppercase

        # Place order
        order = binance_client.futures_create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )

    return 'Success', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)