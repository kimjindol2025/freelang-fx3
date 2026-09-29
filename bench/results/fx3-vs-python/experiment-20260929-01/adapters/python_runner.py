import json
import sys

from final.python import order_total


if __name__ == "__main__":
    print(order_total(json.loads(sys.stdin.read())))
