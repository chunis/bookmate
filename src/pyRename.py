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

class PyRename(wx.Panel):
	def __init__(self, parent=None, id=-1, tty=sys.stdout):
		wx.Panel.__init__(self, parent, id)
		#self.SetBackgroundColour('White')
		self.create_widgets()


	def create_widgets(self):
		wx.StaticText(self, -1, 'PyRename Not Implemented Yet...', pos=(120, 80))


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
