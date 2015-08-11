#!/usr/bin/env python
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import os
import binascii
import wx

ignore_vcdpath = ['.svn', 'CVS', '.git', '.hg']


def calc_crc(myfile):
	size = 4*1024*1024
	crc = 0

	if not os.path.exists(myfile):
		return -1

	f = open(myfile)
	block = f.read(size)
	while block:
		crc = binascii.crc32(block, crc)
		block = f.read(size)

	return (crc & 0xffffffff)

class Book():
	''' All things about a single book '''
	def __init__(self, fullname, spath):
		self.abspath = os.path.dirname(fullname)
		self.spath = spath	# shelf path
		self.name = os.path.basename(fullname)
		self.size = os.path.getsize(fullname)
		self.mtime = os.path.getmtime(fullname)
		self.color = wx.GREEN
		self.crc32 = 0  # only calculate it when needed
		self.isbn = 0

	def calc_crc(self):
		if self.crc32 == 0:  # we won't re-calculate it
			self.crc32 = calc_crc(os.path.join(self.abspath, self.name))
		return self

	def delete_myself(self):
		os.remove(os.path.join(self.abspath, self.name))

	def show_info(self):
		print " abspath: %-30s" %self.abspath,
		#print " spath: %-20s" %self.spath,
		print " name: %-20s" %self.name,
		print " size: %-10s" %self.size,
		print " crc32: 0x%x" %self.crc32,
		#print "isbn:", self.isbn,
		print


class BookShelf():
	''' each path means a bookshelf '''
	def __init__(self, path, expaths=[], ignore_hidden=True, ignore_vcd=True):
		self.location = os.path.abspath(path)
		abs_expaths = [os.path.abspath(p) for p in expaths]
		self.books = []
		self.add_books(self.location, abs_expaths, ignore_hidden, ignore_vcd)

	def add_books(self, path, expaths=[], igh=True, igv=True):
		for _f in os.listdir(path):
			f = os.path.join(path, _f)
			if os.path.isfile(f):
				if not _f.startswith('.') or not igh:
					self.add_a_book(f)
			elif os.path.isdir(f):
				if f not in expaths:
					if igv and _f in ignore_vcdpath:
						pass
					else:
						self.add_books(f)

	def add_a_book(self, fullname):
		book = Book(fullname, self.location)
		self.books.append(book)

	def show_all_books(self):
		for x in self.books:
			x.show_info()

	def iter_books(self):
		for x in self.books:
			yield x


if __name__ == '__main__':
	mybook = Book(os.path.abspath(__file__), os.path.curdir)
	mybook.show_info()

	mybookShelf = BookShelf('.')
	mybookShelf.show_all_books()
