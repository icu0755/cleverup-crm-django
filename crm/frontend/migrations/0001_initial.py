# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GroupAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attendance_time', models.DateField()),
                ('customer', models.ForeignKey(to='frontend.Customer')),
                ('group', models.ForeignKey(related_name='attendance', to='frontend.CustomerGroup')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='group',
            field=models.ForeignKey(related_name='customers', to='frontend.CustomerGroup'),
        ),
    ]
