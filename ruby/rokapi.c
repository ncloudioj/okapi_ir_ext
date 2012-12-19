/* Ruby wrap for libokapi */

#include "ruby.h"
#include "okapi-bss.h"

#define SMALL_SIZE 10*1024
#define LARGE_SIZE 1024*1024

static VALUE t_init(VALUE self)
{
    initialise_bss();

    return self;
}

static VALUE t_use(VALUE self, VALUE dbname)
{
    char *name;
	
	if (TYPE(dbname) != T_STRING){
		rb_raise(rb_eArgError, 
				 "ArgError: need a String, %s given", 
				 rb_obj_classname(dbname));
	}
    name = StringValueCStr(dbname);
    return INT2NUM(open_database(name));
}

/* static VALUE t_show_database(VALUE self)
 * {
 * 	char *result;
 * 
 * 	result = ALLOC_N(char *, SMALL_SIZE*sizeof(char));
 * 	if (result == NULL) {
 * 		rb_raise(rb_eMemError, "MemError: no memory available.");
 * 	}
 * 
 * 	if (show_database(result, SMALL_SIZE*sizeof(char)) == 0) {
 * 		
 * 	}
 * }
 */

VALUE cRokapi;

void Init_rokapi()
{
    cRokapi = rb_define_class("Rokapi", rb_cObject);
    rb_define_method(cRokapi, "initialize", t_init, 0);
    rb_define_method(cRokapi, "use", t_use, 1);
}


