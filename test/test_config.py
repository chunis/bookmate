#!/usr/bin/python

import wx    
import gettext


extract_str = "Configurations for Extract"

class ExtractInfo(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)
        self.label_hidden_notes = wx.StaticText(self, wx.ID_ANY, _(extract_str))

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_4.Add(self.label_hidden_notes, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_4)
        self.Layout()


class SameName(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Panel.__init__(self, *args, **kwds)
        self.label_smn_from = wx.StaticText(self, wx.ID_ANY, _("Compare Directory:"))
        self.text_ctrl_smn_from_path = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_smn_from_path = wx.Button(self, wx.ID_ANY, _("..."))

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetSize((871, 546))

    def __do_layout(self):
        grid_sizer_1 = wx.FlexGridSizer(1, 3, 0, 0)
        grid_sizer_1.Add(self.label_smn_from, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_smn_from_path, 1, wx.ALIGN_BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        grid_sizer_1.Add(self.button_smn_from_path, 0, 0, 0)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableCol(1)
        self.Layout()


config_extract = [("Extraction", ExtractInfo)]
config_same_name = [("Same Name", SameName)]


class Config(wx.Treebook):
    def __init__(self, parent, id):
        wx.Treebook.__init__(self, parent, id, style=wx.BK_DEFAULT)
        self.pos = 0

        self.addPages(config_extract)
        self.addPages(config_same_name)

        # This is a workaround for a sizing bug on Mac...
        # TODO: does this still needed or not?
        wx.FutureCall(100, self.AdjustSize)

    def AdjustSize(self):
        self.GetTreeCtrl().InvalidateBestSize()
        self.SendSizeEvent()


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


class BookMateConfig(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        #self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Hello World"))
        self.config = Config(self, -1)
        self.static_line_1 = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        self.button_cancel = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.button_ok = wx.Button(self, wx.ID_ANY, _("OK"))

        self.__do_layout()


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.config, 1, wx.EXPAND, 0)
        #sizer_1.Add(self.label_1, 1, 0, 0)
        sizer_1.Add(self.static_line_1, 0, wx.ALL | wx.EXPAND, 5)
        sizer_2.Add(self.button_cancel, 0, wx.ALIGN_RIGHT, 0)
        sizer_2.Add((60, 20), 0, 0, 0)
        sizer_2.Add(self.button_ok, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()


def test_inner():
    frame = wx.Frame(None, -1, "My Config")
    win = Config(frame, -1)
    frame.SetSize((850, 500))
    frame.Centre()
    frame.Show()
    frame.window = win
    win.SetFocus()

def test_outer():
    frame = BookMateConfig(None, -1, "My Config")
    frame.SetSize((850, 500))
    frame.Centre()
    frame.Show()
    frame.SetFocus()

if __name__ == '__main__':
    gettext.install("Config") # replace with the appropriate catalog name
    app = wx.App()

    #test_inner()    # This is OK
    test_outer()   # This is OK, too

    app.MainLoop()
