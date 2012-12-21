
cdef extern from "okapi-bss.h":
	void initialise_bss()
	int show_database(char *, size_t)
	int open_database(char *)
	void close_bss()
	int okapi_search(int, char **, int *, int *)
	int okapi_show(int, int, int, char *, size_t)
	void okapi_delete(int)
