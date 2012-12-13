/*
**  ok-test defs.h
*/

#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <malloc.h>
#include <signal.h>
#include <stdlib.h>
//#include <defines.h>
#include <math.h>
#include <errno.h>

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif

#ifndef NULL
#define NULL 0
#endif

#define NONE_ASSIGNED -1

#define V_SMALL_BUFFER 256
#define SMALL_BUFFER 1024
#define BIG_BUFFER 10 * 1024
#define MAXSETS (16*1024)

#define MAX_FIELDS 32
#define MAX_INDEXES 32
#define MAX_TERM_LENGTH 256

#define WRITE 0
#define READ 1
#define APPEND 2

#define LEGAL_GSL "HFISGPN"
#define STOP_TERMS "FH"

/* 
 * Portotype of libi0
 */
void iinit(void) ;
int i0(char *, char *) ;
void iexit(void) ;
