$:.unshift(File.dirname(__FILE__))
require "rokapi"

describe Rokapi do
	it "open the okapi database" do
		Rokapi.new.use("med.sample").should eq(1)
	end
end

describe Rokapi do
	it "open the okapi database with an invalid name" do
		expect{ Rokapi.new.use(1) }.to raise_error(ArgumentError)
	end
end
