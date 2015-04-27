#!/bin/sh

all_lang="en cn"
dir=locale
potfile=messages.pot

mkdir -p $dir
pygettext -a $(find . -name '*.py')

# change below items in $dir/messages.pot: 
#	charset=gb2312
#	Content-Transfer-Encoding:utf8

cat $potfile | sed '1d' \
	| sed '/^# Copyright (C)/s/YEAR ORGANIZATION/2015/' \
	| sed '/^# FIRST AUTHOR <EMAIL@ADDRESS>/s/.*/# Chunis Deng <chunchengfh@gmail.com>/' \
	| sed '/^"Project-Id-Version:/s/PACKAGE VERSION/BookMate/' \
	| sed '/^"Last-Translator:/s/FULL NAME <EMAIL@ADDRESS>/Chunis Deng/' \
	| sed '/^"Language-Team:/s/LANGUAGE <LL@li.org>/Chunis Deng/' \
	| sed '/^"Content-Type:/s/charset=CHARSET/charset=utf-8/' \
	| sed '/^"Content-Transfer-Encoding/s/ENCODING/utf-8/' \
	> $potfile.tmp
mv $potfile.tmp $potfile

for x in $all_lang; do
	mkdir -p $dir/$x
	cp $potfile $dir/$x/$x-orig.po
	[ -f $dir/$x/$x.po ] || cp $dir/$x/$x-orig.po $dir/$x/$x.po
done

rm -f $potfile
# in each dir except en, merge changes from $dir/$x-orig.po to $dir/$x.po
