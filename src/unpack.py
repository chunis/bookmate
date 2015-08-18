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

UNPACK_LOG = "unpack.log"
TMP_DIR = "bookmate_tmp"

def unpack_file(zipfile, outpath='.', tool='patool'):
	tmpdir = os.path.join(outpath, TMP_DIR)
	try:
		if not os.path.exists(outpath):
			os.mkdir(outpath)
		os.mkdir(tmpdir)
	except OSError, e:
		print "mkdir %s failed: %s" %(tmpdir, str(e))
		return -1

	try:
		cmd = [tool, "extract", "--outdir", tmpdir, zipfile]
		#print 'cmd:', cmd
		subprocess.check_output(cmd)
	except OSError:
		print 'Got OSERROR'
	except subprocess.CalledProcessError as e:
		print "unpack_file() failed!"
		fl = open(UNPACK_LOG, 'a')
		fl.write('\n------' + time.asctime() + '------\n')
		for c in cmd:
			fl.write("%s " %c)
		fl.write('\n')
		fl.write(e.output)
		fl.write("\n")
		fl.flush()
		fl.close()
		return -1
	else:
		all_files = os.listdir(tmpdir)
		if len(all_files) == 1:
			shutil.move(os.path.join(tmpdir, all_files[0]), outpath)
			os.rmdir(tmpdir)
		elif len(all_files) > 1:
			# TODO: strip sufix such as 'tar.gz' or 'rar'
			newdir = os.path.join(outpath, os.path.basename(zipfile))
			os.rename(tmpdir, newdir)
	return 0


# Let's test it:
if __name__ == '__main__':
	#unpack_file("test.gz", 'mydir')
	unpack_file("test.tar.gz", 'mydir')
	#unpack_file("test.rar", 'mydir')
	#unpack_file("test.7z", 'mydir')


