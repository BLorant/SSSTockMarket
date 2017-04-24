from trade import Trade
from datetime import datetime as dt
from collections import namedtuple

TRADE_TYPE = namedtuple('types', ['BUY', 'SELL'])(-1, 1)


class TradeHandler:
    """
    This class mimics a database or some other element that can store and return trade elements for a given stock
    Sole purpose of this implementation is tu support the tests in this exercise
    Everything should work perfectly if this class is replaced until the public methods are implemented
    """

    def __init__(self):
        self._trades = {}
        self._stocks = set()

    # in a real implementation it makes sense to use two different methods for buy and sell
    # they might be stored somewhere else or there are different alerts and checks to them
    def buy_stock(self, stock, quantity, price, timestamp=None):
        """
        records a buy event for a given stock if no Timestamp is provided it uses the current timestamp
        returns the Trade
        """
        return self._record_trade(stock, Trade(quantity, TRADE_TYPE.BUY, price, timestamp=(timestamp or dt.now())))

    def sell_stock(self, stock, quantity, price, timestamp=None):
        """
        records a sell event for a given stock if no Timestamp is provided it uses the current timestamp
        returns the Trade
        """
        return self._record_trade(stock, Trade(quantity, TRADE_TYPE.SELL, price, timestamp=(timestamp or dt.now())))

    def _record_trade(self, stock, trade):
        """
        Records a Trade for a stock and returns the Trade
        """
        self._stocks.add(stock)
        if stock.symbol not in self._trades:
            self._trades[stock.symbol] = {'common': [], 'preferred': []}
        self._trades[stock.symbol][stock.type].append(trade)
        return trade

    def get_all_trades_for_stock(self, stock):
        """
        returns all trades for a given stock empty list if there are no recorded trades
        """
        if stock.symbol in self._trades:
            return self._trades[stock.symbol][stock.type][:]
        return []

    def get_all_stocks(self):
        """
        returns all stocks that the system knows about
        """
        return set(self._stocks)
