def calculate_total(price, qty):
    total = 0
    if price > 0:
        if qty > 0:
            total = price * qty
    return total
