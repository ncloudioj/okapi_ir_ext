

require 'mkmf'

dir_config('rokapi')

if ! have_header('../okapi-bss.h')
    puts "cannot find okapi-bss.h file."
    exit(1)
end

if have_library('okapibss')
	create_makefile("rokapi")
else
	puts "no okapibss available"
end

