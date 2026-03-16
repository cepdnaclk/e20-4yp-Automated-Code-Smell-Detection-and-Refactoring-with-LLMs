def process_order(order):
    subtotal = 0
    for item in order["items"]:
        subtotal += item["price"] * item["quantity"]

    discount = 0
    if order["customer_type"] == "vip":
        discount = subtotal * 0.10
    elif order["customer_type"] == "member":
        discount = subtotal * 0.05

    shipping = 0
    if subtotal > 100:
        shipping = 0
    else:
        shipping = 12

    tax = (subtotal - discount) * 0.08
    total = subtotal - discount + shipping + tax

    summary = {
        "customer": order["customer_name"],
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "tax": tax,
        "total": total,
    }
    return summary
