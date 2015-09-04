# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KDaily',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=8)),
                ('market', models.CharField(max_length=8)),
                ('p', models.DecimalField(max_digits=8, decimal_places=5)),
                ('o', models.DecimalField(max_digits=8, decimal_places=5)),
                ('h', models.DecimalField(max_digits=8, decimal_places=5)),
                ('l', models.DecimalField(max_digits=8, decimal_places=5)),
                ('c', models.DecimalField(max_digits=8, decimal_places=5)),
                ('amt', models.DecimalField(max_digits=16, decimal_places=2)),
                ('vol', models.DecimalField(max_digits=8, decimal_places=0)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=8)),
                ('currency', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=8)),
                ('market', models.CharField(max_length=8)),
                ('companyName', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=8)),
                ('market', models.CharField(max_length=8)),
                ('watchReason', models.CharField(max_length=256)),
            ],
        ),
    ]
