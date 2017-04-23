import datetime


def get_volume_weighted_stock_price(th, stock):
    """
    returns the volume_wighted_stock_price if there are trades for the stock and 
    None if there aren't any
    """
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
    """
    returns the all share index if there are trades in the system
    None if there aren't any
    """
    weighted_stock_prices = []
    for stock in th.get_all_stocks():
        _price = get_volume_weighted_stock_price(th, stock)
        if _price:
            weighted_stock_prices.append(_price)
    return _geometrical_mean(weighted_stock_prices)


def get_all_share_index_based_on_last_price(th):
    """
    returns the all share index based on last price if there are trades in the system
    None if there aren't any
    """
    last_prices = []
    for stock in th.get_all_stocks():
        all_trades = th.get_all_trades_for_stock(stock)
        if all_trades:
            last_prices.append(all_trades[-1].price)
    return _geometrical_mean(last_prices)


def _geometrical_mean(numbers):
    """
    returns None if the parameter is an empty list,
    because 0 could be a valid value in geometrical mean
    """
    if not numbers:
        return None
    cum_product = 1
    for n in numbers:
        cum_product *= n
    return cum_product ** (1.0 / len(numbers))
