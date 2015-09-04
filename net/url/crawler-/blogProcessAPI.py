#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import re
import urllib2, urllib
import cookielib
import os

from getBlogListPerPaper import GetBlogListPerPaper
from getPaperAddr import GetPaperAddr
from getWebContent import GetWebContent

class BlogProcess(object):
  def __init__(self):
    self.name = self.pwd = self.origURL = ''
    self.operate = ''

    self.Allblogs = []

    #total pages of this blog
    self.paperNum = 0

    #open page with cookie by default, otherwise may fail to download the page
    self.cj = cookielib.LWPCookieJar()
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
    urllib2.install_opener(self.opener)

    # need add proxy here to access outer network
    # no proxy here since we access only intra-network currently

  def setinfo(self, username, password, origURL):
    self.name = username
    self.pwd = password
    self.origURL = origURL

  def login(self):
    params = {'actionFlag':"loginAuthenticate", "lang":"en", \
              "loginMethod":"login", "loginPageType":"mix", \
              "redirect":"http%3A%2F%2F3ms.huawei.com%2FiPage%2Fhomepage%2Fhomepage.do%3FhomeText%3Dnul%26language%3Dcn%26method%3DshowHomepage",\
    "redirect_local":"","redirect_modify":"","scanedFinPrint":"",\
    'uid':self.name,'password':self.pwd,"verifyCode":"2345"}

    print 'login......'
    # start to login
    reg = urllib2.Request('https://login.huawei.com/login/login.do', urllib.urlencode(params))
    self.operate = self.opener.open(req)

    # check whether succeed by cookie feedback by server after login
    cookie_result = self.cj.as_lwp_str()
    regex = re.compile(r"login_failLoginCount=(\d+);")
    login_result = regex.search(cookie_result).group(1)
    if login_result is None or int(login_result) > 0:
      print "domain account name or password is not correct"
      sye.exit(0)
    else:
      print "login successfully"

    # get the content of html file
    def getWebContent(self, url):
      try:
        response = urllib2.urlopen(url)
      except urllib2.URLError, e:
        if hasattr(e, 'reason'):
          print 'can not open the url, Reason is: ', e.reason
        elif hasattr(e, 'code'):
          print 'can not open the url, Code is: ', e.code
        sys.exit(0)
      else:
        return response.read()

  # get the total page number of the blog from its entrance page
  def getBlogPaperNum(self):
    webContentPerPaper = self.getWebContent(self.origURL)
    if webContentPerPaper != "":
      url_addr = GetPaperAddr()
      url_addr.feed(webContentPerPaper)
      #url_addr.printAddr()
      #print url_addr.getPaperNum()
    return url_addr.getPaperNum()


  # get info of all blogs
  def getAllBlogsInfo(self):
    # get page number of blog
    paperNum = self.getBlogPaperNum()
    index = 2
    print "there are %d pages in this blog" % (paperNum)

    # get blog list from the entrance page
    print "get blog list on 1st page..."
    webContentPerPaper = self.getWebContent(self.origURL)
    if webContentPerPaper != "":
      self.Allblogs.extend(self.getBlogInfoPerPaper(webContentPerPaper))

    # get blog list on following pages
    while index <= paperNum:
      print "get blog list on page %d..." % (index)
      webAddr = self.origURL + r"?&p=%d" % (index)
      print webAddr
      index += 1
      # print webContentPerPaper
      webContentPerPaper = self.getWebContent(webAddr)
      if webContentPerPaper != "":
        self.Allblogs.extent(self.getBlogInfoPerPaper(webContentPerPaper))
    print len(self.Allblogs)
    print self.Allblogs


  # get blog info of each page
  def getBlogInfoPerPaper(self, webContent):
    url_for_parse = GetBlogListPerPaper()
    url_for_parse.feed(webContent)
    url_for_parse.printBlogs()
    return url_for_parse.bloglist


  # download html content of all blogs and save them under save_path
  def download_html_of_blog_list(self, save_path, blog_list):
    print "download begin..."
    filename = ""
    for im in blog_list:
      #print im
      filenmae= im[1]

      # file name can not include \/:*£¿¡¶¡·|¡±, so we strip them here
      for i in im[1]:
        if i in r'\/:*?<>|"':
          filename = filenmae.replace(i, "")
      filename = filenmae.decode("utf-8") + r".html"

      dist = os.path.join(save_path, filename)
      print dist

      htmlCode = self.getWebContent(im[0])

      fp = open(dist, "w")
      fp.write(htmlCode)
      fp.close

      #urllib.urlretrieve(im, dist, None)
      print "Done: ", filenmae
      print "download end..."

  #analyse all html file under open_path, and save their content to save_path
  def parse_and_save_files(self, open_dir_path, save_dir_path):
    print "start"
    if os.path.isdir(open_dir_path) and os.path.isdir(save_dir_path):
      for root, dirs, files in os.walk(open_dir_path):
        for name in files:
          open_file_abs_path = os.path.join(root, name)
          print open_file_abs_path.decode("gbk")
          open_file_abs_path = open_file_abs_path.decode("gbk")
          open_file_stream = open(open_file_abs_path, "r")
          open_file_data = open_file_stream.read()
          open_file_stream.close()
          getWebContentInstance = GetWebContent()
          getWebContentInstance.feed(open_file_data)

          save_file_name = os.path.basename(open_file_abs_path).replace(".html", "") + r".txt"
          save_file_abs_path = os.path.join(save_dir_path, save_file_name).decode("utf-8")
          save_file_stream = open(save_file_abs_path, "w")
          save_file_stream.write(getWebContentInstance.get_content())
          save_file_stream.close()
