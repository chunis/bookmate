#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import shutil
from thirdparty import desktop

OPEN_FILE_FLAG = 1
OPEN_DIR_FLAG = 1

def openfile(file):
	desktop.open(file)

def copyfile(src, dst):
	shutil.copy(src, dst)

def movefile(src, dst):
	shutil.move(src, dst)
