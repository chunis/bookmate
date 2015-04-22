#!/usr/bin/env python

from bookShelf import Book, BookShelf

class BookDatabase():
	def __init__(self, paths):
		self.bookshelves = {}
		for pth in paths:
			self.bookshelves[pth] = BookShelf(pth)

	def list_shelves(self):
		for shelf in self.bookshelves:
			#for book in self.bookshelves[shelf]:
			#	book.show_info()
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
	mybook = BookDatabase('.')
	mybook.list_shelves()
