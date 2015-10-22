from django.db import models

# Create your models here.
from django.contrib import admin
from _mysql import NULL
from django.db.models.fields.related import ForeignKey
#???from coverage import start
from numpy import maximum
#from untws.instrument import Stock
from pandas.io.wb import country_codes
from apptools.type_registry.tests.dummies import Abstract

# Create your models here.
class Market(models.Model):     
    name = models.CharField(max_length=8, unique=True)
    currency = models.CharField(max_length=3)     
    def __str__(self):
        return self.name
#    class admin:
#        pass

class Product(models.Model):
    source = models.CharField(max_length=8)  # 'dzh', 'szse.sse'
    code = models.CharField(max_length=8)
    market = models.CharField(max_length=8)
    submarket = models.CharField(max_length=8, null=True)
    #market = models.ForeignKey(Market)     
    name = models.CharField(max_length=16)     
    type = models.CharField(max_length=1, null=True)  # stock / fund / warrant / structuredFund/ option 
    #bDataHist = models.BooleanField()
    dateHistEnd = models.DateField(null=True)
    dateHistBegin = models.DateField(null=True)
    dateTickEnd = models.DateField(null=True)
    dateTickBegin = models.DateField(null=True)
    dateMinuteEnd = models.DateField(null=True)
    dateMinuteBegin = models.DateField(null=True)
    maskSite = models.CharField(max_length=64)  # 缺乏此product数据的网站，如很多创业板等很多指数在yahoo没有，以.分隔
    errInfo = models.CharField(max_length=32, null=True)
    ratioFrwdBegin = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # change percent
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    class Meta:
        unique_together = ('code', 'market')
#    class admin:
#        pass

class Product_(models.Model):
    source = models.CharField(max_length=8)  # 'dzh', 'szse.sse'
    code = models.CharField(max_length=8)
    market = models.CharField(max_length=8)
    submarket = models.CharField(max_length=8, null=True)
    #market = models.ForeignKey(Market)     
    name = models.CharField(max_length=16)     
    type = models.CharField(max_length=1)  # stock / fund / structuredFund / deriative:: warrant / option 
    #bDataHist = models.BooleanField()
    dateHistEnd = models.DateField(null=True)
    dateHistBegin = models.DateField(null=True)
    dateTickEnd = models.DateField(null=True)
    dateTickBegin = models.DateField(null=True)
    dateMinuteEnd = models.DateField(null=True)
    dateMinuteBegin = models.DateField(null=True)
    errInfo = models.CharField(max_length=32, null=True)
    maskSite = models.CharField(max_length=64)  # 缺乏此product数据的网站，如很多创业板等很多指数在yahoo没有，以.分隔
    ratioFrwdBegin = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # change percent
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    class Meta:
        unique_together = ('source', 'code', 'market')


class ProductConcept(models.Model):
    product = models.ForeignKey(Product)     
    groupName = models.CharField(max_length=8)
    groupDesc = models.CharField(max_length=32)
    class Meta:
        unique_together = ('product', 'groupName')

class ProductInfo(models.Model):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.OneToOneField(Product)     
    companyName = models.CharField(max_length=32)     
    IPOShares = models.DecimalField(max_digits=16, decimal_places=0)
    IPOPrice = models.DecimalField(max_digits=8, decimal_places=3)
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    #class Meta:
    #    unique_together = ('code', 'market')

class BigTrade(models.Model):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.ForeignKey(Product)     
    buyer = models.CharField(max_length=32)     
    shares = models.DecimalField(max_digits=16, decimal_places=0)
    price = models.DecimalField(max_digits=8, decimal_places=3)
    date = models.DateField() 
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    class Meta:
        unique_together = ('product', 'buyer', 'date')

bigone={} # 社保 QFII 阿里 百度 腾讯 

class ProductFinacialRpt(models.Model):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.ForeignKey(Product, unique_for_date='date')     
    date = models.DateField() 
    earnings = models.DecimalField(max_digits=16, decimal_places=0)
    bookVal = models.DecimalField(max_digits=16, decimal_places=0)
    sales = models.DecimalField(max_digits=16, decimal_places=0)
    totalShares = models.DecimalField(max_digits=16, decimal_places=0)
    totalHolder = models.DecimalField(max_digits=16, decimal_places=0)
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
#    class admin:
#        pass

class ProductWeight(models.Model):   # 拆细信息是否会在权息文件中？
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.ForeignKey(Product, unique_for_date='date')     
    date = models.DateField()
    bonus = models.DecimalField(max_digits=8, decimal_places=3)
    giftStck = models.DecimalField(max_digits=4, decimal_places=2)
    incrStck = models.DecimalField(max_digits=4, decimal_places=2)
    sellStck = models.DecimalField(max_digits=4, decimal_places=2)
    p4SellStck = models.DecimalField(max_digits=8, decimal_places=3)
    freeStck = models.DecimalField(max_digits=16, decimal_places=0)
    totalStck = models.DecimalField(max_digits=16, decimal_places=0)
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    class Meta:
        unique_together = ('product', 'date')
#    class admin:
#        pass

class ProductData(models.Model):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.ForeignKey(Product, unique_for_date='date')     
    date = models.DateField() 
    marginBuy = models.DecimalField(max_digits=16, decimal_places=0)
    marginPay = models.DecimalField(max_digits=16, decimal_places=0)
    marginAmt = models.DecimalField(max_digits=16, decimal_places=0)
    shortSell = models.DecimalField(max_digits=16, decimal_places=0)
    shortPay = models.DecimalField(max_digits=16, decimal_places=0)
    shortVol = models.DecimalField(max_digits=16, decimal_places=0)
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    class Meta:
        unique_together = ('product', 'date')

class ProductIdx(models.Model):              # cci, boll, rsi, kdj, psy,  sma, macd, 
    product = models.ForeignKey(Product, unique_for_date='date')     
    date = models.DateField() 
    cci = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    psy = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    class Meta:
        unique_together = ('product', 'date')

# watchreason
class WatchList(models.Model):
    product = models.OneToOneField(Product)     
    watchReason = models.CharField(max_length=256)     
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
#    class admin:
#        pass

class _KNoId(models.Model):
    p = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # previous close
    o = models.DecimalField(max_digits=8, decimal_places=3)
    h = models.DecimalField(max_digits=8, decimal_places=3)
    l = models.DecimalField(max_digits=8, decimal_places=3)
    c = models.DecimalField(max_digits=8, decimal_places=3)
    kt = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    chngPerc = models.DecimalField(max_digits=7, decimal_places=3, null=True)  # change percent
    r_kt = models.DecimalField(max_digits=2, decimal_places=0, null=True)  # r_:: relative / reference product
    r_chngPerc = models.DecimalField(max_digits=7, decimal_places=3, null=True)  # change percent
    adjC = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # adjusted close
    ratioFrwd = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # change percent
    ratioBack = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # change percent
    amt = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    vol = models.DecimalField(max_digits=16, decimal_places=0)
    class Meta:
        abstract = True

class _KD(_KNoId):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.ForeignKey(Product) #, unique_for_date='date')     
    date = models.DateField() 
    pDate = models.DateField(null=True) 
    class Meta:
        unique_together = ('product', 'date')
        abstract = True
    def __str__(self):
        return '%s.%s %s' % (self.code, self.market, self.date)

class productPosition(models.Model):
    product = models.ForeignKey(Product, unique=True) #, unique_for_date='date')     

    h3Mon = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    hD3M = models.DateField(null=True) 
    l3Mon = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    lD3M = models.DateField(null=True) 

    hYear = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    hDY = models.DateField(null=True) 
    lYear = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    lDY = models.DateField(null=True) 

    h2Year = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    hD2Y = models.DateField(null=True) 
    l2Year = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    lD2Y = models.DateField(null=True) 

    h3Year = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    hD3Y = models.DateField(null=True) 
    l3Year = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    lD3Y = models.DateField(null=True) 

    c = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    per2H = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # change percent, H = max(h3mon, hYear), h-c/c
    per2L = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # change percent, L = max(l3mon, lYear), c-l/l
    vSinceH = models.DecimalField(max_digits=16, decimal_places=0, null=True)   #  latest H
    vSinceL = models.DecimalField(max_digits=16, decimal_places=0, null=True)   #  latest L

class _KT(_KNoId):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.ForeignKey(Product) #, unique_for_date='date')     
    date = models.DateField() 
    dt = models.DateTimeField() 
    pDt = models.DateTimeField(null=True) 
    class Meta:
        unique_together = ('product', 'dt')
        abstract = True
    def __str__(self):
        return '%s.%s %s' % (self.code, self.market, self.date)


class _KDaily(_KD):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    '''
    product = models.ForeignKey(Product) #, unique_for_date='date')     
    p = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # previous close
    o = models.DecimalField(max_digits=8, decimal_places=3)
    h = models.DecimalField(max_digits=8, decimal_places=3)
    l = models.DecimalField(max_digits=8, decimal_places=3)
    c = models.DecimalField(max_digits=8, decimal_places=3)
    chngPerc = models.DecimalField(max_digits=7, decimal_places=3, null=True)  # change percent
    adjC = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # adjusted close
    amt = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    vol = models.DecimalField(max_digits=16, decimal_places=0)
    date = models.DateField() 
    pDate = models.DateField(null=True)
    ''' 
    weekday = models.DecimalField(max_digits=1, decimal_places=0, null=True)
    week = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    month = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    year = models.DecimalField(max_digits=4, decimal_places=0, null=True)
    class Meta(_KD.Meta):
        abstract = True

class KDaily(_KDaily):  ## _XXY   XX-country(CN/HK/US)  Y-type(Idx/Stock/Fund/Deriative)  
    pass

class KDaily_CNS(_KDaily):   #     CNS: newly imported data; 　　CNS_: hist data; CNS_Tmp: 　　　adjusted price for analyse 
    pass

class KDaily_CNS_(_KDaily):   ##       
    pass

class KDaily_CNS_Tmp(_KDaily):   ##       
    pass

class KDaily_CNI(_KDaily):   ##       
    pass

class KDaily_CNF(_KDaily):   ##       
    pass

class KDaily_HKS(_KDaily):   ##       
    pass

class KDaily_HKS_(_KDaily):   ##       
    pass

class KDaily_HKS_Tmp(_KDaily):   ##       
    pass

class KDaily_HKI(_KDaily):   ##       
    pass

class KDaily_HKF(_KDaily):   ##       
    pass

class KDaily_HKD(_KDaily):   ##       
    pass


# 拆表方案： 拆后A股少1/3仍近千万条，再拆中小/创业？


class seqDate(models.Model):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.ForeignKey(Product) #, unique_for_date='date')     
    date = models.DateField() 
    pDate = models.DateField(null=True) 
    class Meta:
        unique_together = ('product', 'date')

class kDate(models.Model):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.ForeignKey(Product) #, unique_for_date='date')     
    date = models.DateField() 
    class Meta:
        unique_together = ('product', 'date')


class KMonth(_KD):
    hDate = models.DateField() 
    lDate = models.DateField() 

class KWeek(_KD):
    hDate = models.DateField() 
    lDate = models.DateField() 

class KMin(_KT):
    #date = models.DateTimeField()   # Django 中，重写 Field 实例是不允许的(至少现在还不行)。如果基类中有一个 author 字段，你就不能在子类中创建任何名为 author 的字段
    #minute = models.DateTimeField() 
    #pMinute = models.DateTimeField(null=True) 
    class Meta:
        pass
        # unique_together = ('product', 'date',' minute')
    def __str__(self):
        return '%s.%s %s %s' % (self.code, self.market, self.date, self.minute)

'''
class prodHistCheck(models.Model):
    code = models.CharField(max_length=8)     
    market = models.CharField(max_length=8)     
    #date = models.DateField()
    dataItem = models.CharField(max_length=8)  # k line / minK / idx / 
    def __str__(self):
        return '%s.%s %s %s' % (self.code, self.market, self.date, self.dataItem)
'''

'''
Do Django models support multiple-column primary keys?¶
No. Only single-column primary keys are supported.
But this isn’t an issue in practice, because there’s nothing stopping you from adding other constraints (using the unique_together model option or creating the constraint directly in your database), 
'''


################### realtime
class TradeRealTime(models.Model):             # o/h/l/vol for k-line is null, product_id+dt may be not unique
    product = models.ForeignKey(Product) #, unique_for_date='date')     
    date = models.DateField() 
    p = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # previous close
    c = models.DecimalField(max_digits=8, decimal_places=3)
    chngPerc = models.DecimalField(max_digits=7, decimal_places=3, null=True)  # change percent
    adjC = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # adjusted close
    ratioFrwd = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # change percent
    ratioBack = models.DecimalField(max_digits=8, decimal_places=3, null=True)  # change percent
    amt = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    vol = models.DecimalField(max_digits=16, decimal_places=0)
    dt = models.DateTimeField() 
    pDt = models.DateTimeField(null=True) 

    changeSpeedMin = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    changeSpeed5Min = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    dealNum = models.DecimalField(max_digits=8, decimal_places=0)
    direction = models.BooleanField()   # buy--true sell--false
    buy0 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy1 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy2 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy3 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy4 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy5 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy6 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy7 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy8 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy9 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    buy0v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    buy1v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    buy2v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    buy3v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    buy4v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    buy5v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    buy6v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    buy7v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    buy8v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    buy9v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell0 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell1 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell2 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell3 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell4 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell5 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell6 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell7 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell8 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell9 = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    sell0v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell1v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell2v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell3v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell4v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell5v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell6v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell7v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell8v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    sell9v = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    #class Meta:
    #    unique_together = ('product', 'tick', 'buy0v', 'sell0v')

class marketTrend(models.Model):
    market = models.ForeignKey(Market)
    date = models.DateField()
    pDate = models.DateField(null=True)
    endDate = models.DateField(null=True)   # be null until close 
    h = models.DecimalField(max_digits=8, decimal_places=3)
    l = models.DecimalField(max_digits=8, decimal_places=3)
    c = models.DecimalField(max_digits=8, decimal_places=3)
    status = models.CharField(max_length=3) # 'end/ing/may   latest/turn?'  # only 1 not ended trend?
    trendUp = models.BooleanField() # True--up False Down
    maxAmp = models.DecimalField(max_digits=6, decimal_places=2)  # top/low
    currentAmp = models.DecimalField(max_digits=6, decimal_places=2) # top/now
    drawdown = models.DecimalField(max_digits=6, decimal_places=2)   # now/low
    #trendType = 'top/sub'
    #parentTrend = models.ForeignKey(marketStatus) # 小波段的父波段？ No, 先简化，先不搞嵌套，
    # 简化规则：趋势（峰谷之间）延续9个月以上且峰谷比幅度超2且大于1.6则为一个波段，或：逆峰超越前谷          end规则: 
    # 任何时候最多有两个未end趋势，前一个已经满足趋势条件但尚未确认结束，最新一个为前一个的逆行但尚未满足作为趋势的充要条件（可理解为萌芽中的革命）  那么如何判断当前处于什么趋势呢？？？！！！

class marketPeriod(models.Model):  # 不同市场有不同定义阈值？ A股每个峰谷比超100/75的波段或超过1个月，指数/个股（按波动率定阈值？蓝筹和创板个股不同？）
    market = models.ForeignKey(Market)
    date = models.DateField()
    pDate = models.DateField(null=True)
    ### similar to marketTrend ?? 

class productStatus(models.Model):
    product = models.ForeignKey(Product)
    

class periodHL_(models.Model):
    product = models.ForeignKey(Product)     
    l = models.DecimalField(max_digits=8, decimal_places=3)
    #c = models.DecimalField(max_digits=8, decimal_places=3)
    h = models.DecimalField(max_digits=8, decimal_places=3)
