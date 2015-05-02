#!/usr/bin/python

import sys, os
import wx

#import thread
#thread.start_new(real_find, ())


def get_config_file_name(basename):
	return os.path.join(os.path.expanduser(os.environ['USER']), basename)


# restore saved configs
def read_from_config(file):
	try:
		cfg_file = open(file, 'r')
	except IOError, msg:  # set default values
		tmp_dir = dirname = ''
		type = '*'
		recu = 0
	else:  # read the config file
		cfg = {}
		line = cfg_file.readline().rstrip()
		while line:
			options = line.split('=')
			try:
				cfg[options[0]] = options[1]
			except IndexError:
				pass
			line = cfg_file.readline().rstrip()
		cfg_file.close()
		tmp_dir = dirname = cfg.get('dir', '')
		type = cfg.get('type', '*')
		recu = int(cfg.get('recu', 0))
		cfg_file.close()
	return (tmp_dir, type, recu)

def write_to_config(epath, etype, var, cfgfile):
	try:
		cfg_file = open(file, 'w')
	except IOError, msg:
		pass
	else:
		if not os.path.isdir(epath):
			epath = ''
		cfg_file.write('dir=%s\n' %epath)
		cfg_file.write('type=%s\n' %etype)
		cfg_file.write('recu=%s\n' %var)
		cfg_file.close()


def test_config():
	pass


class pyConfig(wx.Panel):
	def __init__(self, parent=None, id=-1, tty=sys.stdout):
		wx.Panel.__init__(self, parent, id)
		#self.SetBackgroundColour('White')
		self.create_widgets()

	def create_widgets(self):
		wx.StaticText(self, -1, 'Not implemented yet...', pos=(120, 80))


class testFrame(wx.Frame):
	def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
		wx.Frame.__init__(self, parent, -1, pos=pos, size=size)
		self.panel = pyConfig(self)

class MyApp(wx.App):
	def OnInit(self):
		self.frame = testFrame(pos=(300,120), size=(320, 200))
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True


if __name__ == '__main__':
	# test_config()
	myapp = MyApp()
	myapp.MainLoop()
