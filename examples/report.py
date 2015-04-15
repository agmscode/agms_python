__author__ = 'maanas'

import agms

agms.Configuration.init('init.ini')

# A sample transaction report
rep = agms.Report()

params = {
    'start_date': {'value': '2015-03-25'},
    'end_date': {'value': '2015-03-31'},
}

result = rep.list_transactions(params)
print result

# A sample SAFE report
rep = agms.Report()

params = {
    'start_date': {'value': '2015-03-25'},
    'end_date': {'value': '2015-03-31'},
}

result = rep.list_SAFEs(params)
print result