#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#
# generated by wxGlade 0.6.3 on Mon Jun 27 15:27:43 2011

import sys, os, time
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin

import tool
from search_in_web import search_in_amazon, search_in_douban


DIR_COL = 3
DB_FILE = "bookmate.db"

# begin wxGlade: extracode
# end wxGlade


class MyListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, ColumnSorterMixin):
	def __init__(self, parent, id):
		wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)
		ListCtrlAutoWidthMixin.__init__(self)
		ColumnSorterMixin.__init__(self, 6)
		self.itemDataMap = {}

		self.InsertColumn(0, "Name", width=440)
		self.InsertColumn(1, "Size", format=wx.LIST_FORMAT_RIGHT, width=100)
		self.InsertColumn(2, "Date Modified", format=wx.LIST_FORMAT_RIGHT, width=210)
		self.InsertColumn(3, "Directory", width=400)

	def GetListCtrl(self):
		return self

	def GetColumnSorter(self):
		if self._col == 1:
			return self.StrToFloatSorter
		return ColumnSorterMixin.GetColumnSorter(self)

	def StrToFloatSorter(self, key1, key2):
		col = self._col
		item1 = self.itemDataMap[key1][col]
		item2 = self.itemDataMap[key2][col]

		ascending = self._colSortFlag[col]
		if ascending:
			return int(item1) - int(item2)
		else:
			return int(item2) - int(item1)

	def set_value(self, booklist, color=None):
		for book in booklist:
			mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(book.mtime))
			#size = str(book.size/1024) + 'K'

			item = (book.name, str(book.size), mtime, book.abspath)
			index = self.InsertStringItem(sys.maxint, item[0])
			for col, text in enumerate(item[1:]):
				self.SetStringItem(index, col+1, text)
			self.SetItemData(index, index)
			self.itemDataMap[index] = item
			if color:
				#self.SetItemTextColour(index, color)
				self.SetItemBackgroundColour(index, color)


def to_unicode_or_bust( obj, encoding='utf-8'):
	if isinstance(obj, basestring):
		if not isinstance(obj, unicode):
			obj = unicode(obj, encoding)
	return obj

def find_str(booklist, str):
	ret_list = []
	tlist = str.strip().split()

	#tlist = [ unicode(x, 'utf-8') for x in tlist ]
	tlist = [ to_unicode_or_bust(x) for x in tlist ]

	for x in booklist:
		flag = True
		name = to_unicode_or_bust(x.name).lower()
		for y in tlist:
			if y.lower() not in name:
				break
		else:
			#ret_list += [x.name.encode('utf-8')]
			ret_list.append(x)

	return ret_list


class pySearch(wx.Panel):
	def __init__(self, *args, **kwds):
		self.select = 0

		self.open_file_id = wx.NewId()
		self.open_dir_id = wx.NewId()
		self.clear_id = wx.NewId()
		self.copy_id = wx.NewId()
		self.move_id = wx.NewId()
		self.amazon_id = wx.NewId()
		self.douban_id = wx.NewId()

		# begin wxGlade: pySearch.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Panel.__init__(self, *args, **kwds)
		self.text_ctrl_1 = wx.TextCtrl(self, -1, "")
		self.text_ctrl_1.SetFocus()
		# self.list_ctrl_1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
		self.list_ctrl_1 = MyListCtrl(self, -1)

		self.__do_layout()
		#self.files = open(DB_FILE).readlines()
		#self.files = [ x.strip() for x in self.files ]
		#self.ufiles = [ x.decode('utf-8') for x in self.files ]
		#self.list_ctrl_1.set_value(self.ufiles)
		self.valstr = []

		self.Bind(wx.EVT_TEXT, self.doSearch, self.text_ctrl_1)

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected, self.list_ctrl_1)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeselected, self.list_ctrl_1)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onOpenItem, self.list_ctrl_1)
		self.list_ctrl_1.Bind(wx.EVT_CONTEXT_MENU, self.onRightClick)
		self.list_ctrl_1.Bind(wx.EVT_CHAR, self.onEsc)
		self.text_ctrl_1.Bind(wx.EVT_CHAR, self.onEsc)

		# end wxGlade

	def onEsc(self, event):
		key_code = event.GetKeyCode()
		# print "Key: ", key_code
		if key_code == 27:	# ESC pressed
			search_str = self.text_ctrl_1.GetValue()
			if search_str != "":
				self.text_ctrl_1.SetValue("")
			else:
				self.Close()
		else:
			event.Skip()

	def onRightClick(self, event):
		#print 'Right click now...'
		menu = wx.Menu()

		menu.Append(self.open_file_id, "Open")
		menu.Append(self.open_dir_id, "Open Directory")
		menu.Append(self.copy_id, "Copy to...")
		menu.Append(self.move_id, "Move to...")
		menu.AppendSeparator()
		menu.Append(self.amazon_id, "Search in Amazon.com")
		menu.Append(self.douban_id, "Search in Douban.com")

		self.Bind(wx.EVT_MENU, self.onOpenItem, id = self.open_file_id)
		self.Bind(wx.EVT_MENU, self.onOpenDir, id = self.open_dir_id)
		self.Bind(wx.EVT_MENU, self.onCopy, id = self.copy_id)
		self.Bind(wx.EVT_MENU, self.onMove, id = self.move_id)
		self.Bind(wx.EVT_MENU, self.onAmazon, id = self.amazon_id)
		self.Bind(wx.EVT_MENU, self.onDouban, id = self.douban_id)

		self.PopupMenu(menu)
		menu.Destroy()

	def onOpenDir(self, event):
		#index = event.GetIndex()
		index = self.select
		dir = self.list_ctrl_1.GetItem(index, DIR_COL).GetText()
		tool.openfile(dir)

	def prepareCopyOrMove(self, event, string, func):
		#index = event.GetIndex()
		index = self.select
		name = self.list_ctrl_1.GetItem(index).GetText()
		dir = self.list_ctrl_1.GetItem(index, DIR_COL).GetText()
		print 'Selected %s' %(os.path.join(dir, name))
		file = os.path.join(dir, name)

		if not os.path.exists(file):
			wx.MessageBox("File '%s' doesn't exist!\n"
				"Have you move it already?" %file, "No File Found",
				style=wx.OK|wx.ICON_ERROR)
			return

		dir = wx.DirDialog(None, string)
		if dir.ShowModal() == wx.ID_OK:
			dest_path = dir.GetPath()
		dir.Destroy()

		# Test if it will overwrite existed file
		tmp_file = os.path.join(dest_path, name)
		if os.path.exists(tmp_file):
			dlg = wx.MessageDialog(None, '%s already exist!\n'
				'Do you want to overwrite it?' %tmp_file,
				'File exist',
				wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
			retcode = dlg.ShowModal()
			dlg.Destroy()

			if retcode == wx.ID_NO:
				return

		func(file, dest_path)


	def onCopy(self, event):
		self.prepareCopyOrMove(event, "Copy File To...", tool.copyfile)


	def onMove(self, event):
		self.prepareCopyOrMove(event, "Move File To...", tool.movefile)
		# TODO
		# if moved, update that file's new status

	def onAmazon(self, event):
		index = self.select
		name = self.list_ctrl_1.GetItem(index).GetText()
		search_in_amazon(os.path.splitext(name)[0])

	def onDouban(self, event):
		index = self.select
		name = self.list_ctrl_1.GetItem(index).GetText()
		search_in_douban(os.path.splitext(name)[0])


	def __do_layout(self):
		# begin wxGlade: pySearch.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		sizer_2.Add(self.text_ctrl_1, 0, wx.EXPAND, 0)
		sizer_2.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
		sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		self.Layout()
		# end wxGlade

	def onItemSelected(self, event):
		self.select = event.GetIndex()
		#print 'self.select:', self.select

	def onItemDeselected(self, event):
		#self.select = event.GetIndex
		pass

	def onOpenItem(self, event):
		#index = event.GetIndex()
		index = self.select
		name = self.list_ctrl_1.GetItem(index).GetText()
		dir = self.list_ctrl_1.GetItem(index, DIR_COL).GetText()
		print 'Selected %s' %(os.path.join(dir, name))
		file = os.path.join(dir, name)
		tool.openfile(file)

	def doSearch(self, event): # wxGlade: pySearch.<event_handler>
		self.list_ctrl_1.DeleteAllItems()

		search_str = self.text_ctrl_1.GetValue()
		#print search_str

		#file_list = find_str(self.ufiles, search_str.decode('utf-8'))
		asked_booklist = find_str(self.orig_booklist, search_str)
		self.list_ctrl_1.set_value(asked_booklist)
		# print file_list
		# event.Skip()

# end of class pySearch


class testFrame(wx.Frame):
	def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
		wx.Frame.__init__(self, parent, -1, pos=pos, size=size)
		self.panel = pySearch(self)

class MyApp(wx.App):
	def OnInit(self):
		#wx.InitAllImageHandlers()
		self.frame = testFrame(pos=(300,120), size=(600, 400))
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True


if __name__ == '__main__':
	myapp = MyApp()
	myapp.MainLoop()
