__author__ = 'maanas'

import agms

agms.Configuration.init('init.ini')

safe = agms.SAFE()

# params = {
#     'payment_type': {'value': 'creditcard'},
#     'first_name': {'value': 'Joe'},
#     'last_name': {'value': 'Smith'},
#     'cc_number': { 'value': '4111111111111111'},
#     'cc_exp_date': {'value': '0520'},
#     'cc_cvv': {'value': '123'}
# }

# result = safe.add(params)

# print result

params = {
    'payment_type': {'value': 'creditcard'},
    'first_name': {'value': 'Joe'},
    'last_name': {'value': 'Smith'},
    'cc_number': {'value': '4111111111111111'},
    'cc_exp_date': {'value': '0500'},
    'cc_cvv': {'value': '123'}
}
safe_result = safe.add(params)
print safe_result
safe_id = safe.response.getSafeId()
print safe_id
params = {
    'first_name': {'value': 'Joe'},
    'last_name': {'value': 'Smith'},
    'cc_number': {'value': '4111111111111111'},
    'safe_id': {'value': safe_id},
}

safe_result = safe.update(params)

print safe_result