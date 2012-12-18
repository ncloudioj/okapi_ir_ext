# libokapibss

The C, Python, and Ruby wrappers for Okapi BM25 BSS IR system.

## Installation
### For C Wrapper

    $ make
    $ sudo make install

#### Test for C Wrapper

    $ make testokapi

#### Usage

    $ ./testokapi dataset_name query_terms

### For Python Wrapper

    $ cd python
    $ sudo python setup.py install

Note that this wrapper requires the package python-dev.

#### Test for Python Wrapper

    $ cd okapi/test
    $ python test_okapi_bss.py

### For Ruby Wrapper

    $ cd ruby
    $ make

## License

See LICENSE

