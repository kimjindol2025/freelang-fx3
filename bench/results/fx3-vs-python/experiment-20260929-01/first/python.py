import json
import sys


def order_total(order: dict[str, int]) -> int:
    subtotal = order["subtotal"]
    shipping = order["shipping"]
    return subtotal + shipping


if __name__ == "__main__":
    print(order_total(json.loads(sys.stdin.read())))
