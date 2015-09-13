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
	title, author, isbn, date = None, None, None, None

	if os.path.exists(name):
		try:
			ebook = SimpleEPUB(path=name)
			title = ebook.title
			isbn = ebook.identifier
			author = ebook.author
			date = ebook.date
		except:
			pass
	return title, author, isbn, date


if __name__ == '__main__':
	info = get_epub_info("cc.epub")
	for x in info:
		print x
