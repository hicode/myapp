# coding=utf-8

try:
    # py3
    from urllib.request import Request, urlopen
    #from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    #from urllib import urlencode

import re

def dataFromUrl(url):
    req = Request( url )
    resp = urlopen(req)
    return resp.read()
    '''
    import pycurl
    import StringIO
     
    crl = pycurl.Curl()
    crl.setopt(pycurl.VERBOSE,1)
    crl.setopt(pycurl.FOLLOWLOCATION, 0)
    crl.setopt(pycurl.MAXREDIRS, 5)
    crl.fp = StringIO.StringIO()
    crl.setopt(pycurl.URL, url)
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
    crl.perform()
    return crl.fp.getvalue()
    '''

def regDataFromUrl(url, formatStr):
    req = Request( url )
    resp = urlopen(req)
    res = resp.read().strip()
    return re.findall( formatStr, res )

    lines=str(resp.read().strip()).split('\n')
    r=[]
    # 港股查询结果格式不同
    for ln in lines:
        data=ln.split('"')[1].split(",")
        r.append({})
        i=0
        for k in itemLst:
            r[-1][k]=data[i]
            i=i+1
    return r
    #return str(resp.read().decode('utf-8').strip())

