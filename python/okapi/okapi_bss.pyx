cimport okapi_bss
from libc.stdlib cimport malloc, free, realloc

cdef enum:
    SMALL_SIZE = 10 * 1024
    LARGE_SIZE = 1024 * 1024
    SKIP_SIZE = 1 # skip the leading useles of document

cdef class OkapiBss:
    """Wrap okapi-bss library"""

    def __init__(self):
        okapi_bss.initialise_bss()

    def __dealloc__(self):
        okapi_bss.close_bss()

    def show_database(self):
        cdef char *result
        cdef bytes output

        result = <char *>malloc(SMALL_SIZE*sizeof(char))
        if not result:
            raise MemoryError()
        if okapi_bss.show_database(result, SMALL_SIZE*sizeof(char)) == 0:
            output = result
            for line in output.rstrip('\n').split('\n')[1:]: # skip the first line
                record = {}
                for column in line.split(' '):
                    [name, value] = column.split('=')
                    record[name] = value.strip(' ')
                yield record

        free(result)


    def use(self, dbname):
        cdef char *database_name = dbname

        return okapi_bss.open_database(database_name)

    def search(self, keywords):
        cdef char **keywords_list
        cdef int i
        cdef int nlen = len(keywords)
        cdef int nset, nposting

        keywords_list = <char **>malloc(nlen*sizeof(char *))
        if not keywords_list:
            raise MemoryError()

        for i in range(nlen):
            keywords_list[i] = keywords[i]

        okapi_bss.okapi_search(nlen, keywords_list, &nset, &nposting)

        free(keywords_list)

        return (nset, nposting)

    def show(self, nset, show_from, nposting):
        cdef size_t size = SMALL_SIZE
        cdef size_t max_size = LARGE_SIZE
        cdef char *docs = <char *>malloc(size)
        if not docs:
            raise MemoryError()

        cdef int ret

        ret = okapi_bss.okapi_show(nset, show_from, nposting, docs, size)
        while ret != nposting and size < max_size:
            size <<= 1
            docs = <char *>realloc(docs, size)
            ret = okapi_bss.okapi_show(nset, show_from, nposting, docs, size)

        cdef bytes output = docs
        for record in output.split('\n\n\n'):
            record = record.lstrip('\n')
            result = {}
            try:
                index_b = record.index('Weight')  # index of 'Wight'
                index_e = record.index('\n')      # index of first '\n'
                index_t = record.index('\n', index_e+1)    # index of first '\n\n'
            except ValueError as e:
                continue
            else:
                result['weight'] = float(record[index_b+len('Weight ') : index_e])
                result['posting'] = record[record.find(':', index_e)+2 : index_t]
                result['text'] = record[index_t+SKIP_SIZE:]
            yield result

        free(docs)
