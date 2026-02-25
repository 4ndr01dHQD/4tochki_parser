from parser.model import FilterDomain


def is_price_relevant(price: int, filter: FilterDomain):
    if filter.min_price is not None and price < filter.min_price:
        return False
    if filter.max_price is not None and price > filter.max_price:
        return False
    return True