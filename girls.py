from random import randint
from urllib.parse import quote, unquote
import os
import os.path

rootdir = 'girl'

class Girls():
	def __init__( self ):
		self.contents = []

	def getContent(self, content):
		for parent,dirnames,filenames in os.walk(rootdir):
			count = len(dirnames)
			if count > 0:
				dirname = dirnames[randint(0,count-1)]
				with open('%s/%s/个人简介.txt' % (rootdir, dirname), 'r') as file_object:
					pic_url = 'http://hin.wechat.3w.dkys.org/girl/{name}.jpg'.format(name=quote(dirname))
					news = {}
					news['type'] = 'news'
					news['title'] = dirname
					news['pic_url'] = pic_url
					news['content'] = file_object.read()
					news['url'] = pic_url
					self.contents.append(news)

		return self.contents
