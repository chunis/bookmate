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
import os, shutil
#import glob, sys, thread
from pySearch import PySearch
from config.myconfig import BookMateConfig, xloadConfigFromFile
from pyDuplication import PyDuplication, LIST_COLORS
from pyExtraction import PyExtraction
from pyRename import PyRename
from pySameName import PySameName
from bookDatabase import BookDatabase
import mypubsub as pub


Name	= 'BookMate'
Version	= '0.0.3-dev'
Author	= 'Deng Chunhui'
Email	= 'chunchengfh@gmail.com'
Date	= '2015.08.30'
ABOUT   = "Your friendly book management tool implemented by WxPython"

WIN_WIDTH = 1000
WIN_HEIGH = 640

LOG_FILE = "bookmate.log"
CFG_FILE = "bookmate.cfg"
CFG_EXAMPLE_FILE = "bookmate-example.cfg"
[POS_PAGE_SEARCH, POS_PAGE_DUPLI,
 POS_PAGE_EXTRACT, POS_PAGE_RENAME,
 POS_PAGE_SMNAME ] = range(5)


class MyFrame(wx.Frame):
	"Main frame for BookMate"

	def __init__(self, parent=None, id=-1, title='BookMate',
			pos=wx.DefaultPosition, size=wx.DefaultSize):
		wx.Frame.__init__(self, None, -1, title, pos, size)
		pub.subscribe(self._init_config, "configChanged")
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


	def _init_config(self, msg):
		if pub.pub_version == "version_1":
			self.co = msg.data
		elif pub.pub_version == "version_3":
			self.co = msg
		self.init_config(self.co)

	def init_config(self, co):
		self.bookdb = BookDatabase(self.co.dirlist, self.co.exdirlist,
				self.co.ignore_hidden, self.co.ignore_vcd)

		self.search_frame.orig_booklist = self.bookdb.to_booklist()
		self.search_frame.list_ctrl_1.DeleteAllItems()
		self.search_frame.list_ctrl_1.set_value(self.search_frame.orig_booklist)

		self.remove_dupli_frame.co_dupli_keep = self.co.dupli_keep
		self.remove_dupli_frame.co_dupli_destiny = self.co.dupli_destiny
		self.remove_dupli_frame.co_abs_dupsomewhere = self.co.abs_dupsomewhere

		self.batch_extract_frame.co_extract2destination = self.co.extract2destination
		self.batch_extract_frame.co_abs_extsomewhere = self.co.abs_extsomewhere
		self.batch_extract_frame.co_exrm_destiny = self.co.exrm_destiny
		self.batch_extract_frame.co_abs_exrmsomewhere = self.co.abs_exrmsomewhere
		self.batch_extract_frame.showAllArchive(self.search_frame.orig_booklist)

		self.batch_rename_frame.co_add_text = self.co.ren_add_text
		self.batch_rename_frame.co_remove_text = self.co.ren_remove_text
		self.batch_rename_frame.co_add_to = self.co.ren_add_to
		self.batch_rename_frame.co_remove_from = self.co.ren_remove_from
		self.batch_rename_frame.co_add_press = self.co.ren_add_press
		self.batch_rename_frame.co_add_isbn = self.co.ren_add_isbn
		self.batch_rename_frame.co_add_date = self.co.ren_add_date
		self.batch_rename_frame.orig_booklist = self.search_frame.orig_booklist
		self.batch_rename_frame.asked_booklist = self.batch_rename_frame.orig_booklist
		self.batch_rename_frame.showAllFiles()


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
		tb_reload = toolbar.AddSimpleTool(-1, wx.Bitmap('images/reload.png'),
				"Reload",
				"Reload data for all panels")
		toolbar.AddSeparator()
		tb_find_samefile = toolbar.AddSimpleTool(-1, wx.Bitmap('images/find.png'),
				"Find Same File",
				"Find all the same files with or without the same name")
		tb_process_samefile = toolbar.AddSimpleTool(-1, wx.Bitmap('images/clear.png'),
				"Process Same File",
				"Process all same files (in red) except one (in Green)")
		toolbar.AddSeparator()
		tb_do_extraction = toolbar.AddSimpleTool(-1, wx.Bitmap('images/unpack.png'),
				"Extract Archive Files",
				"Extract all filtered archived files")
		tb_remove_archive = toolbar.AddSimpleTool(-1, wx.Bitmap('images/trash.png'),
				"Remove Useless Archive Files",
				"Remove all archived files after they've already be extracted")
		toolbar.AddSeparator()
		tb_suggest_name = toolbar.AddSimpleTool(-1, wx.Bitmap('images/suggest_name.png'),
				"Suggest New Names",
				"Suggest a new name based on meta info and config")
		tb_do_rename = toolbar.AddSimpleTool(-1, wx.Bitmap('images/rename.png'),
				"Re-Name Files Marked in GREEN",
				"Rename all files currently marked in GREEN color")
		toolbar.Realize()

		self.Bind(wx.EVT_MENU, self.onConfig, tb_config)
		self.Bind(wx.EVT_MENU, self.onReload, tb_reload)
		self.Bind(wx.EVT_MENU, self.onFindSameFile, tb_find_samefile)
		self.Bind(wx.EVT_MENU, self.onProcessSameFile, tb_process_samefile)
		self.Bind(wx.EVT_MENU, self.onDoExtraction, tb_do_extraction)
		self.Bind(wx.EVT_MENU, self.onRemoveArchive, tb_remove_archive)
		self.Bind(wx.EVT_MENU, self.onSuggestNewName, tb_suggest_name)
		self.Bind(wx.EVT_MENU, self.onReName, tb_do_rename)


	def createStatusBar(self):
		self.CreateStatusBar()
		self.SetStatusText('Welcome to use BookMate!')

	def updateStatusBar(self, msg):
		if pub.pub_version == "version_1":
			self.SetStatusText(msg.data)
		elif pub.pub_version == "version_3":
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

	def onDoExtraction(self, event):
		self.nb.ChangeSelection(POS_PAGE_EXTRACT)
		dlg = wx.MessageDialog(None, "Extract all showed archive files?\n"
				"Check the config for where to put the extracted files.",
				'Extract Archive Files', wx.YES_NO | wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_YES:
			self.batch_extract_frame.onDoExtraction()

	def onRemoveArchive(self, event):
		self.nb.ChangeSelection(POS_PAGE_EXTRACT)
		dlg = wx.MessageDialog(None, "Process(Delete) all showed archive files?\n"
				"Make sure all files are already extracted successfully.\n"
				"Check the config for how to process the extracted files.",
				'Process Archive Files', wx.YES_NO | wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_YES:
			self.batch_extract_frame.onRemoveArchive()

	def onSuggestNewName(self, event):
		self.nb.ChangeSelection(POS_PAGE_RENAME)
		self.batch_rename_frame.onSuggestNewName()

	def onReName(self, event):
		self.nb.ChangeSelection(POS_PAGE_RENAME)
		dlg = wx.MessageDialog(None, "Rename All Files in GREEN?\n\n"
				"WARNING! All files in GREEN will be renamed.\n"
				"Check the config to make sure the names according your requirements",
				'Re-Name Files', wx.YES_NO | wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_YES:
			self.batch_rename_frame.onReName()

	def onGoSearchBar(self, event):
		self.search_frame.text_ctrl_1.SetFocus()


	def onConfig(self, event):
                frame = BookMateConfig(CFG_FILE, None, -1, "BookMate Config")

                frame.SetSize((850, 500))
                frame.Centre()
                frame.Show()
                frame.SetFocus()

	def onReload(self, event):
		self.init_config(self.co)

	def onClearResult(self, event):
		self.search_frame.onClearResult(event)


	def onHelp(self, event):
		wx.MessageBox('Sorry, No help yet', 'Help', wx.OK | wx.ICON_INFORMATION, self)

	def onAbout(self, event):
		about = (Name 	+ '\n\n' + ABOUT
				+ '\n\nVersion:\t' + Version
				+ '\nAuthor:\t' + Author
				+ '\nEmail:\t' + Email
				+ '\nDate:\t' + Date)
		wx.MessageBox(about, 'About %s' %Name, wx.OK | wx.ICON_INFORMATION, self)

	def onExit(self, event):
		self.Close()


class BookMate(wx.App):
	"Main App for BookMate"

	def OnInit(self):
		self.frame = MyFrame(self, size=(WIN_WIDTH, WIN_HEIGH))
		self.frame.Center()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True


if __name__ == '__main__':
        gettext.install("Config")
	if not os.path.exists(CFG_FILE):
		shutil.copy(CFG_EXAMPLE_FILE, CFG_FILE)

	bookMate = BookMate(False)
	#bookMate = BookMate(True, LOG_FILE)
	bookMate.MainLoop()
