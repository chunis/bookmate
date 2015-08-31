#!/usr/bin/python
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import sys
import wx
from pyCommon import CommonListCtrl, find_str
from pySearch import PySearch
import mypubsub as pub


class RenameListCtrl(CommonListCtrl):
	def __init__(self, parent, id):
		CommonListCtrl.__init__(self, parent, id)

	def set_value(self, booklist, color):
		for book in booklist:
			mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(book.mtime))
			#size = str(book.size/1024) + 'K'

			item = (book.name, str(book.size), mtime, book.abspath)
			index = self.InsertStringItem(sys.maxint, item[0])
			for col, text in enumerate(item[1:]):
				self.SetStringItem(index, col+1, text)
			self.SetItemData(index, index)
			self.itemDataMap[index] = item
			self.SetItemBackgroundColour(index, color)
			self.SetItemTextColour(index, book.color)


class PyRename(PySearch):
	# TODO: how to merge PySearch's init and self.init_config()?
	#def __init__(self, *args, **kwds):
		#PySearch.__init__(self, args, kwds)

	def init_config(self):
		self.co_add_text = ""
		self.co_remove_text = ""
		self.co_add_to = 2
		self.co_remove_from = 3
		self.co_add_author = False
		self.co_add_isbn = False
		self.co_add_date = False

	def showAllFiles(self):
		self.asked_booklist = self.orig_booklist
		self.list_ctrl_1.DeleteAllItems()
		self.list_ctrl_1.set_value(self.orig_booklist)
		msg="Total Files found: %d" %len(self.orig_booklist)
		pub.sendMessage("updateStatusBar", msg=msg)

	def onSuggestNewName(self):
		print "onSuggestNewName"
		# TODO:
		# based on the config, give suggestions
		# if the new name is the same, don't change the color
		# if has a new name, mark it GREEN
		# only change name if it is marked in GREEN
		# the color can be changed, and names can be edited manually

		pub.sendMessage("updateStatusBar", msg="All new names are marked in GREEN")


	def onReName(self):
		print "onReName"


class testFrame(wx.Frame):
	def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
		wx.Frame.__init__(self, parent, -1, pos=pos, size=size)
		self.panel = PyRename(self)

class MyApp(wx.App):
	def OnInit(self):
		self.frame = testFrame(pos=(300,120), size=(320, 200))
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True


if __name__ == '__main__':
	myapp = MyApp()
	myapp.MainLoop()
