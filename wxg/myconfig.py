#!/usr/bin/python

import wx    
import gettext
import ConfigParser
import os

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


config_config = [("Generic", GenericInfo), ("Setting Pathes", ConfigPath), ("Ignore Directories and Files", ConfigIgnore)]
config_dupli = [("Duplication", DuplicateInfo), ("Keep One File", DuplicateKeep), ("Remove Duplicate Files", DuplicateRemove)]
config_extract = [("Extraction", ExtractInfo), ("Extract To", ExtractTo), ("Remove Archived Files", ExtractOK)]
config_rename = [("Rename", ReName)]
config_same_name = [("Same Name", SameName)]


class Config(wx.Treebook):
    def __init__(self, parent, id):
        wx.Treebook.__init__(self, parent, id, style=wx.BK_DEFAULT)
        self.pos = 0
        self.allpages = []

        self.addPages(config_config)
        self.addPages(config_dupli)
        self.addPages(config_extract)
        self.addPages(config_rename)
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
        self.allpages.append(win)

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

    def loadConfigFromFile(self, file):
        config = ConfigParser.ConfigParser()
        config.read(file)
        #print config.sections()

        # ['Generic.Path', 'Generic.Ignore', 'Duplication.Keep', 'Duplication.Remove',
        #  'Extraction.To', 'Extraction.Remove', 'Rename', 'Same Name']
        dir1 = config.get('Generic.Path', 'dir1')
        dir2 = config.get('Generic.Path', 'dir2')
        dir3 = config.get('Generic.Path', 'dir3')
        dir4 = config.get('Generic.Path', 'dir4')
        exdir1 = config.get('Generic.Path', 'exdir1')
        exdir2 = config.get('Generic.Path', 'exdir2')

        dirlist = [d for d in [dir1, dir2, dir3, dir4] if d]
        dirs = set(dirlist)
        if len(dirs) != len(dirlist) or exdir1 == exdir2:
            print "WARNING: same dirs found in Generic:Setting Pathes!"
        all_dirs = []
        for d in [dir1, dir2, dir3, dir4, exdir1, exdir2]:
            if not d:
                all_dirs.append(None)
            elif not os.path.isdir(d):
                print "WARNING: path '%s' doesn't exist! will be removed from config" %d
                config.set('Generic.Path', d, '')
                all_dirs.append(None)
            else:
                all_dirs.append(d)

        self.allpages[1].setPath(all_dirs)  # config_path

        ignore_hidden = config.getboolean('Generic.Ignore', 'ignore_hidden')
        ignore_vcd = config.getboolean('Generic.Ignore', 'ignore_vcd')
        ignore_udd = config.getboolean('Generic.Ignore', 'ignore_udd')
        ignore_udft = config.getboolean('Generic.Ignore', 'ignore_udft')
        #print 'ignore boolean:', ignore_hidden, ignore_vcd, ignore_udd, ignore_udft
        self.allpages[2].setIgnore(ignore_hidden, ignore_vcd, ignore_udd, ignore_udft)  # config_ignore

        dupli_keep = config.getint('Duplication.Keep', 'keep')
        #print 'dupli_keep:', dupli_keep
        self.allpages[4].setKeep(dupli_keep)


        return config

    def saveConfigToFile(self):
        pass


class BookMateConfig(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.config = Config(self, -1)
        self.static_line_1 = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        self.button_cancel = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.button_ok = wx.Button(self, wx.ID_ANY, _("OK"))

        self.__do_layout()
        self.Bind(wx.EVT_BUTTON, self.save_config, self.button_ok)
        self.config.loadConfigFromFile('../src/bookmate.cfg')


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.config, 1, wx.ALL | wx.EXPAND, 10)
        sizer_1.Add(self.static_line_1, 0, wx.ALL | wx.EXPAND, 5)
        sizer_2.Add(self.button_cancel, 0, wx.ALIGN_RIGHT, 0)
        sizer_2.Add((60, 20), 0, 0, 0)
        sizer_2.Add(self.button_ok, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def save_config(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'save_config' not implemented!"
        event.Skip()


if __name__ == '__main__':
    gettext.install("Config") # replace with the appropriate catalog name
    app = wx.App()

    frame = BookMateConfig(None, -1, "BookMate Config")
    frame.SetSize((850, 500))
    frame.Centre()
    frame.Show()
    frame.SetFocus()
    app.MainLoop()
