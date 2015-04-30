#!/usr/bin/python

import webbrowser


amazon_url = 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords='
douban_url = 'http://book.douban.com/subject_search?search_text='

def search_in_web(web_url, search_str):
	search_str = search_str.replace(' ', '+')
	search_str = search_str.replace('-', '+')
	search_str = search_str.replace('_', '+')

	# Open URL in a new tab
	webbrowser.open_new_tab(web_url + search_str) # opens in default browser

def search_in_amazon(str):
	search_in_web(amazon_url, str)

def search_in_douban(str):
	search_in_web(douban_url, str)


if __name__ == '__main__':
	search_str = 'Learn Python'
	search_in_web(amazon_url, search_str)
	search_in_web(douban_url, search_str)
