# -*- coding: utf-8 -*-
import sys, urllib, urllib2, json

url = 'http://apis.baidu.com/apistore/stockservice/stock?stockid=sz002230'

url = 'http://apis.baidu.com/apistore/stockservice/stock?stockid=hk01211'

req = urllib2.Request(url)

req.add_header("apikey", "ed1b13437d191f4e7db9300cf3883421")
#req.add_header("apikey", "Äú×Ô¼ºµÄapikey")


resp = urllib2.urlopen(req)
content = resp.read()
if(content):
    print(content)