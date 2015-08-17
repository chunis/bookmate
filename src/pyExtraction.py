#!/usr/bin/python
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import sys
import wx
import shutil
from pyCommon import CommonListCtrl, find_str
from pySearch import PySearch
try:
	from wx.lib.pubsub import Publisher as pub
except ImportError:
	import wx.lib.pubsub.setupkwargs
	from wx.lib.pubsub import pub


archive_suffix = ['.rar', '.zip', '.7z', 'gz', 'bz2']

class ExtListCtrl(CommonListCtrl):
	def __init__(self, parent, id):
		CommonListCtrl.__init__(self, parent, id)

class PyExtraction(PySearch):
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
		self.list_ctrl_1.DeleteAllItems()
		self.list_ctrl_1.set_value(self.orig_booklist)


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
