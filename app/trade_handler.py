from trade import Trade
from datetime import datetime as dt
from collections import namedtuple

TRADE_TYPE = namedtuple('types', ['BUY', 'SELL'], verbose=True)(-1, 1)


# This class mimics a database or some other element that can store and return trade elements for a given stock
# Sole purpose of this implementation is tu support the tests in this exercise
# Everything should work perfectly if this class is replaced until the public methods are implemented
class TradeHandler:
    def __init__(self):
        self._trades = {}
        self._stocks = set()

    def buy_stock(self, stock, quantity, price, timestamp=None):
        return self._record_trade(stock, Trade(quantity, TRADE_TYPE.BUY, price, timestamp=(timestamp or dt.now())))

    def sell_stock(self, stock, quantity, price, timestamp=None):
        return self._record_trade(stock, Trade(quantity, TRADE_TYPE.SELL, price, timestamp=(timestamp or dt.now())))

    def _record_trade(self, stock, trade):
        self._stocks.add(stock)
        if stock.symbol not in self._trades:
            self._trades[stock.symbol] = {'common': [], 'preferred': []}
        self.get_all_trades_for_stock(stock).append(trade)
        return trade

    def get_all_trades_for_stock(self, stock):
        if stock.symbol in self._trades:
            return self._trades[stock.symbol][stock.type]
        return None

    def get_all_stocks(self):
        return self._stocks
