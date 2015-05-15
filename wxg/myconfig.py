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


config_config = [("ignore"+ ' '*30, ConfigIgnore),  ("Setting path", ConfigPath)]
config_dupli = [("Keep a single copy", DuplicateKeep),  ("remove archive files", DuplicateRemove)]
config_extract = [("extract to", ExtractTo),  ("extract succeed", ExtractOK)]
config_rename = [("rename", ReName)]
config_same_name = [("same name", SameName)]


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

    frame = wx.Frame(None, -1, "my tree book demo")
    win = Config(frame, -1)
    frame.SetSize((900, 500))
    frame.Centre()
    frame.Show()
    frame.window = win
    win.SetFocus()
    app.MainLoop()
