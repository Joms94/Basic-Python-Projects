import yfinance as yf
import pandas as pd


class StockAnalysis(object):
    def __init__(self, ticker):
        self.ticker = ticker

    def history(self, period="max"):
        stock = yf.Ticker(self.ticker)
        stock_history = stock.history(period=period)
        stock_history.reset_index(inplace=True)
        print(stock_history)

    def stock_plot(self, x="Date", y="Open"):
        stock = yf.Ticker(self.ticker)
        stock_history = stock.history(period="max")
        stock_history.reset_index(inplace=True)
        stock_history.plot(x=x, y=y)

    def divs(self):
        stock = yf.Ticker(self.ticker)
        return stock.dividends

apple = StockAnalysis("AAPL")
apple.stock_plot()
