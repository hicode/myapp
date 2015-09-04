#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sgmllib import SGMLParser

class GetWebContent(SGMLParser):
  def reset(self):
    self.enter_div = False
    self.getdata = False
    self.paper_addr = []
    SGMLParser.reset(self)
    self.contentCount = 0
    self.contentStart = 0
    self.contentEnd = 0
    self.getPagContent = False

    #content
    self.content = ""

    #paragraph list
    self.par = []

    #temporarily save content of one paragraph during analyzing process
    self.parText = ""

  def start_div(self, attrs):
    for k,v in attrs:
      if k == 'class' and v == 'gut_style img_resize':
        self.enter_div = True
        return

  def start_p(self, attrs):
    if self.getdata == True:
      self.getPagContent = True
      if len(self.parText) != 0:
        self.par.append(self.parText)
      self.parText = ""

  def end_p(self):
    self.getPagContent = False
    #print self.parText
    self.par.append(self.parText)
    self.parText = ""

  def handle_data(self, data):
    if self.getdata == True:
      #print "data" " + data
      self.parText += data

  def handle_comment(self, data):
    #print "handle_comment: " + data
    if self.enter_div == False or self.contentCount == 1:
      return
    if data.strip() == "HWDocContent":
      self.getdata = True
    elif data.strip() == "/HWDocContent":
      self.getdata = False
      self.contentCount = 1
    else:
      pass

  def get_content(self):
    for i in self.par:
      print i
      self.content = self.congtent + i + "\n"
      #print self.content
    return self.content

def test():
  open_file_abs_path = r"d:\123\download\设计之旅 应用设计模式增强代码的可扩展性、可维护性9.html"
  open_file_stream = open(open_file_abs_path.decode("utf-8"), "r")
  open_file_data = open_file_stream.read()
  open_file_stream.close()
  #print open_file_data

  getWebContentInstance = GetWebContent()
  getWebContentInstance.feed(open_file_data)

  #print getWebContentInstance.par
  print getWebContentInstance.get_content().decode()

if __name__ == "__main__":
  test()
