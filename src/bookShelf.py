#!/usr/bin/env python

import os

class Book():
	''' All things about a single book '''
	def __init__(self, name, path='', size=0, isbn=0, crc32=0):
		self.name = name
		self.path = path
		self.size = size
		self.isbn = isbn
		self.crc32 = 0

	def show_info(self):
		print "name: %-30s" %self.name,
		print "path: %-30s" %self.path,
		print "size: %-10s" %self.size,
		print "isbn:", self.isbn,
		print "\tcrc32:", self.crc32


class BookShelf():
	''' each path means a bookshelf '''
	def __init__(self, path):
		self.location = path
		self.books = []
		self.add_books(path)

	def add_books(self, path):
		for f in os.listdir(path):
			if os.path.isfile(f):
				self.add_a_book(f)

	def add_a_book(self, f):
		book = Book(f)
		self.books.append(book)

	def show_all_books(self):
		for x in self.books:
			x.show_info()


if __name__ == '__main__':
	mybook = Book('.bashrc', '/home/chunis', 234, 0)
	mybook.show_info()

	mybookShelf = BookShelf('.')
	mybookShelf.show_all_books()
