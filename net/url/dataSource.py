# coding=utf-8

try:
    # py3
    from urllib.request import Request, urlopen, URLError, HTTPError
    #from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen, URLError, HTTPError
    #from urllib import urlencode

import re
import sys

def dataFromUrl(url, waittime):
    import contextlib
    try:
        req = Request( url )
        with contextlib.closing( urlopen(req,timeout=waittime) ) as resp:  # HTTP Error 404: Not Found
            rslt = resp.read()
        '''
    except: HTTPError, e:
        print 'The server couldn\'t fulfill the request. Error code: , e.code
        ''' 
    except URLError, e:
        sys.stdout.write( 'except while access url:' + url + '\r\n' )
        if hasattr(e,"code"):                                                # HTTP Error 404: Not Found      
            sys.stdout.write( "The server couldn't fulfill the request. Error code:" + str(e.code) + '\r\n' )  #  + " Return content:" + e.read()
            if e.code==404:
                return 'url not found'
        #elif hasattr(e,"reason"):                                                # Errno 10054:连接被远端重置                          Errno 110] Connection timed out    10060：timeout
        sys.stdout.write( "Failed to reach the server.  The reason:" + str(e.reason) + '\r\n' )
        return ''
    except IOError, e:
        sys.stdout.write(  'except while access url:' + url + 'IOError: ' + str(e) + '\r\n' )
        return ''
    return rslt
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

def regDataFromUrl(url, waittime, formatStr):
    res = dataFromUrl(url, waittime)
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

