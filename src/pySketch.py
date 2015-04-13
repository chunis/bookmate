#!/usr/bin/python

import sys
import wx


class pySketch(wx.Panel):
	def __init__(self, parent=None, id=-1, tty=sys.stdout):
		wx.Panel.__init__(self, parent, id)
		#self.SetBackgroundColour('White')
		self.create_widgets()

	
	def create_widgets(self):
		wx.StaticText(self, -1, 'Not implemented yet...', pos=(120, 80))


class testFrame(wx.Frame):
	def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
		wx.Frame.__init__(self, parent, -1, pos=pos, size=size)
		self.panel = pySketch(self)

class MyApp(wx.App):
	def OnInit(self):
		self.frame = testFrame(pos=(300,120), size=(320, 200))
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True


if __name__ == '__main__':
	myapp = MyApp()
	myapp.MainLoop()
