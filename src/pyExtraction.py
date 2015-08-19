#!/usr/bin/python
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import os, sys
import wx
import shutil
from pyCommon import CommonListCtrl, find_str
from pySearch import PySearch
from unpack import unpack_file
try:
	from wx.lib.pubsub import Publisher as pub
except ImportError:
	import wx.lib.pubsub.setupkwargs
	from wx.lib.pubsub import pub


archive_suffix = ['.rar', '.zip', '.7z', '.tar', '.gz', '.tgz', '.bz2']

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

	def onDoExtraction(self):
		print "onDoExtraction"
		for book in self.asked_booklist:
			#print "extracting %s...", %book.name

			if self.co_extract2destination == DEST_HERE:
				dest = os.path.abspath('.')
			elif self.co_extract2destination == DEST_THERE:
				dest = self.co_abs_extsomewhere
			else:
				print "WARN! co_extract2destination(=%s) too large!" %self.co_extract2destination
				dest = os.path.abspath('.')

			fullname = os.path.join(book.abspath, book.name)
			print "%s --> %s" %(fullname, dest)
			unpack_file(fullname, dest)

	def onRemoveArchive(self):
		print "onRemoveArchive"
		for book in self.asked_booklist:
			print "remove: ", book.name


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
