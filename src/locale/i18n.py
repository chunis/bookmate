#!/usr/bin/python

import gettext

gettext.install('lang', './locale', unicode=False)
#gettext.translation('lang', './locale', languages=['en']).install(True)
gettext.translation('lang', './locale', languages=['cn']).install(True)
  
print _("Hello world")
