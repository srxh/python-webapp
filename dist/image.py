import urllib
import urllib2
import re
import os

class IMAGE:
	def __init__(self,baseUrl,seeLZ):
		self.baseUrl = baseUrl
		self.seeLZ = '?see_lz=' + str(seeLZ)

	def getPageCdoe(self,pageNum):
		try:
			url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			#print response.read().decode('utf-8')
			return response.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print u"connect failed, the reason is:", e.reason
				return None

	def getPageNums(self):
		pageCode = self.getPageCdoe(1)
		pattern = re.compile('<span class="red">(\d)</span>', re.S)
		pageNum = re.search(pattern, pageCode)
		return pageNum.group(1)

	def imageSave(self,imageUrl,imageName):
		url = urllib.urlopen(imageUrl)
		data = url.read()
		f = open(imageName, 'wb')
		f.write(data)
		f.close()

	def mkdir(self,path):
		path = path.strip()
		isExists = os.path.exists(path)
		if not isExists:
			os.makedirs(path)
			return True
		else:
			return False

	def saveAllImage(self):
		pattern = re.compile('<img class="BDE_Image" src="(.*?)"',re.S)
		pageNums = int(self.getPageNums())
		fileName = 0
		for i in range(1, pageNums + 1,1):
			path = '%d' %i
			self.mkdir(path)
			fileName = 0
			pageCode = self.getPageCdoe(i)
			imagAddrList = re.findall(pattern,pageCode)
			for item in imagAddrList:
				fileName += 1
				str = '%d' %fileName
				temp = path + '/' + str + '.jpg'
				self.imageSave(item, temp)
				print "save %s ..." %temp

baseUrl = "http://tieba.baidu.com/p/3138733512"
image = IMAGE(baseUrl,1)
image.saveAllImage()






