#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import os
import urllib
from thirdparty import desktop

OPEN_FILE_FLAG = 1
OPEN_DIR_FLAG = 1

def openfile(file):
	desktop.open(file)

def to_unicode_or_bust( obj, encoding='utf-8'):
	if isinstance(obj, basestring):
		if not isinstance(obj, unicode):
			obj = unicode(obj, encoding)
	return obj

def find_str(booklist, str):
	ret_list = []
	tlist = str.strip().split()

	#tlist = [ unicode(x, 'utf-8') for x in tlist ]
	tlist = [ to_unicode_or_bust(x) for x in tlist ]

	for x in booklist:
		flag = True
		name = to_unicode_or_bust(x.name).lower()
		for y in tlist:
			if y.lower() not in name:
				break
		else:
			#ret_list += [x.name.encode('utf-8')]
			ret_list.append(x)

	return ret_list

# return book if its fullname is the same as 'fullname'
def find_book(booklist, fullname):
	unicode_name = to_unicode_or_bust(fullname)
	for book in booklist:
		bookname = to_unicode_or_bust(os.path.join(book.abspath, book.name))
		if bookname == unicode_name:
			return book
	return None

def beget_new_name(fullname):
	dirname = os.path.dirname(fullname)
	basename = os.path.basename(fullname)
	print "Suggest a name for %s" %basename

	# do url unquote
	newname = urllib.unquote(basename)
	return newname

