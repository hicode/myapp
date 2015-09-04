from django.shortcuts import render

# Create your views here.
'''
from django.shortcuts import render_to_response 
import MySQLdb  
def book_list(request):
     db = MySQLdb.connect(user='me', db='mydb', passwd='secret', host='localhost')
     cursor = db.cursor()     
     cursor.execute('SELECT name FROM books ORDER BY name')     
     names = [row[0] for row in cursor.fetchall()]     
     db.close()     
     return render_to_response('book_list.html', {'names': names}) 
'''

from django.shortcuts import render_to_response 
from mysite.books.models import Book  
def book_list(request):
    books = Book.objects.order_by('name')
    return render_to_response('book_list.html', {'books': books}) 
