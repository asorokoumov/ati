# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Loads, Parser, Stopper

# Register your models here.

admin.site.register(Loads)
admin.site.register(Parser)
admin.site.register(Stopper)
