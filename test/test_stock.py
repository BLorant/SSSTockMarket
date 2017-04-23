from unittest import TestCase
from app.stock import Stock


class TestStock(TestCase):
    def test_invalid_preferred_stock(self):
        with self.assertRaises(Exception) as context:
            Stock('ABC', 12, 100, is_preferred=True)
        self.assertEquals(context.exception.message, 'You need to provide fixed_dividend for preferred stocks')

    def test_get_dividend_yield_with_zero(self):
        stock = Stock('ABC', 12, 100)
        with self.assertRaises(Exception) as context:
            stock.get_dividend_yield(0)
        self.assertEquals(context.exception.message, 'Price cant be zero')

    def test_get_common_dividend_yield_ints(self):
        stock = Stock('ABC', 12, 100)
        self.assertEquals(1, stock.get_dividend_yield(12))
        self.assertEquals(2, stock.get_dividend_yield(6))
        self.assertEquals(3, stock.get_dividend_yield(4))

    def test_get_common_dividend_yield_floats(self):
        stock = Stock('ABC', 10, 100)
        self.assertAlmostEqual(0.1, stock.get_dividend_yield(100))
        self.assertAlmostEqual(0.33333, stock.get_dividend_yield(30), delta=0.00001)

    def test_get_preferred_dividend_yield_ints(self):
        stock = Stock('ABC', 12, 100, is_preferred=True, fixed_dividend=2)
        self.assertEquals(1, stock.get_dividend_yield(200))
        self.assertEquals(4, stock.get_dividend_yield(50))
        self.assertEquals(10, stock.get_dividend_yield(20))

    def test_get_preferred_dividend_yield_floats(self):
        stock = Stock('ABC', 12, 100, is_preferred=True, fixed_dividend=2)
        self.assertAlmostEqual(2.0, stock.get_dividend_yield(100))
        self.assertAlmostEqual(6.66666, stock.get_dividend_yield(30), delta=0.00001)

    def test_get_pe_ratio(self):
        stock = Stock('ABC', 12, 100)
        self.assertAlmostEqual(0.75, stock.get_pe_ratio(3))
        self.assertAlmostEqual(1.33333, stock.get_pe_ratio(4), delta=0.00001)
