#from django.template.loader import get_template 
#from django.template import Context
#from django.http import HttpResponse
from django.shortcuts import render_to_response  
import datetime

def current_datetime(request):
    now=datetime.datetime.now()
    #html="<html><body>It is now %s. </body></html>" % now
    #t = get_template('current_datetime.html')
    #html = t.render(Context({'current_date': now}))
    #return HttpResponse(html)
    return render_to_response('dateapp/current_datetime.html', {'current_date': now})
    #current_date = datetime.datetime.now()
    #return render_to_response('current_datetime.html', locals())

def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    #html="<html><body>In %s hour(s), it will be %s. </body></html>" % (offset, dt)
    #return HttpResponse(html)
    return render_to_response('dateapp/hours_ahead.html', {'hour_offset': offset, 'next_time':dt})
