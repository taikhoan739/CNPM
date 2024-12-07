def count_cart(cart):
    total_amount, total_quantity=0,0
    if cart:
        for c in cart.values():
            total_amount+=c['price']*c['quantity']
            total_quantity+=c['quantity']
    return {
        'total_amount':total_amount,
        'total_quantity':total_quantity
    }