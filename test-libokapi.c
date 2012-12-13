/*
 * Test of libokapi
 *
** The program is called as:
**
**   ok-test <database_name> <query_terms>
*/

#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <malloc.h>
#include <signal.h>
#include <stdlib.h>
#include <math.h>
#include <errno.h>

#include "okapi-bss.h"

/*
** #define various macros
*/

#define TRUE 1
#define FALSE 0

#define NONE_ASSIGNED -1

#define V_SMALL_BUFFER 256
#define SMALL_BUFFER 1024
#define BIG_BUFFER 10 * 1024

#define MAX_FIELDS 32
#define MAX_INDEXES 32

#define LEGAL_GSL "HFISGPN"
#define STOP_TERMS "FH"

int main (int argc,	char *argv[]) {
	int db_open = FALSE;
	char database_name[V_SMALL_BUFFER];

	int docset;
	int npostings;
	int docs_to_show;

	char result[BIG_BUFFER];
	char **keywords;

	/*
	** There must be two command line arguments passed in the order:
	**
	**    database_name, terms file
	*/

	if (argc < 3) {
		fprintf(stderr, "ERROR: Insufficient arguments passed to program.");
		exit(EXIT_FAILURE);
	}
	
	sprintf(database_name, "%s", argv[1]);
	keywords = argv+2;

	int i;
	for (i = 0; i < argc-2; i++) {
		fprintf(stdout, "%s\n", keywords[i]);
	}
	
	/*
	** initialise_bss() initialises the BSS
	*/
	
	initialise_bss();

	if(show_database(result, BIG_BUFFER)==0) {
		printf("database info:\n%s\n", result);
	}

	db_open = open_database(database_name);
	
	if (db_open) {
		printf("Okapi initialisation complete.\n");
		
		okapi_search(argc-2, keywords, &docset, &npostings);
		
		if ((docset != NONE_ASSIGNED) && (npostings > 0)) {
			fprintf(stderr,
							"Search OK: set = %d, np = %d\n", docset, npostings);
			
			docs_to_show = (npostings > 5) ? 5 : npostings;
			okapi_show(docset, 0, docs_to_show, result, BIG_BUFFER);
			fprintf(stdout, "%s\n", result);
		}
		else {
			fprintf(stderr, "ERROR: Quitting.\n");
		}
	}
	else {
		fprintf(stderr, "ERROR opening [%s]\n", database_name);
	}

	close_bss();
	
	exit(EXIT_SUCCESS);
}

