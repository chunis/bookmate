#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.0 on Fri May 15 23:18:24 2015
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
        self.radio_btn_extract_remove = wx.RadioButton(self, wx.ID_ANY, _("Directly delete the original Archive files"))
        self.radio_btn_extract_donothing = wx.RadioButton(self, wx.ID_ANY, _("Do nothing. Leave the archive files as is."))
        self.radio_btn_extract_moveto = wx.RadioButton(self, wx.ID_ANY, _("Move To:"))
        self.text_ctrl_extract_path = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_extract_path = wx.Button(self, wx.ID_ANY, _("..."))
        self.sizer_extract_remove1_staticbox = wx.StaticBox(self, wx.ID_ANY, _("For All Other Files"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ExtractOK.__set_properties
        self.SetSize((758, 535))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ExtractOK.__do_layout
        self.sizer_extract_remove1_staticbox.Lower()
        sizer_extract_remove1 = wx.StaticBoxSizer(self.sizer_extract_remove1_staticbox, wx.VERTICAL)
        sizer_extract_moveto = wx.BoxSizer(wx.HORIZONTAL)
        sizer_extract_remove1.Add(self.radio_btn_extract_remove, 0, wx.TOP, 5)
        sizer_extract_remove1.Add(self.radio_btn_extract_donothing, 0, wx.TOP, 5)
        sizer_extract_moveto.Add(self.radio_btn_extract_moveto, 0, wx.TOP, 5)
        sizer_extract_moveto.Add(self.text_ctrl_extract_path, 1, wx.ALIGN_BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_extract_moveto.Add(self.button_extract_path, 0, 0, 0)
        sizer_extract_remove1.Add(sizer_extract_moveto, 0, wx.EXPAND | wx.TOP, 2)
        self.SetSizer(sizer_extract_remove1)
        self.Layout()
        # end wxGlade

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