def order_total(order: dict[str, int]) -> int:
    subtotal = order["subtotal"]
    if subtotal >= 5000:
        return subtotal
    return subtotal + order["shipping"]
