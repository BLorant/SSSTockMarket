class Stock:
    def __init__(self, symbol, last_dividend, par_value, fixed_dividend=None, is_preferred=False):
        if is_preferred and not fixed_dividend:
            raise Exception('You need to provide fixed_dividend for preferred stocks')
        self.par_value = par_value
        self.symbol = symbol
        self.last_dividend = last_dividend
        self.is_preferred = is_preferred
        self.fixed_dividend = fixed_dividend

    def get_dividend_yield(self, price):
        if price == 0:
            raise Exception('Price cant be zero')
        if self.is_preferred:
            return self._get_preferred_dividend_yield(float(price))
        return self._get_common_dividend_yield(float(price))

    def get_pe_ratio(self, price):
        return price / self.get_dividend_yield(price)

    def _get_preferred_dividend_yield(self, price):
        return (self.fixed_dividend * self.par_value) / price

    def _get_common_dividend_yield(self, price):
        return self.last_dividend / price
