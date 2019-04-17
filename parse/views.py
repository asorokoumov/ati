# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json
import math

from django.shortcuts import render
from parse.models import Loads

# Create your views here.
def index (request):
    import requests
    import json

    regions = ['6f5e4ef8-e210-e311-b4ec-00259038ec34',
               'ee634ef8-e210-e311-b4ec-00259038ec34',
               '79644ef8-e210-e311-b4ec-00259038ec34',
               'e1644ef8-e210-e311-b4ec-00259038ec34',
               '1f654ef8-e210-e311-b4ec-00259038ec34',
               '54654ef8-e210-e311-b4ec-00259038ec34',
               '7c654ef8-e210-e311-b4ec-00259038ec34',
               '9f654ef8-e210-e311-b4ec-00259038ec34',
               'be654ef8-e210-e311-b4ec-00259038ec34',
               ]
    region_count = 0
    for region_from in regions:
        for region_to in regions:
            region_count = region_count + 1
            print 'REGION_COUNTER ' + str(region_count)
            headers = {'content-type': 'application/json', 'cookie': 'last_read_updates=0; _ga=GA1.2.2022737109.1548760403; _ym_uid=1548760404598233320; _ym_d=1548760404; efid=VQX%2540WJE; ASP.NET_SessionId=x0gb40ls02m5lt5kem2ckmep; itemsPerPage=10; ami=1; last_visit=1554808030385::1554818830385; AtiGeo=3611_151_1_1; did=OrewgpxwPtZPpsAUN15KKpM%2BjEDjbfyUOwtGaMzOBUk%3D; sid=169a7993d6f34a7cab68a6e28ab2a79f; last_visit=1554809275946::1554820075946'}


            url = 'https://loads.ati.su/webapi/v1.0/loads/search'
            data_from_chrome = '{"page":1,"items_per_page":10,"filter":{"from":{"type":5,"list_id":"'+region_from+'","list_type":2,"exact_only":true,"radius":0},' \
                               '"to":{"type":5,"list_id":"'+region_to+'","list_type":2,"exact_only":true,"radius":0},"dates":{"date_option":"today-plus","date_from":"2019-01-01",' \
                               '"date_to":null},"truck_type":0,"loading_type":0,"extra_params":0,"dogruz":null,' \
                               '"sorting_type":2,"change_date":0,"show_hidden_loads":false,"board_list":[],' \
                               '"with_dimensions":false},"exclude_geo_dicts":true} '
            data = json.loads(data_from_chrome)
            response = requests.post(url, data=json.dumps(data), headers=headers)
            try:
                result = json.loads(response.content)
                total_items = result['totalItems']
                pages_total = int(math.ceil(total_items/10))

                print pages_total

                for page_number in range(pages_total):
                    data_from_chrome = '{"page":' + str(page_number) +',"items_per_page":10,"filter":{"from":{"type":5,"list_id":"'+region_from+'","list_type":2,"exact_only":true,"radius":0},' \
                               '"to":{"type":5,"list_id":"'+region_to+'","list_type":2,"exact_only":true,"radius":0},"dates":{"date_option":"today-plus","date_from":"2019-01-01",' \
                               '"date_to":null},"truck_type":0,"loading_type":0,"extra_params":0,"dogruz":null,' \
                               '"sorting_type":2,"change_date":0,"show_hidden_loads":false,"board_list":[],' \
                               '"with_dimensions":false},"exclude_geo_dicts":true} '
                    data = json.loads(data_from_chrome)
                    response = requests.post(url, data=json.dumps(data), headers=headers)
                    result = json.loads(response.content)
                    loads = result['loads']
                    print 'PAGE ---- ' + str(page_number)
                    for load in loads:
                        ati_id = load['id']
                        add_date = load['addDate']
                        route_distance = load['route']['distance']
                        truck_loading_types = load['truck']['loadingTypes']
                        truck_unloading_types = load['truck']['unloadingTypes']
                        truck_car_types = load['truck']['carTypes']
                        load_cargo_type = load['load']['cargoType']
                        load_weight = load['load']['weight']
                        load_volume = load['load']['volume']
                        loading_city = load['loading']['location']['city']
                        loading_region = load['loading']['location']['region']
                        unloading_city = load['unloading']['location']['city']
                        unloading_region = load['unloading']['location']['region']
                        rate_price_nds = load['rate']['priceNds']
                        rate_price_nonds = load['rate']['priceNoNds']
                        rate_currency = load['rate']['currency']
                        try:
                            firm_name = load['firm']['name']
                        except KeyError:
                            firm_name = ''

                        try:
                            firm_fullname = load['firm']['firmFullName']
                        except KeyError:
                            firm_fullname = ''

                        try:
                            firm_profile = load['firm']['profile']
                        except KeyError:
                            firm_profile = ''

                        try:
                            firm_city = load['firm']['city']
                        except KeyError:
                            firm_city = ''

                        try:
                            firm_contacts = load['firm']['contacts']
                        except KeyError:
                            firm_contacts = ''

                        obj, created = Loads.objects.get_or_create(
                            ati_id=ati_id,
                            defaults={
                                'add_date': add_date,
                                'route_distance': route_distance,
                                'truck_loading_types': truck_loading_types,
                                'truck_unloading_types': truck_unloading_types,
                                'truck_car_types': truck_car_types,
                                'load_cargo_type': load_cargo_type,
                                'load_weight': load_weight,
                                'load_volume': load_volume,
                                'loading_city': loading_city,
                                'loading_region': loading_region,
                                'unloading_city': unloading_city,
                                'unloading_region': unloading_region,
                                'rate_price_nds': rate_price_nds,
                                'rate_price_nonds': rate_price_nonds,
                                'rate_currency': rate_currency,
                                'firm_name': firm_name,
                                'firm_fullname': firm_fullname,
                                'firm_profile': firm_profile,
                                'firm_city': firm_city,
                                'firm_contacts': firm_contacts,
                            },

                        )

            except ValueError as e:
                print response.content
                print(e)

    return render(request, 'parse/index.html')
