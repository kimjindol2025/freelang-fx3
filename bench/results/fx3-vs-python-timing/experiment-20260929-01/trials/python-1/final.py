def order_total(order: dict[str, int]) -> int:
    if order["subtotal"] >= 5000:
        return order["subtotal"]
    return order["subtotal"] + order["shipping"]
