#!/usr/bin/python
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import sys, os
import time
import wx
from pyCommon import CommonTextCtrl, CommonListCtrl
from pySearch import PySearch
from tool import find_str, find_book, beget_new_name
import mypubsub as pub


class RenameListCtrl(CommonListCtrl):
	def __init__(self, parent, id):
		CommonListCtrl.__init__(self, parent, id)

	def set_value(self, booklist):
		for book in booklist:
			mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(book.mtime))
			#size = str(book.size/1024) + 'K'

			item = (book.name, str(book.size), mtime, book.abspath)
			index = self.InsertStringItem(sys.maxint, item[0])
			for col, text in enumerate(item[1:]):
				self.SetStringItem(index, col+1, text)
			self.SetItemData(index, index)
			self.itemDataMap[index] = item
			#self.SetItemBackgroundColour(index, color)
			self.SetItemTextColour(index, wx.BLACK)

			if not book.name_rename:
				continue

			item_newname = (book.name_rename, "", "", "")
			index = self.InsertStringItem(sys.maxint, item_newname[0])
			for col, text in enumerate(item_newname[1:]):
				self.SetStringItem(index, col+1, text)
			self.SetItemData(index, index)
			self.itemDataMap[index] = item_newname
			#self.SetItemBackgroundColour(index, color)
			self.SetItemTextColour(index, book.color_rename)


class PyRename(wx.Panel):
	def __init__(self, *args, **kwds):
                self.orig_booklist = []
		self.asked_booklist = []  # this is the list of search result

		self.suggest_name_id = wx.NewId()
		self.rename_orig_id = wx.NewId()
		self.rename_sugg_id = wx.NewId()

		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Panel.__init__(self, *args, **kwds)
		self.text_ctrl_1 = CommonTextCtrl(self, -1, "")
		self.text_ctrl_1.SetFocus()
		self.list_ctrl_1 = RenameListCtrl(self, -1)

		self.__do_layout()
		self.init_config()

		self.Bind(wx.EVT_TEXT, self.doSearch, self.text_ctrl_1)
		self.list_ctrl_1.Bind(wx.EVT_CONTEXT_MENU, self.onRightClick)
		self.list_ctrl_1.Bind(wx.EVT_CHAR, self.text_ctrl_1.onEsc)


	def init_config(self):
		self.co_add_text = ""
		self.co_remove_text = ""
		self.co_add_to = 2
		self.co_remove_from = 3
		self.co_add_press = True
		self.co_add_isbn = False
		self.co_add_date = False


	def __do_layout(self):
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		sizer_2.Add(self.text_ctrl_1, 0, wx.EXPAND, 0)
		sizer_2.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
		sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		self.Layout()


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


	def markColor(self, color):
		fullname = self.list_ctrl_1.getFullName()
		# print "fullname: %s" %fullname
		for book in self.orig_booklist:
			if os.path.join(book.abspath, book.name) == fullname:
				book.color_rename = color
		self.list_ctrl_1.markColor(color)

	def onMarkGreen(self, event):
		self.markColor(wx.GREEN)

	def onMarkRed(self, event):
		self.markColor(wx.RED)

	def onRightClick(self, event):
		menu = wx.Menu()

		menu.Append(self.list_ctrl_1.mark_green_id, "Mark as Green (to rename)")
		menu.Append(self.list_ctrl_1.mark_red_id, "Mark as Red (to not rename)")
		menu.AppendSeparator()
		menu.Append(self.suggest_name_id, "Suggest name for me")
		menu.Append(self.rename_orig_id, "Rename (based on the original name)")
		menu.Append(self.rename_sugg_id, "Rename (based on the suggested name)")
		menu.AppendSeparator()
		menu.Append(self.list_ctrl_1.open_file_id, "Open")
		menu.Append(self.list_ctrl_1.open_dir_id, "Open Directory")
		menu.Append(self.list_ctrl_1.copy_id, "Copy to...")
		menu.Append(self.list_ctrl_1.move_id, "Move to...")
		menu.AppendSeparator()
		menu.Append(self.list_ctrl_1.amazon_id, "Search in Amazon.com")
		menu.Append(self.list_ctrl_1.douban_id, "Search in Douban.com")

		self.Bind(wx.EVT_MENU, self.onMarkGreen, id = self.list_ctrl_1.mark_green_id)
		self.Bind(wx.EVT_MENU, self.onMarkRed, id = self.list_ctrl_1.mark_red_id)
		self.Bind(wx.EVT_MENU, self.onSuggestSingleName, id = self.suggest_name_id)
		self.Bind(wx.EVT_MENU, self.onRenameFromOrig, id = self.rename_orig_id)
		self.Bind(wx.EVT_MENU, self.onRenameFromSugg, id = self.rename_sugg_id)
		self.Bind(wx.EVT_MENU, self.list_ctrl_1.onOpenItem, id = self.list_ctrl_1.open_file_id)
		self.Bind(wx.EVT_MENU, self.list_ctrl_1.onOpenDir, id = self.list_ctrl_1.open_dir_id)
		self.Bind(wx.EVT_MENU, self.list_ctrl_1.onCopy, id = self.list_ctrl_1.copy_id)
		self.Bind(wx.EVT_MENU, self.list_ctrl_1.onMove, id = self.list_ctrl_1.move_id)
		self.Bind(wx.EVT_MENU, self.list_ctrl_1.onAmazon, id = self.list_ctrl_1.amazon_id)
		self.Bind(wx.EVT_MENU, self.list_ctrl_1.onDouban, id = self.list_ctrl_1.douban_id)

		self.PopupMenu(menu)
		menu.Destroy()

	def doSearch(self, event):
		self.list_ctrl_1.DeleteAllItems()

		search_str = self.text_ctrl_1.GetValue()
		#print search_str

		self.asked_booklist = find_str(self.asked_booklist, search_str)
		self.list_ctrl_1.set_value(self.asked_booklist)
		msg="Total items showed: %d" %len(self.asked_booklist)
		pub.sendMessage("updateStatusBar", msg=msg)
		# event.Skip()

	def giveNewName(self):
		fullname = self.list_ctrl_1.getFullName()
		return beget_new_name(fullname)


	def getCurrentBook(self):
		return find_book(self.asked_booklist, self.list_ctrl_1.getFullName())

	def onSuggestSingleName(self, event):
		book = self.getCurrentBook()
		book.name_rename = self.giveNewName()
		if book.name_rename != book.name:
			book.color_rename = wx.GREEN
		self.showAllFiles()

	def updateName(self, name):
		dlg = wx.TextEntryDialog(None, "Change the below name to your favorite:",
				'Rename the Book', name)
		if dlg.ShowModal() == wx.ID_OK:
			response = dlg.GetValue()
			print 'renamed name = ', response
			book = self.getCurrentBook()
			book.name_rename = response
			if book.name_rename != book.name:
				book.color_rename = wx.GREEN
			self.showAllFiles()


	def onRenameFromOrig(self, event):
		print "onRenameFromOrig"
		book = find_book(self.asked_booklist, self.list_ctrl_1.getFullName())
		self.updateName(book.name)

	def onRenameFromSugg(self, event):
		print "onRenameFromSugg"
		sugg_name = self.giveNewName()
		self.updateName(sugg_name)

	def showAllFiles(self):
		self.list_ctrl_1.DeleteAllItems()
		self.list_ctrl_1.set_value(self.asked_booklist)
		msg="Total Files found: %d" %len(self.asked_booklist)
		pub.sendMessage("updateStatusBar", msg=msg)

	def onSuggestNewName(self):
		print "onSuggestNewName"
		# TODO:
		# based on the config, give suggestions
		# if the new name is the same, don't change the color
		# if has a new name, mark it GREEN
		# only change name if it is marked in GREEN
		# the color can be changed, and names can be edited manually
		for book in self.asked_booklist:
			book.name_rename = beget_new_name(os.path.join(book.abspath, book.name))
			if book.name_rename != book.name:
				book.color_rename = wx.GREEN

		self.list_ctrl_1.DeleteAllItems()
		self.list_ctrl_1.set_value(self.asked_booklist)
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
