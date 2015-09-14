#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import os
from yael import SimpleEPUB


def get_epub_info(name):
	title, press, isbn, date = None, None, None, None

	if os.path.exists(name):
		try:
			ebook = SimpleEPUB(path=name)
			title = ebook.title
			press = ebook.publisher
			isbn = ebook.identifier
			date = ebook.date
		except:
			print "failed in get_epub_info()"

	return title, press, isbn, date


if __name__ == '__main__':
	info = get_epub_info("cc.epub")
	for x in info:
		print x
