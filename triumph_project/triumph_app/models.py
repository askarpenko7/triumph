#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


class Theme(models.Model):
    theme_title = models.CharField('Название темы', max_length=255)
    coefficient = models.PositiveIntegerField('Множитель', default=1)

    def __str__(self):
        return str(self.theme_title)


class Challenge(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    level = models.PositiveIntegerField('Уровень', default=1)
    sequence = models.CharField('Выражение', max_length=999)

    def __str__(self):
        return str(self.theme) + '; ' + 'Уровень: ' + str(self.level) + '; ' + 'Выражение: ' + self.sequence
