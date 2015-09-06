#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import sys, os, time
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin

import tool
from search_in_web import search_in_amazon, search_in_douban


DIR_COL = 3


class CommonListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, ColumnSorterMixin):
	def __init__(self, parent, id):
		wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)
		ListCtrlAutoWidthMixin.__init__(self)
		ColumnSorterMixin.__init__(self, 6)
		self.itemDataMap = {}
		self.select = 0

		self.mark_green_id = wx.NewId()
		self.mark_red_id = wx.NewId()
		self.open_file_id = wx.NewId()
		self.open_dir_id = wx.NewId()
		self.clear_id = wx.NewId()
		self.copy_id = wx.NewId()
		self.move_id = wx.NewId()
		self.amazon_id = wx.NewId()
		self.douban_id = wx.NewId()

		self.InsertColumn(0, "Name", width=440)
		self.InsertColumn(1, "Size", format=wx.LIST_FORMAT_RIGHT, width=100)
		self.InsertColumn(2, "Date Modified", format=wx.LIST_FORMAT_RIGHT, width=210)
		self.InsertColumn(3, "Directory", width=400)

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeselected)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onOpenItem)

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

	def getFullName(self):
		index = self.select
		name = self.GetItem(index).GetText()
		dir = self.GetItem(index, DIR_COL).GetText()
		print 'Selected %s' %(os.path.join(dir, name))
		return os.path.join(dir, name)

	def markColor(self, color):
		index = self.select
		self.SetItemTextColour(index, color)

	def onItemSelected(self, event):
		self.select = event.GetIndex()

	def onItemDeselected(self, event):
		pass

	def onOpenItem(self, event):
		tool.openfile(self.getFullName())

	def onOpenDir(self, event):
		index = self.select
		dir = self.GetItem(index, DIR_COL).GetText()
		tool.openfile(dir)

	def prepareCopyOrMove(self, event, string, func):
		index = self.select
		name = self.GetItem(index).GetText()
		dir = self.GetItem(index, DIR_COL).GetText()
		file = os.path.join(dir, name)
		print 'Selected %s' %file

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
		name = self.GetItem(index).GetText()
		search_in_amazon(os.path.splitext(name)[0])

	def onDouban(self, event):
		index = self.select
		name = self.GetItem(index).GetText()
		search_in_douban(os.path.splitext(name)[0])


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



class testFrame(wx.Frame):
	def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
		wx.Frame.__init__(self, parent, -1, pos=pos, size=size)
		self.panel = CommonListCtrl(self)

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
