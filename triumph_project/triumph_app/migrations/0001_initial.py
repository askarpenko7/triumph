# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 11:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField(default=1, verbose_name='Уровень')),
                ('difficulty', models.PositiveIntegerField(default=1, verbose_name='Сложность')),
                ('sequence', models.CharField(max_length=100, verbose_name='Выражение')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_title', models.CharField(max_length=255, verbose_name='Название темы')),
                ('coefficient', models.PositiveIntegerField(default=1, verbose_name='Множитель')),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triumph_app.Theme'),
        ),
    ]
