#!/bin/sh

# frozen BookMate under Linux platform


src=../../src
dist=bookmate-linux.tar.gz

#pyinstaller -w -i $src/images/bookmate.ico $src/bookmate.py
pyinstaller -w $src/bookmate.py
cp -r $src/images dist/bookmate/
rm -rf build bookmate.spec

mkdir -p dist/doc
cp -r $src/../doc/user_notes dist/doc
cp -r ../../README dist/doc

rm -f $dist
mv dist bookmate-linux
tar czf $dist bookmate-linux
rm -rf bookmate-linux
