from django.contrib import admin

# Register your models here.
from .models import Market, KDaily, WatchList, Product, KMin, StockInfo, BigTrade,ProductFinacialRpt, ProductData
#from net.website.django.mysite1.myapp.models import KMin, StockInfo, BigTrade,ProductFinacialRpt, ProductData
admin.site.register(Market)
admin.site.register(WatchList)
admin.site.register(Product)
admin.site.register(KDaily)
admin.site.register(KMin)
admin.site.register(StockInfo)
admin.site.register(BigTrade)
admin.site.register(ProductFinacialRpt)
admin.site.register(ProductData)
