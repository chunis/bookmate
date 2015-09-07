#!/usr/bin/python
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import os, sys
import re
import shutil
import wx

from pyCommon import CommonTextCtrl, CommonListCtrl, find_str
from pySearch import PySearch
from unpack import unpack_file
import mypubsub as pub


archive_suffix = ['.rar', '.zip', '.7z', '.tar', '.gz', '.tgz', 'xz', '.bz2']
part1_rar = re.compile(r'part0*1.rar')
partx_rar = re.compile(r'part[0-9]+.rar')

# how to process duplicated files
[PROCESS_DELETE, PROCESS_NO_PROCESS, PROCESS_MOVE] = [1, 2, 3]
[DEST_HERE, DEST_THERE] = [1, 2]


class ExtListCtrl(CommonListCtrl):
	def __init__(self, parent, id):
		CommonListCtrl.__init__(self, parent, id)

class PyExtraction(PySearch):
	# TODO: how to merge PySearch's init and self.init_config()?
	#def __init__(self, *args, **kwds):
		#PySearch.__init__(self, args, kwds)

	def init_config(self):
		self.co_extract2destination = DEST_THERE
		self.co_abs_extsomewhere = ""
		self.co_exrm_destiny = PROCESS_DELETE
		self.co_abs_exrmsomewhere = ""


	def filterArchiveBySuffix(self, booklist, suffix):
		ret = []
		for book in booklist:
			if book.name.endswith(suffix):
				ret.append(book)
		return ret

	def getArchiveList(self, booklist):
		ret = []
		for atype in archive_suffix:
			tmp = self.filterArchiveBySuffix(booklist, atype)
			ret += tmp
		return ret

	def showAllArchive(self, booklist):
		self.orig_booklist = self.getArchiveList(booklist)
		self.asked_booklist = self.orig_booklist
		self.list_ctrl_1.DeleteAllItems()
		self.list_ctrl_1.set_value(self.orig_booklist)
		msg="Total archive items found: %d" %len(self.orig_booklist)
		pub.sendMessage("updateStatusBar", msg=msg)

	def onDoExtraction(self):
		#print "onDoExtraction"
		if self.co_extract2destination == DEST_HERE:
			dest = os.path.abspath('.')
		elif self.co_extract2destination == DEST_THERE:
			dest = self.co_abs_extsomewhere
		else:
			print "WARN! co_extract2destination(=%s) too large!" %self.co_extract2destination
			dest = os.path.abspath('.')

		count = 0
		totalcount = len(self.asked_booklist)
		for book in self.asked_booklist:
			#print "extracting %s...", %book.name
			count += 1

			# skip xx.part2.rar, xx.part3.rar...
			if re.search(partx_rar, book.name) and not re.search(part1_rar, book.name):
				continue

			fullname = os.path.join(book.abspath, book.name)
			print "Extracting %s --> %s" %(fullname, dest)
			msg="Extracting [%d/%d]: %s..." %(count, totalcount, fullname)
			pub.sendMessage("updateStatusBar", msg=msg)
			unpack_file(fullname, dest)  # TODO: mark failed archive file in RED

		pub.sendMessage("updateStatusBar", msg="All files were extracted")


	def moveOrRemoveBook(self, func, dest=""):
		for book in self.asked_booklist:
			print "moveOrRemoveBook %s" %book.name
			if dest:
				func(os.path.join(book.abspath, book.name), dest)
			else:
				func(os.path.join(book.abspath, book.name))
		for book in self.asked_booklist:
			self.orig_booklist.remove(book)
		self.asked_booklist = []
		self.list_ctrl_1.DeleteAllItems()  # should be empty now

	def onRemoveArchive(self):
		print "onRemoveArchive"
		if self.co_exrm_destiny == PROCESS_NO_PROCESS:
			wx.MessageBox('Per config, nothing will be done for archive files',
					'Process Archive Files', wx.OK | wx.ICON_INFORMATION, self)
		elif self.co_exrm_destiny == PROCESS_DELETE:
			self.moveOrRemoveBook(os.remove)
		elif self.co_exrm_destiny == PROCESS_MOVE:
			print "Move to %s" %self.co_abs_exrmsomewhere
			if not self.co_abs_exrmsomewhere or not os.path.isdir(self.co_abs_exrmsomewhere):
				wx.MessageBox("You can't set 'Extraction.Remove:destiny=3' with "
				    "a wrong 'Extraction.Remove:somewhere' value.\n"
				    'Please correct it first.',
				    'Config Wrong', wx.OK | wx.wx.ICON_EXCLAMATION, self)
				return
			self.moveOrRemoveBook(shutil.move, self.co_abs_exrmsomewhere)


class testFrame(wx.Frame):
	def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
		wx.Frame.__init__(self, parent, -1, pos=pos, size=size)
		self.panel = PyExtraction(self)

class MyApp(wx.App):
	def OnInit(self):
		self.frame = testFrame(pos=(300,120), size=(320, 200))
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True


if __name__ == '__main__':
	myapp = MyApp()
	myapp.MainLoop()
