#!/bin/sh

# About: update xx/LC_MESSAGES/lang.mo file based on xx/xx.po (xx = en/cn)

all_lang="en cn"
dir=locale

for x in $all_lang; do
	mkdir -p $dir/$x/LC_MESSAGES
	if [ -f $dir/$x/$x.po ]; then  # update po file
		msgfmt -o $dir/$x/LC_MESSAGES/lang.mo $dir/$x/$x.po
	fi
done
