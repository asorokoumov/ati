# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now

# Create your models here.
class Loads(models.Model):
    ati_id = models.TextField(default=None, blank=True, null=True)
    add_date = models.TextField(default=None, blank=True, null=True)
    route_distance = models.FloatField(default=None, blank=True, null=True)
    truck_loading_types = models.TextField(default=None, blank=True, null=True)
    truck_unloading_types = models.TextField(default=None, blank=True, null=True)
    truck_car_types = models.TextField(default=None, blank=True, null=True)
    load_cargo_type = models.TextField(default=None, blank=True, null=True)
    load_weight = models.TextField(default=None, blank=True, null=True)
    load_volume = models.TextField(default=None, blank=True, null=True)
    loading_city = models.TextField(default=None, blank=True, null=True)
    loading_region = models.TextField(default=None, blank=True, null=True)
    unloading_city = models.TextField(default=None, blank=True, null=True)
    unloading_region = models.TextField(default=None, blank=True, null=True)
    rate_price_nds = models.TextField(default=None, blank=True, null=True)
    rate_price_nonds = models.TextField(default=None, blank=True, null=True)
    rate_currency = models.TextField(default=None, blank=True, null=True)
    firm_name = models.TextField(default=None, blank=True, null=True)
    firm_fullname = models.TextField(default=None, blank=True, null=True)
    firm_profile = models.TextField(default=None, blank=True, null=True)
    firm_city = models.TextField(default=None, blank=True, null=True)
    firm_contacts = models.TextField(default=None, blank=True, null=True)
    last_found = models.DateTimeField(default=now)

    def __str__(self):
        return self.ati_id

