def order_total(order: dict[str, int]) -> int:
    subtotal = order["subtotal"]
    shipping = order["shipping"]
    if subtotal >= 5000:
        return subtotal
    return subtotal + shipping
