import datetime


def get_volume_wighted_stock_price(th, stock):
    cumulative_quantity = 0
    cumulative_sum = 0
    right_now = datetime.datetime.now()
    for trade in th.get_all_trades_for_stock(stock):
        if right_now - trade.timestamp <= datetime.timedelta(minutes=15):
            cumulative_quantity += trade.quantity
            cumulative_sum += (trade.quantity * trade.price)
    if cumulative_quantity == 0:
        return None
    return cumulative_sum / float(cumulative_quantity)


def get_all_share_index(th):
    weighted_stock_prices = []
    for stock in th.get_all_stocks():
        _price = get_volume_wighted_stock_price(th, stock)
        if _price:
            weighted_stock_prices.append(_price)
    return _geometrical_mean(weighted_stock_prices)


def get_all_share_index_based_on_last_price(th):
    last_prices = []
    for stock in th.get_all_stocks():
        all_trades = th.get_all_trades_for_stock(stock)
        if all_trades:
            last_prices.append(all_trades[-1].price)
    return _geometrical_mean(last_prices)


def _geometrical_mean(numbers):
    if not numbers:
        return None
    cum_product = 1
    for n in numbers:
        cum_product *= n
    return cum_product ** (1.0 / len(numbers))
