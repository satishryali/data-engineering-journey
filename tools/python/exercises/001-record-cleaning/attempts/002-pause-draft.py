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
valid_list  = []
invalid_list = []
valid_orders = {}
invalid_orders = {}
for i in orders:
    for order_id,amount in i.items():
        try:
            if amount > 0:
                res = valid_orders['order_id'] = amount
                valid_list.append(res.items())
            else:
                invalid_orders['order_id'] = amount
        except Exception as e:
            invalid_orders['order_id'] = amount
        print(valid_orders)