#!/usr/bin/env python  
#coding=utf8  
  
  
'''''Author: Zheng Yi 
Email: zhengyi.bupt@qq.com'''  
  
  
import WeiboCrawl  
  
    
if __name__ == '__main__':  
    weiboLogin = WeiboCrawl.WeiboLogin('13012866991', 'cccccc66')  
    if weiboLogin.Login() == True:  
        print "The WeiboLogin module works well!"
      
    #start with my blog :)  
    webCrawl = WeiboCrawl.WebCrawl('http://weibo.com/yaochen')  
    webCrawl.Crawl()  
    del webCrawl  
