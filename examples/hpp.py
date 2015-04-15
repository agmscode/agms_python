__author__ = 'maanas'

import agms

agms.Configuration.init('init.ini')

# A minimalist example of a quick $20 payment page with template 1

hpp = agms.HPP()

params = {
    'transaction_type': {'value': 'sale'},
    'amount': {'value': '20.00'},
    'first_name': {'setting': 'required'},
    'last_name': {'setting': 'required'},
    'zip': {'setting': 'required'},
    'email': {'setting': 'required'},
    'hpp_format': {'value': '1'},
}

result = hpp.generate(params)
print 'Quick $20 payment page: <a href="' + hpp.get_link() + '" target="_blank">' + hpp.get_link() + "</a>";
print result


# A more comprehensive example for myagms.com express portal pages

hpp = agms.HPP()

params = {
    'transaction_type': {'value': 'sale'},
    'amount': {'value': '37.08'}, 
    'first_name': {'value': 'Joe', 'setting': 'disabled'},
    'last_name': {'value': 'Smith', 'setting': 'disabled'},
    'zip': {'value': '55418', 'setting': 'disabled'},
    'email': {'value': 'jsmith@test.com', 'setting': 'disabled'},
    'tax_amount': {'value': '2.09', 'setting': 'disabled'},
    'shipping_amount': {'value': '5.00', 'setting': 'disabled'},
    'address': {'value': '123 Main St.', 'setting': 'disabled'},
    'city': {'value': 'Dallas', 'setting': 'disabled'},
    'state': {'value': 'TX', 'setting': 'disabled'},
    'phone': {'value': '555-555-5555', 'setting': 'disabled'},
    'order_id': {'value': '123232', 'setting': 'disabled'},
    'description': {'value': 'Eyeglass Repair', 'setting': 'disabled'},
    'shipping_first_name': {'value': 'Joe', 'setting': 'disabled'},
    'shipping_last_name': {'value': 'Smith', 'setting': 'disabled'},
    'shipping_zip': {'value': '55418', 'setting': 'disabled'},
    'shipping_address': {'value': '123 Main St.', 'setting': 'disabled'},
    'shipping_city': {'value': 'Dallas', 'setting': 'disabled'},
    'shipping_state': {'value': 'TX', 'setting': 'disabled'},
    'shipping_tracking_number': {'value': '1Z23990203949283910', 'setting': 'disabled'},
    'shipping_carrier': {'value': 'UPS', 'setting': 'disabled'},
}

result = hpp.generate(params)
print 'Express payment page generator example: <a href="' + hpp.get_link() + '" target="_blank">' + hpp.get_link() + "</a>";
print result


# A redirection example of a $20 payment

hpp = agms.HPP()

params = {
    'transaction_type': {'value': 'sale'},
    'amount': {'value': '20.00'}, 
    'first_name': {'setting': 'required'},
    'last_name': {'setting': 'required'},
    'zip': {'setting': 'required'},
    'email': {'setting': 'required'},
    # 'enable_auto_add_to_safe': {'value': True}, 
    'return_url': {'value': 'http://dev02.agmsdallas.com/agms_php/mike/redirect_landing.php'},
}

result = hpp.generate(params)
print 'Redirect test: <a href="' + hpp.get_link() + '" target="_blank">' + hpp.get_link() + "</a>";
print result

