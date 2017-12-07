__author__ = 'zhenghao'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TOOL:
    def __init__(self):
        self.removeBR = re.compile('<br>')
        self.removeHREF = re.compile('<a href=".*?>')
        self.removeA = re.compile('</a>')
        self.removeClass = re.compile('<a class=.*?>')

    def remove(self,string):
        string = re.sub(self.removeBR,"\n",string)
        string = re.sub(self.removeHREF,"",string)
        string = re.sub(self.removeA," ",string)
        string = re.sub(self.removeClass,"",string)
        return string.strip()

class BDTB:

    #定义类的初始化函数
    def __init__(self,baseUrl,seeLZ):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.stories = []
        self.Tool = TOOL();

    #获取指定页码的帖子信息
    def getPage(self,pageNum):
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"百度贴吧链接错误，原因是：", e.reason
                return None

    def getTitle(self):
        try:
            pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
            pageCode = self.getPage(1)
            result = re.search(pattern,pageCode)
            if result:
                return result.group(1)
            else:
                return None
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"获取标题错误，原因是：", e.reason
                return None
    def getPageNum(self):
        pattern = re.compile('<li class="l_reply_num".*?<span class="red">(.*?)</span>',re.S)
        pageCode = self.getPage(1)
        result = re.search(pattern,pageCode)
        if result:
            return result.group(1)
        else:
            return None

    def getPageStories(self,pageNum):
        pattern = re.compile('<div id="post_content_.*?<img class="BDE_Image.*?' +
                             '<br>(.*?)</div>',re.S)
        pageCode = self.getPage(pageNum)
        story = re.findall(pattern,pageCode)
        title = self.getTitle()
        file = open(title+'.txt','ab+')
        if pageNum==1:
            del story[0]
        for i in story:
            string = self.Tool.remove(i)
            file.write(string)
            file.write("\n\n***************************************\n\n")

    def getAllStories(self):
        num = int(self.getPageNum())
        for i in range(1,num+1,1):
             self.getPageStories(i)


baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL,1)
bdtb.getAllStories()

