#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

"BookMate: Your friendly book management tool implemented by WxPython"

import wx
import gettext
#import os, sys
#import glob, shutil, thread
from pySearch import PySearch
from config.myconfig import BookMateConfig, xloadConfigFromFile
from pyDuplication import PyDuplication, LIST_COLORS
from pyExtraction import PyExtraction
from pyRename import PyRename
from pySameName import PySameName
from bookDatabase import BookDatabase
try:
	from wx.lib.pubsub import Publisher as pub
except ImportError:
	import wx.lib.pubsub.setupkwargs
	from wx.lib.pubsub import pub


Name	= 'BookMate'
Version	= '0.0.2-dev'
Author	= 'Deng Chunhui'
Email	= 'chunchengfh@gmail.com'
Date	= '2015.08.13'
ABOUT   = "Your friendly book management tool implemented by WxPython"

WIN_WIDTH = 1000
WIN_HEIGH = 640

CFG_FILE = "bookmate.cfg"
[POS_PAGE_SEARCH, POS_PAGE_DUPLI,
 POS_PAGE_EXTRACT, POS_PAGE_RENAME,
 POS_PAGE_SMNAME ] = range(5)


class MyFrame(wx.Frame):
	"Main frame for BookMate"

	def __init__(self, parent=None, id=-1, title='BookMate',
			pos=wx.DefaultPosition, size=wx.DefaultSize):
		wx.Frame.__init__(self, None, -1, title, pos, size)
		pub.subscribe(self.init_config, "configChanged")
		pub.subscribe(self.updateStatusBar, "updateStatusBar")

		self.panel = wx.Panel(self)
		#self.panel.SetBackgroundColour('white')
		self.nb = wx.Notebook(self.panel)

		self.createMenuBar()
		self.createStatusBar()
		self.createToolBar()

		self.search_frame = PySearch(self.nb)
		self.remove_dupli_frame = PyDuplication(self.nb)
		self.batch_extract_frame = PyExtraction(self.nb)
		self.batch_rename_frame = PyRename(self.nb)
		self.same_name_frame = PySameName(self.nb)

		self.nb.AddPage(self.search_frame, "Quick Search", select=True)
		self.nb.AddPage(self.remove_dupli_frame, "Remove Duplications")
		self.nb.AddPage(self.batch_extract_frame, "Batch Extract")
		self.nb.AddPage(self.batch_rename_frame, "Batch Rename")
		self.nb.AddPage(self.same_name_frame, "Same Name")

		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(self.nb, 1, wx.EXPAND)
		self.panel.SetSizer(box)
		#box.Fit(self)

		self.co = xloadConfigFromFile(CFG_FILE)
		self.search_frame.text_ctrl_1.SetFocus()
		self.init_config(self.co)


	def init_config(self, co):
		self.co = co
		self.bookdb = BookDatabase(self.co.dirlist, self.co.exdirlist,
				self.co.ignore_hidden, self.co.ignore_vcd)
		self.search_frame.orig_booklist = self.bookdb.to_booklist()
		self.search_frame.list_ctrl_1.DeleteAllItems()
		self.search_frame.list_ctrl_1.set_value(self.search_frame.orig_booklist)

		self.remove_dupli_frame.co_dupli_keep = self.co.dupli_keep
		self.remove_dupli_frame.co_dupli_destiny = self.co.dupli_destiny
		self.remove_dupli_frame.co_abs_dupsomewhere = self.co.abs_dupsomewhere

	def menu_data(self):
		return [ ("&File", (
				("&Save Result", "Save Search Result", self.mypass),
				("", "", ""),
				("C&onfigure...", "Configure Search Options", self.onConfig),
				("", "", ""),
				("&Close", "Close this tool", self.onExit))),
			 ("&Action", (
				("&Go to Search Bar\tCTRL-F", "Go to Search Bar", self.onGoSearchBar),
				("&Open", "Open", self.mypass),
				("&Open Dir", "Open Dir", self.mypass),
				("&Copy To", "Copy Selected Files to Another Place", self.mypass),
				("&Delete", "Delete Selected Files", self.mypass),
				("", "", ""),
				("&Clear Result\tCTRL-Q", "Clear Search Result", self.onClearResult))),
			 ("&Help", (
				("&Help Contents\tF1", "Help of this tool", self.onHelp),
				("&About", "About this tool", self.onAbout))) ]


	def createMenuBar(self):
		menuBar = wx.MenuBar()
		for eachMenuData in self.menu_data():
			menuLabel = eachMenuData[0]
			menuItems = eachMenuData[1]
			menuBar.Append(self.createMenu(menuItems), menuLabel)
		self.SetMenuBar(menuBar)


	def createMenu(self, menuitems):
		menu = wx.Menu()
		for each_menu in menuitems:
			if each_menu[0] == '':
				menu.AppendSeparator()
			else:
				tmpmenu = menu.Append(wx.NewId(), each_menu[0], each_menu[1])
				self.Bind(wx.EVT_MENU, each_menu[2], tmpmenu)

		return menu


	def mypass(self, event):
		pass

	def createToolBar(self):
		toolbar = self.CreateToolBar()
		tb_config = toolbar.AddSimpleTool(-1, wx.Bitmap('images/configure.png'),
				"Configuration",
				"Configure BookMate")
		toolbar.AddSeparator()
		tb_find_samefile = toolbar.AddSimpleTool(-1, wx.Bitmap('images/find.png'),
				"Find Same File",
				"Find all the same files with or without the same name")
		tb_process_samefile = toolbar.AddSimpleTool(-1, wx.Bitmap('images/clear.png'),
				"Process Same File",
				"Process all same files (in red) except one (in Green)")
		toolbar.AddSeparator()
		toolbar.Realize()

		self.Bind(wx.EVT_MENU, self.onConfig, tb_config)
		self.Bind(wx.EVT_MENU, self.onFindSameFile, tb_find_samefile)
		self.Bind(wx.EVT_MENU, self.onProcessSameFile, tb_process_samefile)


	def createStatusBar(self):
		self.CreateStatusBar()
		self.SetStatusText('Welcome to use BookMate!')

	def updateStatusBar(self, msg):
		self.SetStatusText(msg)


	def onFindSameFile(self, event):
		self.nb.ChangeSelection(POS_PAGE_DUPLI)
		self.remove_dupli_frame.bookdb = self.bookdb
		self.remove_dupli_frame.onFindSameFile()

	def onProcessSameFile(self, event):
		self.nb.ChangeSelection(POS_PAGE_DUPLI)
		dlg = wx.MessageDialog(None, "Do you want to process the duplicated files (marked in red)?\n"
				"Double check the config for the right choice.",
				'Process Duplicated Files?', wx.YES_NO | wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_YES:
			self.remove_dupli_frame.onProcessSameFile()


	def onGoSearchBar(self, event):
		self.search_frame.text_ctrl_1.SetFocus()


	def onConfig(self, event):
		#wx.MessageBox('No Configuration yet', 'Configuration', wx.OK | wx.ICON_INFORMATION, self)
                frame = BookMateConfig(CFG_FILE, None, -1, "BookMate Config")

                frame.SetSize((850, 500))
                frame.Centre()
                frame.Show()
                frame.SetFocus()


	def onClearResult(self, event):
		self.search_frame.onClearResult(event)


	def onHelp(self, event):
		wx.MessageBox('Sorry, No help yet', 'Help', wx.OK | wx.ICON_INFORMATION, self)

	def onAbout(self, event):
		#about = (Name 	+ '\nThis is another PyFind implemented by WxPython'
		about = (Name 	+ '\n\n' + ABOUT
				+ '\n\nVersion:\t' + Version
				+ '\nAuthor:\t' + Author
				+ '\nEmail:\t' + Email
				+ '\nDate:\t' + Date)
		wx.MessageBox(about, 'About %s' %Name, wx.OK | wx.ICON_INFORMATION, self)

	def onExit(self, event):
		#save_config()
		self.Close()



class BookMate(wx.App):
	"Main App for BookMate"

	def OnInit(self):
		self.frame = MyFrame(self, size=(WIN_WIDTH, WIN_HEIGH))
		self.frame.Center()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True

#	thread.start_new(myprint, ())

if __name__ == '__main__':
        gettext.install("Config")
	bookMate = BookMate(False)
	bookMate.MainLoop()
