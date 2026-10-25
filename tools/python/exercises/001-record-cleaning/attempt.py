# Python 001 first prediction:
# Expected printed output:
# Amount value type:
# No learner attempt or tutor solution yet.

orders = [
    {"order_id": 101, "amount": "500"},
    {"order_id": 102, "amount": "200"},
    {"order_id": 103, "amount": "bad"},
    {"order_id": 104, "amount": ""},
    {"order_id": 105, "amount": " 300 "},
]


valid_orders = []
rejected_orders = []

for i in orders:
    for order_id,amount in i.items():
        try:
            if amount > 0:
                return i['order_id'] = amount
                print(res)
        except Exception as e:
            print("Type Error")