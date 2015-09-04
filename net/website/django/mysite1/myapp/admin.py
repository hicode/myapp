from django.contrib import admin

# Register your models here.
from .models import Market, KDaily, WatchList, Product
admin.site.register(Market)
admin.site.register(WatchList)
admin.site.register(Product)
admin.site.register(KDaily)
