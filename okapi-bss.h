#ifndef __OKAPI_BSS_H
#define __OKAPI_BSS_H

#ifdef __cplusplus
	extern "C" {
#endif

void initialise_bss(void);

int show_database(char *info, size_t n);

int open_database(char *database_name);

void close_bss(void);

int okapi_search(int nkeywords, char **keywords, int *docset, int *npostings);

int okapi_show(int set, int from, int no_docs, char *result, size_t max); 

void okapi_delete(int set);

#ifdef __cplusplus
	}
#endif

#endif
