# coding=gbk
from sgmllib import SGMLParser

class URLLister(SGMLParser):
    def reset(self):                              
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):                     
        href = [v for k, v in attrs if k=='href'] 
        if href:
            self.urls.extend(href)

#getURL(url)用来将HTML中的url放入urls列表中
import urllib #, urllister'''
def getURL(url):
    try:
        usock = urllib.urlopen(url)
    except:
        print 'get url excepton'
        return []
    parser = URLLister() #urllister.URLLister()
    parser.feed(usock.read())
    usock.close()
    parser.close()
    urls = parser.urls
    return urls

#spider(startURL,depth)递归调用getURL(url)，startURL为起始URL，depth为递归次数，及遍历的深度

def spider(startURL, depth):
    i = 0
    global num      #num为全局变量，用来记录打印的url的数目
    if depth <= i:
       return 0
    else:
        urls = getURL(startURL)
        if len(urls) > 0:
            for url in urls:
                print url, num
                num = num + 1
                spider(url,depth - 1)
        else:
            return 0
    return 1

num = 0
#spider("http://www.xjtu.edu.cn/"%22,2)
spider("http://www.xjtu.edu.cn/", 2)

