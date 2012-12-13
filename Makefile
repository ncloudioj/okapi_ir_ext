##

SHELL :=
SHELL := /bin/sh

uname_M := $(shell sh -c 'uname -m 2>/dev/null || echo not')

LIB := libokapibss
TEST := testokapi

VERSION := 1.0.0 

## CC
CC := gcc 
OPTIMISE := -O2
DEBUG := -g
NOW := -Wall
CFLAGS := $(OPTIMISE) $(DEBUG) $(NOW) 
RM := rm -f

## Make gcc happy when linking so file on X86_64
ifeq ($(uname_M),x86_64)
  CFLAGS += -fPIC
endif

## Dependent files
BSS_LIB := -L${OKAPI_ROOT}/lib
I0_DEFS := ${OKAPI_ROOT}/bss_defs
MATH_LIBS := -lm
INCL_DIR = -I. -I$(I0_DEFS)
LIB_DIR = $(BSS_LIB)
LIB_OBJS = okapi-bss.o
TEST_OBJS = test-libokapi.o
ALL_HEAD = defs.h
ALL_LIBS := -li0+ $(MATH_LIBS) 

## Targets
all: $(LIB) $(TEST)

$(LIB):$(LIB_OBJS)
	$(CC) -shared $(CFLAGS) $(INCL_DIR) $(LIB_DIR) \
		-Wl,-soname,$(LIB).so.1 -o $(LIB).so.$(VERSION) \
		$(LIB_OBJS) $(ALL_LIBS)

$(TEST):$(TEST_OBJS) $(LIB)
	$(CC) $(CFLAGS) $(INCL_DIR) $(LIB_DIR) -o $(TEST) \
		${TEST_OBJS} $(LIB).so.$(VERSION) ${ALL_LIBS}

%.o:%.c
	$(CC) $(CFLAGS) -c $<

install: $(LIB).so.$(VERSION)
	cp $< /usr/lib;
	ldconfig;
	ln -sf /usr/lib/$(LIB).so.1 /usr/lib/$(LIB).so

.PHONEY: clean
clean:
	$(RM) *.o *~*

