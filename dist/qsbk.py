# coding=utf-8
__author__ = 'zhenghao'

import urllib
import urllib2
import re
import thread
import time

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        self.headers = {'User-Agent':self.user_agent}
        self.stories = []
        self.enable = False
    def getPage(self,pageIndex):
        try:
            url = "http://www.qiushibaike.com/hot/page/" + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"connect error, the reason is:",e.reason
                return None

    def getPageItems(self,pageIndex):

        #获得一整页的html信息
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "page load failed...."
            return None
        pattern = re.compile('<div class="article block untagged mb15 .*?'+
                             '<h2>\n(.*?)\n</h2>.*?<span>\n(.*?)\n</span>.*?'+
                             '<div class=(.*?)>',re.S)
        pageStories = []

        #获取一整页的关键信息，并返回[[作者，内容],......]
        items = re.findall(pattern,pageCode)
        for item in items:
            haveImg = re.search("thumb",item[2])
            if not haveImg:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR,"\n",item[1])
                pageStories.append([item[0].strip(),text.strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                #获取一整页的关键信息，并填充到stories
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            if input == "Q":
                self.enable = False
                return
            print "page:%d\tauthor:%s\tcontent:%s" %(page,story[0],story[1])

    def start(self):
        print u"Loading qsbk, press \"enter\" to display the new content; press \"Q\" to quit!"
        self.enable = True
        nowpage = 0
        while self.enable:
            self.loadPage()
            nowpage += 1
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                del self.stories[0]
                self.getOneStory(pageStories,nowpage)

spider = QSBK()
spider.start()









