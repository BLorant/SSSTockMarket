import datetime


def get_volume_weighted_stock_price(th, stock):
    """
    returns the volume_wighted_stock_price if there are trades for the stock and 
    throws ValueError if there are no trades for the Stock
    """
    cumulative_quantity = 0
    cumulative_sum = 0
    right_now = datetime.datetime.now()
    for trade in th.get_all_trades_for_stock(stock):
        if right_now - trade.timestamp <= datetime.timedelta(minutes=15):
            cumulative_quantity += trade.quantity
            cumulative_sum += (trade.quantity * trade.price)
    if cumulative_quantity == 0:
        raise ValueError('No Trades found for the given Stock')
    return cumulative_sum / float(cumulative_quantity)


def get_all_share_index(th):
    """
    returns the all share index using the volume_weighted_stock_price
    throws ValueError if the latter is not available for any stock
    """
    weighted_stock_prices = []
    for stock in th.get_all_stocks():
        _price = get_volume_weighted_stock_price(th, stock)
        if _price:
            weighted_stock_prices.append(_price)
    if not weighted_stock_prices:
        raise ValueError('No Trades found for the in the System in the past 15 minutes')
    return _geometrical_mean(weighted_stock_prices)


def get_all_share_index_based_on_last_price(th):
    """
    returns the all share index based on last price if there are trades in the system
    throws ValueError if there aren't any
    """
    last_prices = []
    for stock in th.get_all_stocks():
        all_trades = th.get_all_trades_for_stock(stock)
        if all_trades:
            last_prices.append(all_trades[-1].price)
    if not last_prices:
        raise ValueError('No Trades found for the in the System')
    return _geometrical_mean(last_prices)


def _geometrical_mean(numbers):
    """
    returns the geometrical mean
    throws ValueError if the parameter is an empty list or None
    """
    if not numbers:
        raise ValueError('Not able to calculate geometrical mean of empty list or None')
    cumulative_product = 1
    for n in numbers:
        cumulative_product *= n
    return cumulative_product ** (1.0 / len(numbers))
