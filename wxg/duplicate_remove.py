#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.0 on Fri May 15 22:34:50 2015
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class DuplicateRemove(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: DuplicateRemove.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.radio_btn_dupli_remove = wx.RadioButton(self, wx.ID_ANY, _("Directly Delete"))
        self.radio_btn_dupli_donothing = wx.RadioButton(self, wx.ID_ANY, _("Do nothing. Just show them"))
        self.radio_btn_dupli_moveto = wx.RadioButton(self, wx.ID_ANY, _("Move To:"))
        self.text_ctrl_dupli_path = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_dupli_path = wx.Button(self, wx.ID_ANY, _("..."))
        self.sizer_dupli_remove1_staticbox = wx.StaticBox(self, wx.ID_ANY, _("For All Other Files"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: DuplicateRemove.__set_properties
        self.SetTitle(_("frame_2"))
        self.SetSize((758, 535))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: DuplicateRemove.__do_layout
        self.sizer_dupli_remove1_staticbox.Lower()
        sizer_dupli_remove1 = wx.StaticBoxSizer(self.sizer_dupli_remove1_staticbox, wx.VERTICAL)
        sizer_dupli_moveto = wx.BoxSizer(wx.HORIZONTAL)
        sizer_dupli_remove1.Add(self.radio_btn_dupli_remove, 0, wx.TOP, 5)
        sizer_dupli_remove1.Add(self.radio_btn_dupli_donothing, 0, wx.TOP, 5)
        sizer_dupli_moveto.Add(self.radio_btn_dupli_moveto, 0, wx.TOP, 5)
        sizer_dupli_moveto.Add(self.text_ctrl_dupli_path, 1, wx.ALIGN_BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_dupli_moveto.Add(self.button_dupli_path, 0, 0, 0)
        sizer_dupli_remove1.Add(sizer_dupli_moveto, 0, wx.EXPAND | wx.TOP, 2)
        self.SetSizer(sizer_dupli_remove1)
        self.Layout()
        # end wxGlade

# end of class DuplicateRemove
class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        config = DuplicateRemove(None, wx.ID_ANY, "")
        self.SetTopWindow(config)
        config.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    gettext.install("BookMateConfig") # replace with the appropriate catalog name

    BookMateConfig = MyApp(0)
    BookMateConfig.MainLoop()