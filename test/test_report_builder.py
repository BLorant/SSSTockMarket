from unittest import TestCase
from app.report_builder import *
from app.stock import Stock
from app.trade_handler import TradeHandler

from app.report_builder import _geometrical_mean


class TestReportBuilder(TestCase):
    def test_geometrical_mean(self):
        self.assertAlmostEqual(6, _geometrical_mean([2, 18]))
        self.assertAlmostEqual(16, _geometrical_mean([10, 51.2, 8]))
        self.assertAlmostEqual(10, _geometrical_mean([10, 10, 10, 10, 10, 10]))

    def test_get_volume_wighted_stock_price(self):
        th = TradeHandler()
        stock = Stock('ABC', 10, 100)
        th.buy_stock(stock, 2, 10)
        th.buy_stock(stock, 3, 10)
        self.assertAlmostEqual(10.0, get_volume_weighted_stock_price(th, stock))
        th.sell_stock(stock, 10, 20)
        self.assertAlmostEqual(16.66666, get_volume_weighted_stock_price(th, stock), delta=0.00001)

    def test_get_volume_wighted_stock_price_with_only_old_trades(self):
        th = TradeHandler()
        stock = Stock('ABC', 10, 100)
        th.buy_stock(stock, 2, 10, timestamp=datetime.datetime.now() - datetime.timedelta(minutes=16))
        self.assertIsNone(get_volume_weighted_stock_price(th, stock))

    def test_get_volume_wighted_stock_price_with_older_trades(self):
        th = TradeHandler()
        stock = Stock('ABC', 10, 100)
        too_old = datetime.datetime.now() - datetime.timedelta(minutes=16)
        should_be_okay = datetime.datetime.now() - datetime.timedelta(minutes=14)
        th.buy_stock(stock, 2, 10, timestamp=too_old)
        th.buy_stock(stock, 2, 10, timestamp=should_be_okay)
        th.buy_stock(stock, 3, 30, timestamp=should_be_okay)
        th.buy_stock(stock, 1, 50)
        self.assertAlmostEqual(26.66666, get_volume_weighted_stock_price(th, stock), delta=0.00001)

    def test_get_all_share_index_with_no_valid_trades(self):
        th = TradeHandler()
        stock = Stock('ABC', 10, 100)
        th.buy_stock(stock, 2, 10, timestamp=datetime.datetime.now() - datetime.timedelta(minutes=16))
        self.assertIsNone(get_all_share_index(th))

    def test_get_all_share_index(self):
        th = TradeHandler()
        stock1 = Stock('ABC', 10, 100)
        stock2 = Stock('ABD', 10, 100)
        th.buy_stock(stock1, 10, 10)
        th.buy_stock(stock1, 10, 10)
        th.buy_stock(stock2, 10, 10)
        self.assertAlmostEqual(10, get_all_share_index(th))
        th.buy_stock(stock2, 50, 1)
        self.assertAlmostEqual(5, get_all_share_index(th))

    def test_get_all_share_index_based_on_last_price(self):
        th = TradeHandler()
        stock1 = Stock('ABC', 10, 100)
        stock2 = Stock('ABD', 10, 100)
        stock3 = Stock('ABE', 10, 100)
        th.buy_stock(stock1, 1, 9)
        th.buy_stock(stock1, 10, 10)
        th.buy_stock(stock2, 64, 4)
        th.buy_stock(stock2, 50, 10)
        th.buy_stock(stock3, 1, 346)
        th.buy_stock(stock3, 1, 10)
        self.assertAlmostEqual(10, get_all_share_index_based_on_last_price(th))
