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
	def __init__(self, fullname):
		self.abspath = os.path.dirname(fullname)
		self.name = os.path.basename(fullname)
		self.size = os.path.getsize(fullname)
		self.mtime = os.path.getmtime(fullname)
		self.color = wx.GREEN
		self.crc32 = 0  # only calculate it when needed
		self.isbn = 0

		# for smart rename
		self.name_rename = ""
		#self.color_rename = wx.BLACK
		self.color_rename = '#666666'


	def calc_crc(self):
		if self.crc32 == 0:  # we won't re-calculate it
			self.crc32 = calc_crc(os.path.join(self.abspath, self.name))
		return self

	def delete_myself(self):
		os.remove(os.path.join(self.abspath, self.name))

	def show_info(self):
		print " abspath: %-30s" %self.abspath,
		print " name: %-20s" %self.name,
		print " size: %-10s" %self.size,
		print " crc32: 0x%x" %self.crc32,
		#print "isbn:", self.isbn,
		print


if __name__ == '__main__':
	mybook = Book(os.path.abspath(__file__), os.path.curdir)
	mybook.show_info()

