#!/usr/bin/python
# -*- coding: utf-8 -*-

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
