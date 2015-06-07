#!/usr/bin/python

import wx    
import gettext

from config_ignore import ConfigIgnore
from config_path import ConfigPath
from duplicate_keep import DuplicateKeep
from duplicate_remove import DuplicateRemove
from extract_ok import ExtractOK
from extract_to import ExtractTo
from rename import ReName
from same_name import SameName


generic_str = "Configurations for searched directories, ignored directories and file types"
extract_str = "Configurations for Extract"
duplicate_str = "Configurations for Search and remove Duplicated files"


class GenericInfo(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)
        self.label_hidden_notes = wx.StaticText(self, wx.ID_ANY, _(generic_str))

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_4.Add(self.label_hidden_notes, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_4)
        self.Layout()

class ExtractInfo(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)
        self.label_hidden_notes = wx.StaticText(self, wx.ID_ANY, _(extract_str))

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_4.Add(self.label_hidden_notes, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_4)
        self.Layout()

class DuplicateInfo(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)
        self.label_hidden_notes = wx.StaticText(self, wx.ID_ANY, _(duplicate_str))

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_4.Add(self.label_hidden_notes, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_4)
        self.Layout()


config_config = [("Generic", GenericInfo), ("Ignore Directories and Files", ConfigIgnore),  ("Setting Pathes", ConfigPath)]
config_dupli = [("Duplication", DuplicateInfo), ("Keep One File", DuplicateKeep),  ("Remove Duplicate Files", DuplicateRemove)]
config_extract = [("Extraction", ExtractInfo), ("Extract To", ExtractTo),  ("Extract Succeed", ExtractOK)]
config_rename = [("Rename", ReName)]
config_same_name = [("Same Name", SameName)]


class Config(wx.Treebook):
    def __init__(self, parent, id):
        wx.Treebook.__init__(self, parent, id, style=wx.BK_DEFAULT)
        self.pos = 0

        self.addPages(config_config)
        self.addPages(config_dupli)
        self.addPages(config_extract)
        self.addPages(config_rename)
        self.addPages(config_same_name)

        self.Bind(wx.EVT_TREEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TREEBOOK_PAGE_CHANGING, self.OnPageChanging)

        # This is a workaround for a sizing bug on Mac...
        # TODO: does this still needed or not?
        wx.FutureCall(100, self.AdjustSize)

    def AdjustSize(self):
        self.GetTreeCtrl().InvalidateBestSize()
        self.SendSizeEvent()


    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print 'OnPageChanged, old:%d, new:%d, sel:%d' %(old, new, sel)
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print 'OnPageChanging, old:%d, new:%d, sel:%d' %(old, new, sel)
        event.Skip()


    def addSinglePage(self, text, myobj, func):
        p = wx.Panel(self, -1)
        win = myobj(p, -1)
        p.win = win

        def OnCPSize(evt, win=win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())

        p.Bind(wx.EVT_SIZE, OnCPSize)
        func(p, text)


    def addPages(self, pagelist):
        text, obj = pagelist[0]
        self.addSinglePage(text, obj, self.AddPage)

        for text, obj in pagelist[1:]:
            self.addSinglePage(text, obj, self.AddSubPage)

        # expand all sub nodes
        self.ExpandNode(self.pos, True)
        self.pos += len(pagelist)


if __name__ == '__main__':
    gettext.install("Config") # replace with the appropriate catalog name
    app = wx.App()

    frame = wx.Frame(None, -1, "BookMate Config")
    win = Config(frame, -1)
    frame.SetSize((850, 500))
    frame.Centre()
    frame.Show()
    frame.window = win
    win.SetFocus()
    app.MainLoop()
