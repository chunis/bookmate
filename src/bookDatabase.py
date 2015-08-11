#!/usr/bin/env python
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import os
import wx
from bookShelf import Book, BookShelf

[SORT_LONGEST_NAME, SORT_OLDEST, SORT_LESS_DIRS, SORT_MORE_DIRS, SORT_NO_SORT] = range(5)
sort_based_on = [SORT_LONGEST_NAME, SORT_OLDEST, SORT_LESS_DIRS, SORT_MORE_DIRS, SORT_NO_SORT]

class BookDatabase():
	def __init__(self, paths, expaths=[], ignore_hidden=True, ignore_vcd=True):
		self.bookshelves = {}
		for pth in paths:
			if os.path.isdir(pth):
				self.bookshelves[pth] = BookShelf(pth, expaths, ignore_hidden, ignore_vcd)

	def list_shelves(self):
		for shelf in self.bookshelves:
			self.bookshelves[shelf].show_all_books()

	def add_shelves(self, paths):
		for p in paths:
			self.add_shelf(p)

	def del_shelves(self, path):
		for p in paths:
			self.del_shelf(p)

	def add_shelf(self, path, expaths=[], ignore_hidden=True, ignore_vcd=True):
		self.bookshelves[path] = BookShelf(pth, expaths, ignore_hidden, ignore_vcd)

	def del_shelf(self, path):
		del self.bookshelves[path]

	def remove_book(self, book):  # TODO
		pass

	def to_booklist(self):
		ret = []
		for bookshelf in self.bookshelves:
			for book in self.bookshelves[bookshelf].iter_books():
				ret.append(book)
		return ret

	def get_same_size_booklist(self):
		ret = []
		size_dict = {}
		for bookshelf in self.bookshelves:
			for book in self.bookshelves[bookshelf].iter_books():
				size = book.size
				if size not in size_dict:
					size_dict[size] = [1, [book]]
				else:
					size_dict[size][0] += 1
					size_dict[size][1].append(book)

		for size in size_dict:
			if size_dict[size][0] > 1:
				ret.append(size_dict[size][1])
		return ret

	def sort_duplicate(self, filelist, sort_by):
		if sort_by == SORT_NO_SORT:
			pass
		if sort_by == SORT_LONGEST_NAME:
			filelist.sort(key=lambda book: len(book.name), reverse=True)
		if sort_by == SORT_OLDEST:
			filelist.sort(key=lambda book: book.mtime)
		if sort_by == SORT_LESS_DIRS:
			filelist.sort(key=lambda book: len(book.abspath.split(os.path.sep)))
		if sort_by == SORT_MORE_DIRS:
			filelist.sort(key=lambda book: len(book.abspath.split(os.path.sep)), reverse=True)
		return filelist

	def mark_color(self, list_of_list):
		for bklist in list_of_list:
			bklist[0].color = wx.GREEN
			for book in bklist[1:]:
				book.color = wx.RED

	def get_duplicate_booklist(self, sort_by=SORT_NO_SORT):
		ret = []
		crc32_dict = {}

		all_list = self.get_same_size_booklist()
		for booklist in all_list:
			for book in booklist:
				crc32 = book.calc_crc().crc32
				if crc32 not in crc32_dict:
					crc32_dict[crc32] = [1, [book]]
				else:
					crc32_dict[crc32][0] += 1
					crc32_dict[crc32][1].append(book)

		for crc32 in crc32_dict:
			if crc32_dict[crc32][0] > 1:
				ret.append(self.sort_duplicate(crc32_dict[crc32][1], sort_by))
		return ret


	# this method maybe not needed
	def to_sorted_booklist(self):
		ret = self.to_booklist()
		return sorted(ret, key=lambda book: book.size)


if __name__ == '__main__':
	mybook = BookDatabase(['.'])
	mybook.list_shelves()
