# py-okapi

The python binding for Okapi IR system.

## Installation

    $ sudo python setup install

## Getting started

    >>> import okapi
    >>> bss = okapi.OkapiBss()
    >>> for db in bss.show_database()
    ...     print db['name']
    med.sample
    calm.sample
    >>> bss.use('med.sample')
    >>> bss.search(['query', 'word', 'list'])
    (1, 42)
    >>> for posting in bss.show(nset=1, 0, 10):
    ...     print posting['text']
    The document of the search result....

## License

See LICENSE

