#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#
# generated by wxGlade 0.7.0 on Sun Jun  7 21:31:04 2015
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class ExtractOK(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ExtractOK.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Panel.__init__(self, *args, **kwds)
        self.label_extract_moveto_note = wx.StaticText(self, wx.ID_ANY, _("After extracting is done, how to process the original archive files?"))
        self.radio_btn_extract_remove = wx.RadioButton(self, wx.ID_ANY, _("Directly delete the original Archive files"))
        self.radio_btn_extract_donothing = wx.RadioButton(self, wx.ID_ANY, _("Do nothing. Leave the archive files as is."))
        self.radio_btn_extract_moveto = wx.RadioButton(self, wx.ID_ANY, _("Move To:"))
        self.text_ctrl_extract_path = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_extract_path = wx.Button(self, wx.ID_ANY, _("..."))
        self.radios = [self.radio_btn_extract_remove, self.radio_btn_extract_donothing, self.radio_btn_extract_moveto]

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        self.Bind(wx.EVT_BUTTON, self.onBrowsePath, self.button_extract_path)


    def __set_properties(self):
        # begin wxGlade: ExtractOK.__set_properties
        self.SetSize((758, 535))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ExtractOK.__do_layout
        sizer_extract_remove1 = wx.BoxSizer(wx.VERTICAL)
        sizer_extract_moveto = wx.BoxSizer(wx.HORIZONTAL)
        sizer_extract_remove1.Add(self.label_extract_moveto_note, 0, wx.EXPAND, 0)
        sizer_extract_remove1.Add(self.radio_btn_extract_remove, 0, wx.TOP, 5)
        sizer_extract_remove1.Add(self.radio_btn_extract_donothing, 0, wx.TOP, 5)
        sizer_extract_moveto.Add(self.radio_btn_extract_moveto, 0, wx.TOP, 5)
        sizer_extract_moveto.Add(self.text_ctrl_extract_path, 1, wx.ALIGN_BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_extract_moveto.Add(self.button_extract_path, 0, 0, 0)
        sizer_extract_remove1.Add(sizer_extract_moveto, 0, wx.EXPAND | wx.TOP, 2)
        self.SetSizer(sizer_extract_remove1)
        self.Layout()
        # end wxGlade

    def onBrowsePath(self, event):
        dir = wx.DirDialog(None, "Choose a Directory:")
        if dir.ShowModal() == wx.ID_OK:
                path = dir.GetPath()
                self.text_ctrl_extract_path.SetValue(path)
        dir.Destroy()

    def setExtractRemove(self, destiny, somewhere):
        if destiny > len(self.radios):
            print "WARNING! Extraction.Remove:destiny too large"
        else:
            self.radios[destiny-1].SetValue(True)

        if somewhere:
            self.text_ctrl_extract_path.SetValue(somewhere)

    def getExtractRemove(self):
        def get_destiny():
            for index, obj in enumerate(self.radios):
                if obj.GetValue():
                    return index+1  # we count start from 1 instead of 0

            print "Something wrong in getRemove(). Should not reach here"
            return 1

        destiny = str(get_destiny())
        somewhere = self.text_ctrl_extract_path.GetValue()
        return (destiny, somewhere)


# end of class ExtractOK
class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        config = ExtractOK(None, wx.ID_ANY, "")
        self.SetTopWindow(config)
        config.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    gettext.install("BookMateConfig") # replace with the appropriate catalog name

    BookMateConfig = MyApp(0)
    BookMateConfig.MainLoop()
