require 'rokapi'
require 'test/unit'

class TestRokapi < Test::Unit::TestCase

	def setup
		@okapi = Rokapi.new

	def test_use
		@okapi = Rokapi.new
		asser_equal(@okapi.use('med.sample'), 1)
	end

	def test_use_raise()
		@okapi = Rokapi.new
		asser_raise(@okapi.use(1), ArgumentError())
	end
end
