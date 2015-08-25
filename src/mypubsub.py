#!/usr/bin/python
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

# http://wiki.wxpython.org/WxLibPubSub
try:
	from wx.lib.pubsub import Publisher as pubsub
	pub_version = "version_1"
except ImportError:
	import wx.lib.pubsub.setupkwargs
	from wx.lib.pubsub import pub as pubsub
	pub_version = "version_3"


subscribe = pubsub.subscribe

if pub_version == "version_1":
	def sendMessage(msg_str, msg=""):
		return pubsub.sendMessage(msg_str, msg)
elif pub_version == "version_3":
	def sendMessage(msg_str, msg=""):
		return pubsub.sendMessage(msg_str, msg=msg)
