# AGMS Python Client Library [![Build Status](https://travis-ci.org/agmscode/agms_python.png?branch=master)](https://travis-ci.org/agmscode/agms_python)

The AGMS library provides integration to the Avant-Garde Payment Gateway.

## Dependencies 
* [requests](http://docs.python-requests.org/en/latest/) or [PycURL](http://pycurl.sourceforge.net/)

## Installation

```python
easy_install agms
```

or

```python
pip install agms
```

## Usage

Examples on how the AGMS Ruby library can be used are found as part of this package in:
examples/
* hpp.py
* invoicing.py
* recurring.py
* report.py
* safe.py
* transaction.py


## Release Notes

Support for Invoicing and Recurring are not yet completed and are still under development.


## Documentation

* [Official documentation](http://onlinepaymentprocessing.com/docs/)
* [Bug Tracker](http://github.com/agmscode/agms_python/issues)

Examples can be found as part of this package in example_hpp.py, example_invoicing.py, example_recurring.py, example_report.py, example_safe.py, example_transaction.py.


## License

See the LICENSE file.

## Development

Test cases can be run with: `nosetests agms/test/unit/*`

## Contributing

1. Fork it ( https://github.com/agmscode/agms_python#fork-destination-box )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

