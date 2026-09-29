import json
import sys

from final.python import order_total


for line in sys.stdin:
    if line.strip():
        print(order_total(json.loads(line)))
