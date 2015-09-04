# -*- coding:utf-8 -*-
# file: MyFetion.py
# by Lee 2009-6-9
"""-----------------------------------------------------------------------------
 The API is offered by gohsy
 on https://fetionapi.appspot.com
 API Format:
  https://fetionAPI.appspot.com/api/?from=您手机号&pw=密码&to=接收方手机号&msg=短信内容
 前提是接收方已经是您的飞信好友
-----------------------------------------------------------------------------"""
import sys
import httplib
import urllib
import re
import time
class Fetion:
    """
        model to call fetionapi.
        attribute:url, fromTel, pwd, toTel, msg
        function:Trans, format_url, SendMsg
    """
    url = "https://fetionAPI.appspot.com/api/?from="
    def __init__(self,
                 toTel,
                 msg,
                 fromTel = '158xxxxxxxx',  # default my phone
                 pwd = 'xxxxxxxx'):
        self.fromTel = fromTel
        self.pwd = pwd
        self.toTel = toTel
        self.msg = self.Trans(msg)
    def Trans(self, msg):
        # change space to '%20', otherwise error raised
        return re.sub(" ", "%20", str(msg))
    def format_url(self):
        url_address = self.url + self.fromTel \
                      + "&pw=" + self.pwd \
                      + "&to=" + self.toTel \
                      + "&msg=" + self.msg
        return url_address
    def SendMsg(self):
        # call the api by http get method
        return urllib.urlopen(self.format_url())

def msg2log(msg):
    logfile = open('MyFetion.log', 'a')
    now = time.strftime('%Y%m%d %H:%M:%S')
    logfile.write('\n'+ now + '\n' + msg + '\n')
    logfile.close()

def main():
    # format mutual message
    print "\n" + " "*10 + "*"*60
    print " "*10 + " Personal Fetion"
    print " "*10 + " Enter the number and message what you want to send to."
    print " "*10 + " blank number means yourself,"
    print " "*10 + " and a blank message line to exit."
    print " "*10 + "*"*60
    # get the destination phone number
    toTel = raw_input("Input the target telphone number:")
    if toTel == "":
        toTel = "136xxxxxxxx"  # none input for a target most used
    # get the message and send by Fetion class
    while True:
        msg = raw_input("Message:")
        if msg == "":
            break  # none input to quit
        else:
            msg2log(msg)
            ff = Fetion(toTel, msg)
            answer = ff.SendMsg()
            #print answer
            print "Done.^_^\n"

if __name__ == '__main__':
    main()
