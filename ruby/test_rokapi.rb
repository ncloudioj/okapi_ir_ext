$:.unshift(File.dirname(__FILE__))
require 'rokapi'
require 'test/unit'

class TestRokapi < Test::Unit::TestCase

	def setup
		@okapi = Rokapi.new
	end

	def test_use
		asser_equal(@okapi.use('med.sample'), 1)
	end

	def test_use_raise()
		asser_raise(@okapi.use(1), ArgumentError())
	end
end
