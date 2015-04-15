# AGMS Python Client Library

The AGMS library provides integration access to the Avant-Garde Gateway.

## Dependencies 
* [requests](http://docs.python-requests.org/en/latest/) or [PycURL](http://pycurl.sourceforge.net/)

_Note:_ Although discouraged, the dependency on PycURL / requests can be bypassed during development or for deployment on servers where they are impossible to use via:

    # Allow unsafe SSL, removes dependency on PycURL 
    agms.Configuration.use_unsafe_ssl = True


## Release Notes

Support for Invoicing and Recurring are not yet completed.



## Documentation

* [Official documentation](https://www.onlinepaymentprocessing.com/docs/python)
* [Bug Tracker](http://github.com/agms/agms_python/issues)

Examples can be found as part of this package in example_hpp.py, example_invoicing.py, example_recurring.py, example_report.py, example_safe.py, example_transaction.py.


## License

See the LICENSE file.

## Contributing

1. Fork it ( https://github.com/agms_code/agms_python/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

