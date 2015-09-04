#!/usr/bin/env python  
#coding=utf8  
  
  
'''''Author: Zheng Yi 
Email: zhengyi.bupt@qq.com'''  
  
  
import urllib2  
import cookielib  
import threading  
import os  
import WeiboEncode  
import WeiboSearch  
import TextAnalyze  
  
  
pagesContent = []           #html content of downloaded pages  
textContent = []            #main text content of downloaded pages  
triedUrl = []               #all tried urls, including failed and success  
toTryUrl = []               #urls to be try  
failedUrl = []              #urls that fails to download  
  
  
class WeiboLogin:  
    "WeiboLogin class is for Weibo login, cookie, etc."  
      
    def __init__(self, user, pwd, enableProxy = False):  
        "Constructor of class WeiboLogin."  
  
        print "Initializing WeiboLogin..."  
        self.userName = user  
        self.passWord = pwd  
        self.enableProxy = enableProxy  
        print "UserName:", user  
        print "Password:", pwd  
          
        self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)&_=1329806375939"  
        self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.1)"  
        self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'}  
  
  
    def Login(self):  
        "Run this function to laungh the login process"  
      
        self.EnableCookie(self.enableProxy)  
          
        serverTime, nonce = self.GetServerTime()  
        postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce)  
        print "Post data length:\n", len(postData)  
  
        req = urllib2.Request(self.loginUrl, postData, self.postHeader)  
        print "Posting request..."  
        result = urllib2.urlopen(req)  
        text = result.read()  
        print "Post result page length: ", len(text)  
          
        try:  
            loginUrl = WeiboSearch.sRedirectData(text)  
            urllib2.urlopen(loginUrl)  
        except:  
            print 'Login error!'  
            return False  
              
        print 'Login sucess!'  
        return True  
  
           
    def GetServerTime(self):  
        "Get server time and nonce, which are used to encode the password"  
          
        print "Getting server time and nonce..."  
        serverData = urllib2.urlopen(self.serverUrl).read()  
        print serverData  
  
        try:  
                serverTime, nonce = WeiboSearch.sServerData(serverData)  
                return serverTime, nonce  
        except:  
                print 'Get server time & nonce error!'  
                return None  
  
  
    def EnableCookie(self, enableProxy):  
        "Enable cookie & proxy (if needed)."  
          
        cookiejar = cookielib.LWPCookieJar()  
        cookie_support = urllib2.HTTPCookieProcessor(cookiejar)  
  
        if enableProxy:  
            proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})  
            opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)  
            print "Proxy enabled"  
        else:  
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
  
        urllib2.install_opener(opener)  
  
  
class WebCrawl:  
    "WebCrawl class is for crawling the Weibo"  
  
    def __init__(self, beginUrl, maxThreadNum = 10, maxDepth = 2, thLifetime = 10, saveDir = "." +os.sep + "CrawledPages"):  
        "Initialize the class WebCrawl"  
          
        toTryUrl.append(beginUrl)  
        self.maxThreadNum = maxThreadNum  
        self.saveDir = saveDir  
        self.maxDepth = maxDepth  
        self.thLifetime = thLifetime  
  
        self.triedPagesNum = 0  
        self.threadPool = []  
  
        if not os.path.exists(self.saveDir):  
            os.mkdir(self.saveDir)  
  
        self.logFile = open(self.saveDir + os.sep + 'log.txt','w')  
  
  
    def Crawl(self):  
        "Run this function to start the crawl process"  
          
        global toTryUrl  
  
        for depth in range(self.maxDepth):  
            print 'Searching depth ', depth, '...'  
            self.DownloadAll()  
            self.UpdateToTry()  
  
  
    def DownloadAll(self):  
        "Download all urls in current depth"  
          
        global toTryUrl  
        iDownloaded = 0  
          
        while iDownloaded < len(toTryUrl):  
            iThread = 0  
            while iThread < self.maxThreadNum and iDownloaded + iThread < len(toTryUrl):  
                iCurrentUrl = iDownloaded + iThread  
                pageNum = str(self.triedPagesNum)  
                self.DownloadUrl(toTryUrl[iCurrentUrl], pageNum)  
  
                self.triedPagesNum += 1  
                iThread += 1  
                  
            iDownloaded += iThread  
              
            for th in self.threadPool:  
                th.join(self.thLifetime)  
                  
            self.threadPool = []  
              
        toTryUrl = []  
  
      
    def DownloadUrl(self, url, pageNum):  
        "Download a single url and save"  
          
        cTh = CrawlThread(url, self.saveDir, pageNum, self.logFile)  
        self.threadPool.append(cTh)  
        cTh.start()  
  
  
    def UpdateToTry(self):  
        "Update toTryUrl based on textContent"  
          
        global toTryUrl  
        global triedUrl  
        global textContent  
          
        newUrlList = []  
  
        for textData in textContent:  
            newUrlList += WeiboSearch.sUrl(textData)  
          
        toTryUrl = list(set(newUrlList) - set(triedUrl))  
        pagesContent = []  
        textContent = []  
  
  
class CrawlThread(threading.Thread):  
    "CrawlThread class is derived from threading.Thread, to create a thread."  
  
    thLock = threading.Lock()  
  
    def __init__(self, url, saveDir, pageNum, logFile):  
        "Initialize the CrawlThread"  
          
        threading.Thread.__init__(self)  
        self.url = url  
        self.pageNum = pageNum  
        self.fileName = saveDir + os.sep + pageNum + '.htm'  
        self.textName = saveDir + os.sep + pageNum + '.txt'  
        self.logFile = logFile  
        self.logLine = 'File: ' + pageNum + '  Url: '+ url    
  
  
    def run(self):  
        "rewrite the run() function"  
          
        global failedUrl  
        global triedUrl  
        global pagesContent  
        global textContent  
  
        try:  
            htmlContent = urllib2.urlopen(self.url).read()              
            transText = TextAnalyze.textTransfer(htmlContent)  
              
            fOut = open(self.fileName, 'w')  
            fOut.write(htmlContent)  
            fOut.close()  
            tOut = open(self.textName, 'w')  
            tOut.write(transText)  
            tOut.close()  
  
        except:  
            self.thLock.acquire()  
            triedUrl.append(self.url)  
            failedUrl.append(self.url)  
            sFailed = 'Failed!   ' + self.logLine  
            print sFailed  
            self.logFile.write(sFailed + '\n')  
            self.thLock.release()  
            return None  
          
        self.thLock.acquire()  
        pagesContent.append(htmlContent)  
        textContent.append(transText)  
        triedUrl.append(self.url)  
        sSuccess = 'Success!  ' + self.logLine  
        print sSuccess  
        self.logFile.write(sSuccess + '\n')  
        self.thLock.release()  
