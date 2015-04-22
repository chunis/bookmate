#!/usr/bin/env python

import os
import binascii


def calc_crc(file):
	size = 4*1024*1024
	crc = 0

	f = open(file)
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
		self.crc32 = 0  # only calculate it when needed
		self.isbn = 0

	def calc_crc(self):
		self.crc32 = calc_crc(os.path.join(self.abspath, self.name))
                return self

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
	def __init__(self, path):
		self.location = os.path.abspath(path)
		self.books = []
		self.add_books(self.location)

	def add_books(self, path):
		for _f in os.listdir(path):
			f = os.path.join(path, _f)
			if os.path.isfile(f):
				self.add_a_book(f)
			elif os.path.isdir(f):
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
