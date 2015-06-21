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


config_config = [("Generic", GenericInfo), ("Setting Search Path", ConfigPath), ("Ignore Directories and Files", ConfigIgnore)]
config_dupli = [("Duplication", DuplicateInfo), ("Keep One File", DuplicateKeep), ("Remove Duplicate Files", DuplicateRemove)]
config_extract = [("Extraction", ExtractInfo), ("Extract To", ExtractTo), ("Remove Archived Files", ExtractOK)]
config_rename = [("Rename", ReName)]
config_same_name = [("Same Name", SameName)]


class Config(wx.Treebook):
    def __init__(self, parent, id):
        wx.Treebook.__init__(self, parent, id, style=wx.BK_DEFAULT)
        self.pos = 0
        self.allpages = []
        self.config_items = None  # to save configs from bookmate.cfg

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

        dir1 = config.get('Generic.Path', 'dir1')
        dir2 = config.get('Generic.Path', 'dir2')
        dir3 = config.get('Generic.Path', 'dir3')
        dir4 = config.get('Generic.Path', 'dir4')
        exdir1 = config.get('Generic.Path', 'exdir1')
        exdir2 = config.get('Generic.Path', 'exdir2')

        dirlist = [d for d in [dir1, dir2, dir3, dir4] if d]
        dirs = set(dirlist)
        if len(dirs) != len(dirlist) or exdir1 and exdir1 == exdir2:
            print "WARNING: same dirs found in Generic:Setting Search Path!"
        all_dirs = []
        for d in [dir1, dir2, dir3, dir4, exdir1, exdir2]:
            if not d:
                all_dirs.append(None)
            elif not os.path.isdir(d):
                print "WARNING: path '%s' doesn't exist! will be removed from config" %d
                config.set('Generic.Path', d, '')
                all_dirs.append(None)
            else:
                all_dirs.append(os.path.abspath(d))

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

        dupli_destiny = config.getint('Duplication.Remove', 'destiny')
        dupli_somewhere = config.get('Duplication.Remove', 'somewhere')
        #print 'dupli_destiny:', dupli_destiny
        #print 'dupli_somewhere:', dupli_somewhere
        if dupli_somewhere and not os.path.isdir(dupli_somewhere):
            print "Warning! %s doesn't exist" %dupli_somewhere
            dupli_somewhere = ""
        if dupli_destiny == 3 and not dupli_somewhere:
            wx.MessageBox("You can't set 'Duplication.Remove:destiny=3' with "
                "a wrong 'Duplication.Remove:somewhere' value.\n"
                'Please correct it first.',
                'Config Wrong', wx.OK | wx.wx.ICON_EXCLAMATION, self)

        if dupli_somewhere:
            abs_somewhere = os.path.abspath(dupli_somewhere)
        else:
            abs_somewhere = None
        self.allpages[5].setRemove(dupli_destiny, abs_somewhere)

        # for extraction.to
        extract2destination = config.getint('Extraction.To', 'destination')
        extract2somewhere = config.get('Extraction.To', 'somewhere')
        #print 'extract2destination:', extract2destination
        #print 'extract2somewhere:', extract2somewhere
        if extract2somewhere and not os.path.isdir(extract2somewhere):
            print "Warning! %s doesn't exist" %extract2somewhere
            extract2somewhere = ""
        if extract2destination == 2 and not extract2somewhere:
            wx.MessageBox("You can't set 'Extraction.To:destination=2' with "
                "a wrong 'Extraction.To:somewhere' value.\n"
                'Please correct it first.',
                'Config Wrong', wx.OK | wx.wx.ICON_EXCLAMATION, self)

        if extract2somewhere:
            abs_somewhere = os.path.abspath(extract2somewhere)
        else:
            abs_somewhere = None
        self.allpages[7].setExtractTo(extract2destination, abs_somewhere)

        # for extraction.remove
        exrm_destiny = config.getint('Extraction.Remove', 'destiny')
        exrm_somewhere = config.get('Extraction.Remove', 'somewhere')
        #print 'exrm_destiny:', exrm_destiny
        #print 'exrm_somewhere:', exrm_somewhere
        if exrm_somewhere and not os.path.isdir(exrm_somewhere):
            print "Warning! %s doesn't exist" %exrm_somewhere
            exrm_somewhere = ""
        if exrm_destiny == 3 and not exrm_somewhere:
            wx.MessageBox("You can't set 'Extraction.Remove:destiny=3' with "
                "a wrong 'Extraction.Remove:somewhere' value.\n"
                'Please correct it first.',
                'Config Wrong', wx.OK | wx.wx.ICON_EXCLAMATION, self)

        if exrm_somewhere:
            abs_somewhere = os.path.abspath(exrm_somewhere)
        else:
            abs_somewhere = None
        self.allpages[8].setExtractRemove(exrm_destiny, abs_somewhere)


        # for rename
        ren_add_text = config.get('Rename', 'add_text')
        ren_remove_text = config.get('Rename', 'remove_text')
        ren_add_to = config.getint('Rename', 'add_to')
        ren_remove_from = config.getint('Rename', 'remove_from')
        ren_add_author = config.getboolean('Rename', 'add_author')
        ren_add_isbn = config.getboolean('Rename', 'add_isbn')
        ren_add_date = config.getboolean('Rename', 'add_date')
        self.allpages[9].setRename(ren_add_text, ren_remove_text, ren_add_to,
                ren_remove_from, ren_add_author, ren_add_isbn, ren_add_date)


        # for same name
        sn_dirs = []
        comp_dir = config.get('SameName', 'comp_dir')
        with_dir = config.get('SameName', 'with_dir')
        for sn_dir in [comp_dir, with_dir]:
            if not sn_dir:
                sn_dirs.append(None)
            elif sn_dir and not os.path.exists(sn_dir):
                print "Warning! '%s' doesn't exist" %sn_dir
                sn_dir = ""
                sn_dirs.append(None)
            else:
                sn_dirs.append(os.path.abspath(sn_dir))
        self.allpages[10].setSameName(*sn_dirs)

        self.config_items = config
        return config


    def saveConfigToFile(self, config=None, conf_file='xbookmate.cfg'):
        if config == None:
            config = self.config_items

        (dir1, dir2, dir3, dir4, exdir1, exdir2) = self.allpages[1].getPath()
        config.set('Generic.Path', 'dir1', dir1)
        config.set('Generic.Path', 'dir2', dir2)
        config.set('Generic.Path', 'dir3', dir3)
        config.set('Generic.Path', 'dir4', dir4)
        config.set('Generic.Path', 'exdir1', exdir1)
        config.set('Generic.Path', 'exdir2', exdir2)

        (ignore_hidden, ignore_vcd, ignore_udd, ignore_udft) = self.allpages[2].getIgnore()
        config.set('Generic.Ignore', 'ignore_hidden', ignore_hidden)
        config.set('Generic.Ignore', 'ignore_vcd', ignore_vcd)
        config.set('Generic.Ignore', 'ignore_udd', ignore_udd)
        config.set('Generic.Ignore', 'ignore_udft', ignore_udft)

        dupli_keep = self.allpages[4].getKeep() + 1 # we count start from 1 instead of 0
        config.set('Duplication.Keep', 'keep', dupli_keep)

        dupli_destiny, dupli_somewhere = self.allpages[5].getRemove()
        if dupli_somewhere:
            if not os.path.isdir(dupli_somewhere):
                wx.MessageBox("Path 'Duplication.Remove:somewhere' doesn't exist.\n"
                    "It will be cleaned in the config",
                    'Config Wrong', wx.OK | wx.wx.ICON_EXCLAMATION, self)
                dupli_somewhere = ""
            else:
                dupli_somewhere = os.path.abspath(dupli_somewhere)
        config.set('Duplication.Remove', 'destiny', dupli_destiny)
        config.set('Duplication.Remove', 'somewhere', dupli_somewhere)

        # for extraction.to
        extract2destination, extract2somewhere = self.allpages[7].getExtractTo()
        if extract2somewhere:
            if not os.path.isdir(extract2somewhere):
                wx.MessageBox("Path 'Extraction.To:somewhere' doesn't exist.\n"
                    "It will be cleaned in the config",
                    'Config Wrong', wx.OK | wx.wx.ICON_EXCLAMATION, self)
                extract2somewhere = ""
            else:
                extract2somewhere = os.path.abspath(extract2somewhere)

        if extract2destination == 2 and not extract2somewhere:
            wx.MessageBox("You can't set 'Extraction.To:destination=2' with "
                "a wrong 'Extraction.To:somewhere' value.\n"
                'Please correct it first.',
                'Config Wrong', wx.OK | wx.wx.ICON_EXCLAMATION, self)

        config.set('Extraction.To', 'destination', extract2destination)
        config.set('Extraction.To', 'somewhere', extract2somewhere)

        # for extraction.remove
        exrm_destiny, exrm_somewhere = self.allpages[8].getExtractRemove()
        if exrm_somewhere and not os.path.isdir(exrm_somewhere):
            wx.MessageBox("Path 'Extraction.Remove:somewhere' doesn't exist.\n"
                "It will be cleaned in the config",
                'Config Wrong', wx.OK | wx.wx.ICON_EXCLAMATION, self)
            exrm_somewhere = ""
        if exrm_destiny == 3 and not exrm_somewhere:
            wx.MessageBox("You can't set 'Extraction.Remove:destiny=3' with "
                "a wrong 'Extraction.Remove:somewhere' value.\n"
                'Please correct it first.',
                'Config Wrong', wx.OK | wx.wx.ICON_EXCLAMATION, self)

        if exrm_somewhere:
            abs_somewhere = os.path.abspath(exrm_somewhere)

        config.set('Extraction.Remove', 'destiny', exrm_destiny)
        config.set('Extraction.Remove', 'somewhere', exrm_somewhere)


        # write it to config file
        cf = open(conf_file, 'w')
        config.write(cf)
        cf.close()



class BookMateConfig(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.config = Config(self, -1)
        self.static_line_1 = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        self.button_cancel = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.button_ok = wx.Button(self, wx.ID_ANY, _("OK"))

        self.__do_layout()
        self.Bind(wx.EVT_BUTTON, self.ignore_config, self.button_cancel)
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

    def ignore_config(self, event):  # wxGlade: MyFrame.<event_handler>
        #print "Start Event handler 'ignore_config'..."
        self.Close()

    def save_config(self, event):  # wxGlade: MyFrame.<event_handler>
        #print "Start Event handler 'save_config'..."
        self.config.saveConfigToFile(None)
        self.Close()


if __name__ == '__main__':
    gettext.install("Config") # replace with the appropriate catalog name
    app = wx.App()

    frame = BookMateConfig(None, -1, "BookMate Config")
    frame.SetSize((850, 500))
    frame.Centre()
    frame.Show()
    frame.SetFocus()
    app.MainLoop()
