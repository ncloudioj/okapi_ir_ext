

require 'mkmf'
dir_config('rokapi')
if have_library('okapibss')
	create_makefile("rokapi")
else
	puts "no okapibss available"
end
