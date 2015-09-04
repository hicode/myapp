#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from sgmllib import SGMLParser

class GetBlogListPerPaper(SGMLParser):
  def reset(self):
    self.enter_dl = False
    self.enter_dt = False
    self.blogfeature = []
    self.bloglist = []
    SGMLParser.reset(self)

  def start_dl(self, attrs):
    for k,v in attrs:
      if k == 'class' and v == 'list_dl':
        self.enter_dl = True
        return

  def end_dl(self):
      self.enter_dl = False

  def start_dt(self, attrs):
    if self.enter_dl == True:
      self.enter_dt = True

  def end_dt(self):
    self.enter_dt = False

  def start_a(self, attrs):
    self.blogfeature = []

    #print attrs
    if self.enter_dt == False:
      return
    for k,v in attrs:
      if k == 'href' and v.startswith("http"):
        self.blogfeature.append(v)
        continue
      if k == "title":
        self.blogfeature.append(v.encode("UTF-8"))
        continue
    if len(self.blogfeature) == 2:
      self.bloglist.append(self.blogfeature)

  def printBlogs(self):
    print "this page includes %d articles" % len(self.bloglist)
    for i in self.bloglist:
      print "url: ".decode("UTF-8") + i[0].decode("UTF-8")
      #print "title of article: ".decode("UTF-8") + i[1].decode("UTF-U")
      print "title of article: " + i[1]
