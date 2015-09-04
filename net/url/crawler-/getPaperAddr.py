#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from sgmllib import SGMLParser
import re

class GetPaperAddr(SGMLParser):
  def reset(self):
    self.enter_div = False
    self.paper_addr = []
    SGMLParser.reset(self)

  def start_div(self, attrs):
    for k,v in attrs:
      if k == 'class' and v == 'page mb20 alR mt5':
        self.enter_div = True
        return

  def end_div(self):
    self.enter_div = False

  def start_a(self, attrs):
    if self.enter_div == True:
      for k,v in attrs:
        if k == "href":
          self.paper_addr.append(v)

  def printAddr(self):
    print "there are %d pages in this blog" % (self.getPaperNum())
    for i in self.paper_addr:
      print "address of page: " + i

  def getPaperNum(self):
    paper_num = 1;
    paper_index = []
    if len(self.paper_addr) == 0:
      return 1
    for i in self.paper_addr:
      regex = re.compile(r'html\?&p=(\d+)')
      paper_index = regex.search(i)
      if paper_index is None:
        return paper_num
      else:
        #print paper_index.group(1)
        if int(paper_index.group(1)) > paper_num:
          paper_num = int(paper_index.group(1))
    return paper_num
