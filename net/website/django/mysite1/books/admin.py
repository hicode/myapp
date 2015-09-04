from django.contrib import admin

# Register your models here.
from .models import Book,Publisher,Author 
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Author)
