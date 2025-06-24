import logging
from binance.client import Client
from binance.enums import *
from getpass import getpass

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        if testnet:
            self.client = Client(api_key, api_secret)
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        else:
            self.client = Client(api_key, api_secret)

    def place_market_order(self, symbol, side, quantity):
        """
        Places a market order (buy/sell) on Binance Futures
        """
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side.lower() == "buy" else SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logging.info(f"Market order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Failed to place market order: {e}")

    def place_limit_order(self, symbol, side, quantity, price):
        """
        Places a limit order (buy/sell) on Binance Futures
        """
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side.lower() == "buy" else SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                quantity=quantity,
                price=price,
                timeInForce=TIME_IN_FORCE_GTC
            )
            logging.info(f"Limit order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Failed to place limit order: {e}")

    def show_balance(self):
        """
        Prints USDT-M Futures account balances
        """
        try:
            balance = self.client.futures_account_balance()
            for asset in balance:
                logging.info(f"{asset['asset']}: {asset['balance']}")
        except Exception as e:
            logging.error(f"Error fetching balance: {e}")

def main():
    print("\n🔐 Enter your Binance Futures Testnet credentials")
    api_key = input("API Key: ")
    api_secret = getpass("API Secret: ")

    bot = BasicBot(api_key, api_secret)

    while True:
        print("\n📋 Menu:")
        print("1. Place Market Order")
        print("2. Place Limit Order")
        print("3. Show Account Balance")
        print("4. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            side = input("Enter side (buy/sell): ").strip().lower()
            quantity = float(input("Enter quantity: "))
            bot.place_market_order(symbol, side, quantity)

        elif choice == "2":
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            side = input("Enter side (buy/sell): ").strip().lower()
            quantity = float(input("Enter quantity: "))
            price = float(input("Enter price: "))
            bot.place_limit_order(symbol, side, quantity, price)

        elif choice == "3":
            bot.show_balance()

        elif choice == "4":
            print("✅ Exiting the bot. Bye!")
            break

        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()