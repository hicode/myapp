try:
    # py3
    from urllib.request import Request, urlopen
    #from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    #from urllib import urlencode


import re

def getWebInfo(url, symbol, formatStr, itemLst):
    req = Request( url + symbol )
    return re.findall( formatStr, urlopen(req) )

    resp = urlopen(req)
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

def getSSEProdLst:
    svr = r'http://www.sse.com.cn/js/common/ssesuggestdata.js'  # ({val:"600000",val2:"浦发银行",val3:"pfyx"})
    formatStr = r'[(]{(.*)}[)]'
    result = _request(url, stockLst, formatStr, _itemLst)
    for prod in result:
        prod.split(',')

def getAStockRealtime(stockLst):
    svr = r'http://hq.sinajs.cn/list='  
    formatStr = r'[(]{(.*)}[)]'
    result = _request(url, stockLst, formatStr, _itemLst)
    for prod in result:
        prod.split(',')
