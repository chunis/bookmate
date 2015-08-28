#!/usr/bin/python
#
# Copyright (C) 2015, Chunis Deng (<chunchengfh@gmail.com>)
#
# This file is part of BookMate and is released under the terms of
# GNU GPLv3 License, see doc/LICENSE for details.
#

import subprocess
import os, time
import shutil
import patoolib

TMP_DIR = "bookmate_tmp"

archive_suffix = ['.rar', '.zip', '.7z', '.tar', '.gz', '.tgz', '.tar.gz', 'xz', '.bz2']


def unpack_file(zipfile, outpath='.'):
	tmpdir = os.path.join(outpath, TMP_DIR)
	try:
		if not os.path.exists(outpath):
			os.mkdir(outpath)
		os.mkdir(tmpdir)
	except OSError, e:
		print "mkdir %s failed: %s" %(tmpdir, str(e))
		return -1

	try:
		patoolib.extract_archive(zipfile, outdir=tmpdir)
	except patoolib.PatoolError:
		# TODO: mark zipfile in RED
		print "unpack file %s failed!" %zipfile
		return -1
	else:
		all_files = os.listdir(tmpdir)
		if len(all_files) == 1:
			shutil.move(os.path.join(tmpdir, all_files[0]), outpath)
			os.rmdir(tmpdir)
		elif len(all_files) > 1:
			barename = os.path.basename(zipfile)
			for suffix in archive_suffix:
				barename = barename.split(suffix)[0]
			newdir = os.path.join(outpath, barename)
			os.rename(tmpdir, newdir)
	return 0


# Let's test it:
if __name__ == '__main__':
	#unpack_file("test.gz", 'mydir')
	unpack_file("test.tar.gz", 'mydir')
	#unpack_file("test.rar", 'mydir')
	#unpack_file("test.7z", 'mydir')


