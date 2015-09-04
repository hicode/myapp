from django.db import models

# Create your models here.
from django.contrib import admin

# Create your models here.
class Market(models.Model):     
    name = models.CharField(max_length=8)
    currency = models.CharField(max_length=3)     
    def __str__(self):
        return self.name
#    class admin:
#        pass

class Product(models.Model):
    code = models.CharField(max_length=8)     
    market = models.CharField(max_length=8)     
    type = models.CharField(max_length=1)  # stock / fund / warrant / structuredFund/ option 
    bDataHist = models.BooleanField()
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    class Meta:
        unique_together = ('code', 'market')
#    class admin:
#        pass

class stockInfo(models.Model):
    #code = models.CharField(max_length=8)     
    #market = models.CharField(max_length=8)
    product = models.ForeignKey(Product)     
    companyName = models.CharField(max_length=32)     
    IPOShares = models.DecimalField(max_digits=16, decimal_places=0)
    IPOPrice = models.DecimalField(max_digits=8, decimal_places=5)
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    #class Meta:
    #    unique_together = ('code', 'market')

class bigTrade(models.Model):
    code = models.CharField(max_length=8)     
    market = models.CharField(max_length=8)     
    buyer = models.CharField(max_length=32)     
    shares = models.DecimalField(max_digits=16, decimal_places=0)
    price = models.DecimalField(max_digits=8, decimal_places=5)
    date = models.DateField() 
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
    class Meta:
        unique_together = ('code', 'market', 'buyer', 'date')

bigone={} # 社保 QFII 阿里 百度 腾讯 

class productFinacialRpt(models.Model):
    code = models.CharField(max_length=8)     
    market = models.CharField(max_length=8)     
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
    class Meta:
        unique_together = ('code', 'market', 'date')

class productData(models.Model):
    code = models.CharField(max_length=8)     
    market = models.CharField(max_length=8)     
    date = models.DateField() 
    rzrq = models.DecimalField(max_digits=16, decimal_places=0)
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
#    class admin:
#        pass
    class Meta:
        unique_together = ('code', 'market', 'date')

# watchreason
class WatchList(models.Model):
    code = models.CharField(max_length=8)     
    market = models.CharField(max_length=8)     
    watchReason = models.CharField(max_length=256)     
    def __str__(self):
        return '%s.%s' % (self.code, self.market)
#    class admin:
#        pass
    class Meta:
        unique_together = ('code', 'market')

class KDaily(models.Model):
    code = models.CharField(max_length=8)     
    market = models.CharField(max_length=8)     
    p = models.DecimalField(max_digits=8, decimal_places=5)  # previous close
    o = models.DecimalField(max_digits=8, decimal_places=5)
    h = models.DecimalField(max_digits=8, decimal_places=5)
    l = models.DecimalField(max_digits=8, decimal_places=5)
    c = models.DecimalField(max_digits=8, decimal_places=5)
    adjC = models.DecimalField(max_digits=8, decimal_places=5)  # adjusted close
    amt = models.DecimalField(max_digits=16, decimal_places=2)
    vol = models.DecimalField(max_digits=16, decimal_places=0)
    date = models.DateField() 
    def __str__(self):
        return '%s.%s %s' % (self.code, self.market, self.date)
    class Meta:
        unique_together = ('code', 'market', 'date')

class KMin(models.Model):
    code = models.CharField(max_length=8)     
    market = models.CharField(max_length=8)     
    p = models.DecimalField(max_digits=8, decimal_places=5)  # previous close
    o = models.DecimalField(max_digits=8, decimal_places=5)
    h = models.DecimalField(max_digits=8, decimal_places=5)
    l = models.DecimalField(max_digits=8, decimal_places=5)
    c = models.DecimalField(max_digits=8, decimal_places=5)
    amt = models.DecimalField(max_digits=16, decimal_places=2)
    vol = models.DecimalField(max_digits=16, decimal_places=0)
    date = models.DateField()
    time = models.TimeField() 
    def __str__(self):
        return '%s.%s %s %s' % (self.code, self.market, self.date, self.time)
    #class Meta:
    #    unique_together = ('code', 'market', 'date',' time')

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
