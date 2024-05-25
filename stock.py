import yfinance as yf
import json
import os

# Define the file to store the portfolio data
PORTFOLIO_FILE = "portfolio.json"

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=4)

def add_stock(portfolio, symbol, shares):
    if symbol in portfolio:
        portfolio[symbol] += shares
    else:
        portfolio[symbol] = shares
    print(f"Added {shares} shares of {symbol} to your portfolio.")

def remove_stock(portfolio, symbol, shares):
    if symbol in portfolio:
        if portfolio[symbol] > shares:
            portfolio[symbol] -= shares
            print(f"Removed {shares} shares of {symbol} from your portfolio.")
        elif portfolio[symbol] == shares:
            del portfolio[symbol]
            print(f"Removed {symbol} from your portfolio.")
        else:
            print(f"Error: You only have {portfolio[symbol]} shares of {symbol}.")
    else:
        print(f"Error: {symbol} is not in your portfolio.")

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo")  # Use a valid period
    if not data.empty:
        return data['Close'].iloc[-1]  # Get the most recent closing price
    else:
        print(f"Error: No data found for symbol {symbol}.")
        return None

def track_portfolio(portfolio):
    total_value = 0.0
    for symbol, shares in portfolio.items():
        price = get_stock_data(symbol)
        if price is not None:
            value = price * shares
            total_value += value
            print(f"{symbol}: {shares} shares @ ${price:.2f} = ${value:.2f}")
    print(f"Total portfolio value: ${total_value:.2f}")

def main():
    portfolio = load_portfolio()
    
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add stock")
        print("2. Remove stock")
        print("3. Track portfolio")
        print("4. Quit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            symbol = input("Enter the stock symbol: ").upper()
            shares = int(input("Enter the number of shares: "))
            add_stock(portfolio, symbol, shares)
            save_portfolio(portfolio)
        elif choice == '2':
            symbol = input("Enter the stock symbol: ").upper()
            shares = int(input("Enter the number of shares: "))
            remove_stock(portfolio, symbol, shares)
            save_portfolio(portfolio)
        elif choice == '3':
            track_portfolio(portfolio)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

