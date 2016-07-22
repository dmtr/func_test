# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=2048, verbose_name='JSON with Array of dicts with numbers')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.IntegerField(verbose_name='Number a')),
                ('b', models.IntegerField(verbose_name='Number b')),
                ('result', models.CharField(max_length=20, verbose_name='Result (JSON)')),
                ('error', models.BooleanField(db_index=True, default=False)),
                ('exception', models.TextField(null=True, verbose_name='Error Description')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NEW', 'NEW'), ('INPROGRESS', 'INPROGRESS'), ('DONE', 'DONE')], db_index=True, default='NEW', max_length=2048)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='funcapp.DataSet')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='testrun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='funcapp.TestRun'),
        ),
    ]
