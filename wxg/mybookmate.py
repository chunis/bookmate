#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.0 on Wed May  6 23:28:00 2015
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame1(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame1.__init__
        wx.Frame.__init__(self, *args, **kwds)
        self.bookmate = wx.Notebook(self, wx.ID_ANY)
        self.bookmate_config_panel = wx.Panel(self.bookmate, wx.ID_ANY)
        self.label_search_path1 = wx.StaticText(self.bookmate_config_panel, wx.ID_ANY, _("Search Path 1:"), style=wx.ALIGN_RIGHT)
        self.button_path1 = wx.Button(self.bookmate_config_panel, wx.ID_ANY, _("Browse"))
        self.text_ctrl_1 = wx.TextCtrl(self.bookmate_config_panel, wx.ID_ANY, "")
        self.label_search_path2 = wx.StaticText(self.bookmate_config_panel, wx.ID_ANY, _("Search Path 2:"), style=wx.ALIGN_RIGHT)
        self.button_path2 = wx.Button(self.bookmate_config_panel, wx.ID_ANY, _("Browse"))
        self.text_ctrl_2 = wx.TextCtrl(self.bookmate_config_panel, wx.ID_ANY, "")
        self.label_search_path3 = wx.StaticText(self.bookmate_config_panel, wx.ID_ANY, _("Search Path 3:"), style=wx.ALIGN_RIGHT)
        self.button_path3 = wx.Button(self.bookmate_config_panel, wx.ID_ANY, _("Browse"))
        self.text_ctrl_3 = wx.TextCtrl(self.bookmate_config_panel, wx.ID_ANY, "")
        self.label_search_path4 = wx.StaticText(self.bookmate_config_panel, wx.ID_ANY, _("Search Path 4:"), style=wx.ALIGN_RIGHT)
        self.button_path4 = wx.Button(self.bookmate_config_panel, wx.ID_ANY, _("Browse"))
        self.text_ctrl_4 = wx.TextCtrl(self.bookmate_config_panel, wx.ID_ANY, "")
        self.label_exclude_path1 = wx.StaticText(self.bookmate_config_panel, wx.ID_ANY, _("Exclude Path 1:"), style=wx.ALIGN_RIGHT)
        self.button_expath1 = wx.Button(self.bookmate_config_panel, wx.ID_ANY, _("Browse"))
        self.text_ctrl_expath1 = wx.TextCtrl(self.bookmate_config_panel, wx.ID_ANY, "")
        self.label_exclude_path2 = wx.StaticText(self.bookmate_config_panel, wx.ID_ANY, _("Exclude Path 2:"), style=wx.ALIGN_RIGHT)
        self.button_expath2 = wx.Button(self.bookmate_config_panel, wx.ID_ANY, _("Browse"))
        self.text_ctrl_expath2 = wx.TextCtrl(self.bookmate_config_panel, wx.ID_ANY, "")
        self.static_line_1 = wx.StaticLine(self.bookmate_config_panel, wx.ID_ANY, style=wx.EXPAND)
        self.checkbox_hidden = wx.CheckBox(self.bookmate_config_panel, wx.ID_ANY, _("Hidden Files"))
        self.checkbox_cvs = wx.CheckBox(self.bookmate_config_panel, wx.ID_ANY, _("Version Control Directories: CVS, .svn, .git, .hg"))
        self.checkbox_user_dir = wx.CheckBox(self.bookmate_config_panel, wx.ID_ANY, _("User Defined Directories"))
        self.checkbox_user_filetype = wx.CheckBox(self.bookmate_config_panel, wx.ID_ANY, _("User Defined File Types"))
        self.sizer_4_staticbox = wx.StaticBox(self.bookmate_config_panel, wx.ID_ANY, _("Ignore These Directories and Files"))
        self.bookmate_duplicate_panel = wx.Panel(self.bookmate, wx.ID_ANY)
        self.radio_box_1_copy_copy = wx.RadioBox(self.bookmate_duplicate_panel, wx.ID_ANY, _("Keep One Copy"), choices=[_("File with longest name"), _("The oldest"), _("File in less layers of directories"), _("File in more layers of directories"), _("Any one is OK. Don't care anything else")], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.radio_btn_1_copy_copy = wx.RadioButton(self.bookmate_duplicate_panel, wx.ID_ANY, _("Directly Delete"))
        self.radio_btn_1 = wx.RadioButton(self.bookmate_duplicate_panel, wx.ID_ANY, _("Move To"))
        self.text_ctrl_5 = wx.TextCtrl(self.bookmate_duplicate_panel, wx.ID_ANY, "")
        self.button_1 = wx.Button(self.bookmate_duplicate_panel, wx.ID_ANY, _("Choose Path"))
        self.radio_btn_2_copy_copy = wx.RadioButton(self.bookmate_duplicate_panel, wx.ID_ANY, _("Do nothing. Just show them"))
        self.sizer_8_copy_copy_staticbox = wx.StaticBox(self.bookmate_duplicate_panel, wx.ID_ANY, _("For All Other Files"))
        self.button_duplicate_keep_copy_copy_copy = wx.Button(self.bookmate_duplicate_panel, wx.ID_ANY, _("Find Duplicate Files"))
        self.button_duplicate_keep_copy_copy_1 = wx.Button(self.bookmate_duplicate_panel, wx.ID_ANY, _("Find Duplicate Files"))
        self.bookmate_rename_panel = wx.Panel(self.bookmate, wx.ID_ANY)
        self.label_1 = wx.StaticText(self.bookmate_rename_panel, wx.ID_ANY, _("Choose File Type:"))
        self.checkbox_1 = wx.CheckBox(self.bookmate_rename_panel, wx.ID_ANY, _("pdf"))
        self.checkbox_2 = wx.CheckBox(self.bookmate_rename_panel, wx.ID_ANY, _("epub"))
        self.checkbox_3 = wx.CheckBox(self.bookmate_rename_panel, wx.ID_ANY, _("mobi"))
        self.checkbox_4 = wx.CheckBox(self.bookmate_rename_panel, wx.ID_ANY, _("Every files"))
        self.label_2 = wx.StaticText(self.bookmate_rename_panel, wx.ID_ANY, _("Add"))
        self.text_ctrl_6 = wx.TextCtrl(self.bookmate_rename_panel, wx.ID_ANY, "")
        self.label_3 = wx.StaticText(self.bookmate_rename_panel, wx.ID_ANY, _("to"))
        self.radio_btn_2 = wx.RadioButton(self.bookmate_rename_panel, wx.ID_ANY, _("start"))
        self.radio_btn_3 = wx.RadioButton(self.bookmate_rename_panel, wx.ID_ANY, _("end (before file type)"))
        self.label_4 = wx.StaticText(self.bookmate_rename_panel, wx.ID_ANY, _("Remove"))
        self.text_ctrl_7 = wx.TextCtrl(self.bookmate_rename_panel, wx.ID_ANY, "")
        self.label_5 = wx.StaticText(self.bookmate_rename_panel, wx.ID_ANY, _("from"))
        self.radio_btn_4 = wx.RadioButton(self.bookmate_rename_panel, wx.ID_ANY, _("start"))
        self.radio_btn_5 = wx.RadioButton(self.bookmate_rename_panel, wx.ID_ANY, _("end"))
        self.radio_btn_6 = wx.RadioButton(self.bookmate_rename_panel, wx.ID_ANY, _("anywhere"))
        self.label_6 = wx.StaticText(self.bookmate_rename_panel, wx.ID_ANY, _("add"))
        self.checkbox_5 = wx.CheckBox(self.bookmate_rename_panel, wx.ID_ANY, _("Author"))
        self.checkbox_6 = wx.CheckBox(self.bookmate_rename_panel, wx.ID_ANY, _("isbn"))
        self.checkbox_7 = wx.CheckBox(self.bookmate_rename_panel, wx.ID_ANY, _("date(year,month)"))
        self.button_2 = wx.Button(self.bookmate_rename_panel, wx.ID_ANY, _("Suggest Names"))
        self.button_3 = wx.Button(self.bookmate_rename_panel, wx.ID_ANY, _("Rename All Files Marked Green"))
        self.bookmate_extract_panel = wx.Panel(self.bookmate, wx.ID_ANY)
        self.bookmate_same_name_panel = wx.Panel(self.bookmate, wx.ID_ANY)
        self.label_7 = wx.StaticText(self.bookmate_same_name_panel, wx.ID_ANY, _("Search:"))
        self.radio_btn_7 = wx.RadioButton(self.bookmate_same_name_panel, wx.ID_ANY, _("File Only"))
        self.radio_btn_8 = wx.RadioButton(self.bookmate_same_name_panel, wx.ID_ANY, _("Directories Only"))
        self.radio_btn_9 = wx.RadioButton(self.bookmate_same_name_panel, wx.ID_ANY, _("Both Directories and Files"))
        self.checkbox_8 = wx.CheckBox(self.bookmate_same_name_panel, wx.ID_ANY, _("Only show files with the same content files besides the same file name"))
        self.button_4 = wx.Button(self.bookmate_same_name_panel, wx.ID_ANY, _("Do it"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame1.__set_properties
        self.SetTitle(_("frame_2"))
        self.SetSize((758, 535))
        self.static_line_1.Hide()
        self.radio_box_1_copy_copy.SetSelection(0)
        self.bookmate.SetMinSize((549, 406))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame1.__do_layout
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_11_copy = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_8_copy_copy_staticbox.Lower()
        sizer_8_copy_copy = wx.StaticBoxSizer(self.sizer_8_copy_copy_staticbox, wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_4_staticbox.Lower()
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_path = wx.FlexGridSizer(6, 3, 0, 0)
        grid_sizer_path.Add(self.label_search_path1, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        grid_sizer_path.Add(self.button_path1, 0, wx.RIGHT, 5)
        grid_sizer_path.Add(self.text_ctrl_1, 0, wx.EXPAND, 0)
        grid_sizer_path.Add(self.label_search_path2, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        grid_sizer_path.Add(self.button_path2, 0, wx.RIGHT, 5)
        grid_sizer_path.Add(self.text_ctrl_2, 0, wx.EXPAND, 0)
        grid_sizer_path.Add(self.label_search_path3, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        grid_sizer_path.Add(self.button_path3, 0, wx.RIGHT, 5)
        grid_sizer_path.Add(self.text_ctrl_3, 0, wx.EXPAND, 0)
        grid_sizer_path.Add(self.label_search_path4, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        grid_sizer_path.Add(self.button_path4, 0, wx.RIGHT, 5)
        grid_sizer_path.Add(self.text_ctrl_4, 0, wx.EXPAND, 0)
        grid_sizer_path.Add(self.label_exclude_path1, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        grid_sizer_path.Add(self.button_expath1, 0, wx.RIGHT, 5)
        grid_sizer_path.Add(self.text_ctrl_expath1, 0, wx.EXPAND, 0)
        grid_sizer_path.Add(self.label_exclude_path2, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        grid_sizer_path.Add(self.button_expath2, 0, wx.RIGHT, 5)
        grid_sizer_path.Add(self.text_ctrl_expath2, 0, wx.EXPAND, 0)
        grid_sizer_path.AddGrowableCol(2)
        sizer_2.Add(grid_sizer_path, 1, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_4.Add(self.checkbox_hidden, 0, 0, 0)
        sizer_4.Add(self.checkbox_cvs, 0, 0, 0)
        sizer_4.Add(self.checkbox_user_dir, 0, 0, 0)
        sizer_4.Add(self.checkbox_user_filetype, 0, 0, 0)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        self.bookmate_config_panel.SetSizer(sizer_1)
        sizer_9_copy.Add(self.radio_box_1_copy_copy, 0, 0, 0)
        sizer_8_copy_copy.Add(self.radio_btn_1_copy_copy, 0, 0, 0)
        sizer_5.Add(self.radio_btn_1, 0, 0, 0)
        sizer_5.Add(self.text_ctrl_5, 0, wx.EXPAND, 0)
        sizer_5.Add(self.button_1, 0, 0, 0)
        sizer_8_copy_copy.Add(sizer_5, 1, 0, 0)
        sizer_8_copy_copy.Add(self.radio_btn_2_copy_copy, 0, 0, 0)
        sizer_10_copy.Add(sizer_8_copy_copy, 1, 0, 0)
        sizer_11_copy.Add(self.button_duplicate_keep_copy_copy_copy, 0, 0, 0)
        sizer_11_copy.Add(self.button_duplicate_keep_copy_copy_1, 0, 0, 0)
        sizer_10_copy.Add(sizer_11_copy, 1, 0, 0)
        sizer_9_copy.Add(sizer_10_copy, 1, 0, 0)
        self.bookmate_duplicate_panel.SetSizer(sizer_9_copy)
        sizer_7.Add(self.label_1, 0, 0, 0)
        sizer_7.Add(self.checkbox_1, 0, 0, 0)
        sizer_7.Add(self.checkbox_2, 0, 0, 0)
        sizer_7.Add(self.checkbox_3, 0, 0, 0)
        sizer_7.Add(self.checkbox_4, 0, 0, 0)
        sizer_6.Add(sizer_7, 0, 0, 0)
        sizer_8.Add(self.label_2, 0, 0, 0)
        sizer_8.Add(self.text_ctrl_6, 0, 0, 0)
        sizer_8.Add(self.label_3, 0, 0, 0)
        sizer_8.Add(self.radio_btn_2, 0, 0, 0)
        sizer_8.Add(self.radio_btn_3, 0, 0, 0)
        sizer_6.Add(sizer_8, 0, 0, 0)
        sizer_9.Add(self.label_4, 0, 0, 0)
        sizer_9.Add(self.text_ctrl_7, 0, 0, 0)
        sizer_9.Add(self.label_5, 0, 0, 0)
        sizer_9.Add(self.radio_btn_4, 0, 0, 0)
        sizer_9.Add(self.radio_btn_5, 0, 0, 0)
        sizer_9.Add(self.radio_btn_6, 0, 0, 0)
        sizer_6.Add(sizer_9, 0, 0, 0)
        sizer_10.Add(self.label_6, 0, 0, 0)
        sizer_10.Add(self.checkbox_5, 0, 0, 0)
        sizer_10.Add(self.checkbox_6, 0, 0, 0)
        sizer_10.Add(self.checkbox_7, 0, 0, 0)
        sizer_6.Add(sizer_10, 0, 0, 0)
        sizer_11.Add(self.button_2, 0, 0, 0)
        sizer_11.Add(self.button_3, 0, 0, 0)
        sizer_6.Add(sizer_11, 0, 0, 0)
        self.bookmate_rename_panel.SetSizer(sizer_6)
        sizer_13.Add(self.label_7, 0, 0, 0)
        sizer_13.Add(self.radio_btn_7, 0, 0, 0)
        sizer_13.Add(self.radio_btn_8, 0, 0, 0)
        sizer_13.Add(self.radio_btn_9, 0, 0, 0)
        sizer_12.Add(sizer_13, 0, 0, 0)
        sizer_12.Add(self.checkbox_8, 0, 0, 0)
        sizer_12.Add(self.button_4, 0, wx.ALIGN_RIGHT, 0)
        self.bookmate_same_name_panel.SetSizer(sizer_12)
        self.bookmate.AddPage(self.bookmate_config_panel, _("config"))
        self.bookmate.AddPage(self.bookmate_duplicate_panel, _("duplicate"))
        self.bookmate.AddPage(self.bookmate_rename_panel, _("rename"))
        self.bookmate.AddPage(self.bookmate_extract_panel, _("extract"))
        self.bookmate.AddPage(self.bookmate_same_name_panel, _("same name"))
        sizer_3.Add(self.bookmate, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_3)
        self.Layout()
        # end wxGlade

# end of class MyFrame1
class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_2 = MyFrame1(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_2)
        frame_2.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    gettext.install("BookMate") # replace with the appropriate catalog name

    BookMate = MyApp(0)
    BookMate.MainLoop()