# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KMin',
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
                ('vol', models.DecimalField(max_digits=16, decimal_places=0)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='kdaily',
            name='vol',
            field=models.DecimalField(max_digits=16, decimal_places=0),
        ),
    ]
