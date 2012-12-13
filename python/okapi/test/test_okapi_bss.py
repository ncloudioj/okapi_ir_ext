#!/usr/bin/env python

from okapi import OkapiBss

def test_use():
    ok = OkapiBss()
    ok.use("med.sample")
    (nset, nposting) = ok.search(["heart"])
    for record in ok.show(nset, 0, 5):
        for key, value in record.items():
            print key, value
    return


def test_show_database():
    ok = OkapiBss()
    for database in ok.show_database():
        for key, value in database.items():
            print key, value

if __name__ == "__main__":
	#print environ
	print test_use()
	print test_show_database()
