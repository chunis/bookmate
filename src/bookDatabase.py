#!/usr/bin/env python

import os
from bookShelf import Book, BookShelf

class BookDatabase():
	def __init__(self, paths):
		self.bookshelves = {}
		for pth in paths:
			if os.path.isdir(pth):
				self.bookshelves[pth] = BookShelf(pth)

	def list_shelves(self):
		for shelf in self.bookshelves:
			self.bookshelves[shelf].show_all_books()

	def add_shelves(self, paths):
		for p in paths:
			self.add_shelf(p)

	def del_shelves(self, path):
		for p in paths:
			self.del_shelf(p)

	def add_shelf(self, path):
		self.bookshelves[path] = BookShelf(pth)

	def del_shelf(self, path):
		del self.bookshelves[path]


if __name__ == '__main__':
	mybook = BookDatabase(['.'])
	mybook.list_shelves()
