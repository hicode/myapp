#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    #sys.path.append("D:\\GitHub\\myapp\\")


    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


    #from django.core.management import call_command
    #call_command('syncdb')

    from django.db import connections
    '''
    f = open('myapp.sql')
    sql = f.read()
    cur = connection.cursor()
    cur.executescript(sql)
    '''

    #connections['default'].creation.create_test_db()
