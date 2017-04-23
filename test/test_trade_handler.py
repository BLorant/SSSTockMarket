from unittest import TestCase
from app.stock import Stock
from app.trade_handler import TradeHandler, TRADE_TYPE


class TestTradeHandler(TestCase):
    def test_buy_one_stock(self):
        th = TradeHandler()
        stock = Stock('ABC', 10, 100)
        trade = th.buy_stock(stock, 2, 10)
        trade_list = th._trades['ABC']['common']
        self.assertEquals(1, len(trade_list))
        self.assertEquals(trade_list[0], trade)
        self.assertEquals(trade_list[0].quantity, 2)
        self.assertEquals(trade_list[0].price, 10)
        self.assertEquals(trade_list[0].indicator, TRADE_TYPE.BUY)

    def test_sell_one_stock(self):
        th = TradeHandler()
        stock = Stock('ABC', 10, 100)
        trade = th.sell_stock(stock, 2, 10)
        trade_list = th._trades['ABC']['common']
        self.assertEquals(1, len(trade_list))
        self.assertEquals(trade_list[0], trade)
        self.assertEquals(trade_list[0].quantity, 2)
        self.assertEquals(trade_list[0].price, 10)
        self.assertEquals(trade_list[0].indicator, TRADE_TYPE.SELL)

    def test_multiple_transactions(self):
        th = TradeHandler()
        stock1 = Stock('ABC', 10, 100)
        stock2 = Stock('ABD', 10, 100)
        stock3 = Stock('ABC', 10, 100, is_preferred=True, fixed_dividend=3)
        trade_stock1_1 = th.sell_stock(stock1, 2, 10)
        trade_stock1_2 = th.sell_stock(stock1, 3, 10)
        trade_stock1_3 = th.buy_stock(stock1, 4, 10)
        trade_stock2_1 = th.sell_stock(stock2, 2, 10)
        trade_stock3_1 = th.sell_stock(stock3, 2, 10)
        self.assertEquals(th._trades['ABC']['common'], [trade_stock1_1, trade_stock1_2, trade_stock1_3])
        self.assertEquals(th._trades['ABD']['common'], [trade_stock2_1])
        self.assertEquals(th._trades['ABC']['preferred'], [trade_stock3_1])

    def test_get_all_trades_for_untraded_stock(self):
        stock1 = Stock('ABC', 10, 100)
        self.assertEquals(TradeHandler().get_all_trades_for_stock(stock1), [])

    def test_get_all_trades_for_stock(self):
        th = TradeHandler()
        stock1 = Stock('ABC', 10, 100)
        stock2 = Stock('ABD', 10, 100)
        stock3 = Stock('ABC', 10, 100, is_preferred=True, fixed_dividend=3)
        trade_stock2_1 = th.buy_stock(stock2, 2, 10)
        trade_stock2_2 = th.buy_stock(stock2, 2, 10)
        trade_stock3_1 = th.buy_stock(stock3, 4, 2)
        self.assertEquals([], th.get_all_trades_for_stock(stock1))
        self.assertEquals(th.get_all_trades_for_stock(stock2), [trade_stock2_1, trade_stock2_2])
        self.assertEquals(th.get_all_trades_for_stock(stock3), [trade_stock3_1])

    def test_get_all_stocks(self):
        th = TradeHandler()
        stock1 = Stock('ABC', 10, 100)
        stock2 = Stock('ABD', 10, 100)
        stock3 = Stock('ABC', 10, 100, is_preferred=True, fixed_dividend=3)
        th.buy_stock(stock2, 2, 10)
        th.buy_stock(stock2, 2, 10)
        th.buy_stock(stock3, 4, 2)
        self.assertEquals(th.get_all_stocks(), {stock2, stock3})
