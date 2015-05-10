#!/usr/bin/python

# frozen BookMate under Windows platform

import sys, os
import subprocess
import zipfile, shutil


root_path = '../..'
src_path = '../../src'
zipname = 'bookmate-win.zip'
pyi = r'C:\Python27\Scripts\pyinstaller'


def myunix2dos(ifile, ofile):
	write_to = open(ofile, 'w')
	lines = []

	for x in open(ifile):
		lines.append(x.strip() + '\n')

	write_to.writelines(lines)
	write_to.close()


cmd = [pyi, '-w', os.path.join(src_path, 'bookmate.py')]
try:
	subprocess.check_call(cmd)
except CalledProcessError:
	print "Error, run '%s' failed" %pyi
	sys.exit()

os.mkdir('dist/doc')
myunix2dos('../../doc/user_notes', 'dist/doc/user_notes.txt')
myunix2dos('../../README', 'dist/doc/README.txt')
shutil.copytree(os.path.join(src_path, 'images'),
		os.path.join('dist/bookmate/', 'images'))

if os.path.exists(zipname):
	os.remove(zipname)
os.rename('dist', 'bookmate-win')

# def zipdir(path, ziph):
# 	# ziph is zipfile handle
# 	for root, dirs, files in os.walk(path):
# 		for file in files:
# 			ziph.write(os.path.join(root, file))
#
# zipf = zipfile.ZipFile(zipname, 'w')
# zipdir('bookmate-win', zipf)
# zipf.close()
shutil.make_archive('bookmate-win', 'zip', 'bookmate-win')

# do some clean
shutil.rmtree('bookmate-win')
shutil.rmtree('build')
os.remove('bookmate.spec')
