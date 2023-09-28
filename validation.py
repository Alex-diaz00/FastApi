
def validate_price(orders):
    for o in orders:
        if o.price < 0:
            return False
    return True