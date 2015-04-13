#!/usr/bin/python
# -*- coding: gb2312 -*-

# About: the backend of PyFind and NPyFind

import os, sys
import glob, shutil, thread

Name	= 'PyFind'
Author	= 'Deng Chunhui'
Email	= 'chunchengfh@gmail.com'
Version	= '0.0.1'
Date	= '2008.05.19'

result = [ ]  # used for store result 
dirnames = [ ] # used for store old dirs


def myhelp(name=Name):
	return (name + ' can find a certain type of files \nin a '
			+ 'certain directory by regular express search')


def myabout(name=Name, version=Version, date=Date):
	return (name 	+ '\nThis is another PyFind implemented by WxPython'
			+ '\n\nVersion: ' + version
			+ '\n Author: ' + Author 
			+ '\n Email: ' + Email 
			+ '\n Date:\t' + date)


def get_config_file(basename):
	if sys.platform == 'linux2':
#		return '~/.pyfind.cfg'
		return os.path.join(os.environ['HOME'], basename)
	else:
		return os.path.join(os.getcwd(), basename)


# restore saved configs
def get_config(file):
	try:
		cfg_file = open(file, 'r')
	except IOError, msg:
		tmp_dir = dirname = ''
		type = '*'
		recu = 0
	else:
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


def save_config(epath, etype, var, cfgfile):
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


def recufind(path, allpath, file, result, find_flag):
	if find_flag == False:
		return

	os.chdir(path)
	books=glob.glob(file)
	for book in books:
		result.append(allpath + '/' + book)
#		print path + '/' + book
	for filepath in os.listdir('.'):
		if os.path.isdir(filepath):
			recufind(filepath, allpath+'/'+filepath, file)
	os.chdir('..')

def myFind(find_flag):
	if find_flag == True:
		find_flag = not find_flag
	else:
		prepare_find()


def prepare_find(dirname):
	if not os.path.isdir(dirname):
		return

	thread.start_new(real_find, ())


def real_find(dirname, dirnames, type, ekeyword, recu, result, find_flag):
	find_flag = True
	if dirname not in dirnames:
#		dirnames.append(dirname)
		dirnames[:0] = [ dirname ]
	os.chdir(dirname)
	keywords = ekeyword.encode('gbk')
	file = '*' + keywords + '*.' + type

	result = [ ]
	books=glob.glob(file)
	for book in books:
		result.append(book)
#		print book

	if recu == 1:
		for filepath in os.listdir('.'):
			if os.path.isdir(filepath):
				recufind(filepath, filepath, file)
	
	if find_flag == True:
		find_flag = False
	


# test
if __name__ == '__main__':
	file = get_config_file('.pyfind.cfg')
	print file
	print get_config(file)

	save_config('/home/denny/sunny', 'pdf', 0, file)
	print get_config(file)

	save_config('/home/denny/sunny/npyfind/bck', 'py', 1, file)
	print get_config(file)

