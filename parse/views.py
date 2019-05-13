# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.shortcuts import render, redirect
from parse.models import Loads, Parser

import requests
import json
import datetime
from django.http import HttpResponse
import json
from django.core import serializers



def update_result(request):

    parsers = Parser.objects.filter(is_finished=False).first()

    data = serializers.serialize('json', [parsers])
    print data
    return HttpResponse(data, content_type="application/json")


# Create your views here.
def index(request):
    process_count = Parser.objects.filter(is_finished=False).count()
    if process_count == 0:
        parser = Parser(is_finished=False, parsed_total=0, created_total=0)
        parser.save()
        parse_ati(parser=parser)
        return redirect('index')

    else:
        parsers = Parser.objects.filter(is_finished=False)
        print parsers
        return render(request, 'parse/index.html', {'parsers': parsers, 'process_count': process_count})


def parse_ati(parser):
    print 'started'
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
    region_combinations_total = len(regions) * len(regions)
    parser.combinations_done = region_count
    parser.combinations_left = region_combinations_total - region_count
    parser.save()
    for region_from in regions:
        for region_to in regions:
            region_count = region_count + 1
            print 'REGION_COUNTER ' + str(region_count)
            headers = {
                'origin': 'https://loads.ati.su',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
                'content-type': 'application/json;charset=UTF-8',
                'accept': 'application/json',
                'referer': 'https://loads.ati.su/',
                'authority': 'loads.ati.su',
                'cookie': 'last_read_updates=0; _ga=GA1.2.2022737109.1548760403; _ym_uid=1548760404598233320; _ym_d=1548760404; efid=VQX%2540WJE; ASP.NET_SessionId=x0gb40ls02m5lt5kem2ckmep; itemsPerPage=10; ami=1; atisuReferrer=utm_source=AJIEIIIKA11; did=OrewgpxwPtZPpsAUN15KKpM%2BjEDjbfyUOwtGaMzOBUk%3D; sid=10c09ab4cd8a4e1288c7de2afa787e93; AtiGeo=3611_151_1_1; last_visit=1557745126648::1557755926648; last_visit=1557745150005::1557755950005',
            }
            url = 'https://loads.ati.su/webapi/v1.0/loads/search'
            data_from_chrome = '{"page":1,"items_per_page":10,"filter":{"from":{"type":5,"list_id":"' + region_from + '","list_type":2,"exact_only":true,"radius":0},' \
                                                                                                                      '"to":{"type":5,"list_id":"' + region_to + '","list_type":2,"exact_only":true,"radius":0},"dates":{"date_option":"manual","date_from":"'+datetime.datetime.now().date().strftime ("%Y-%m-%d")+'",' \
                                                                                                                                                                 '"date_to":null},"truck_type":0,"loading_type":0,"extra_params":0,"dogruz":null,' \
                                                                                                                                                                 '"sorting_type":2,"change_date":3,"show_hidden_loads":false,"board_list":[],' \
                                                                                                                                                                 '"with_dimensions":false},"exclude_geo_dicts":true} '
            data = json.loads(data_from_chrome)
            response = requests.post(url, data=json.dumps(data), headers=headers)
            try:
                result = json.loads(response.content)
                total_items = result['totalItems']
                pages_total = int(math.ceil(total_items / 10))

                print pages_total

                for page_number in range(pages_total):
                    data_from_chrome = '{"page":' + str(
                        page_number) + ',"items_per_page":10,"filter":{"from":{"type":5,"list_id":"' + region_from + '","list_type":2,"exact_only":true,"radius":0},' \
                                                                                                                     '"to":{"type":5,"list_id":"' + region_to + '","list_type":2,"exact_only":true,"radius":0},"dates":{"date_option":"manual","date_from":"'+datetime.datetime.now().date().strftime ("%Y-%m-%d")+'",' \
                                                                                                                                                                '"date_to":null},"truck_type":0,"loading_type":0,"extra_params":0,"dogruz":null,' \
                                                                                                                                                                '"sorting_type":2,"change_date":3,"show_hidden_loads":false,"board_list":[],' \
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
                            firm_id = load['firm']['id']
                        except KeyError:
                            firm_id = ''


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
                            firm_contacts = repr(load['firm']['contacts']).decode("unicode_escape")
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
                                'firm_id': firm_id,
                                'firm_name': firm_name,
                                'firm_fullname': firm_fullname,
                                'firm_profile': firm_profile,
                                'firm_city': firm_city,
                                'firm_contacts': firm_contacts,
                                'full_info': repr(load).decode("unicode_escape"),
                                'parser': parser
                            },

                        )
                        if created:
                            parser.created_total = parser.created_total + 1
                            parser.save()

                        else:
                            obj.route_distance = route_distance
                            obj.truck_loading_types = truck_loading_types
                            obj.truck_unloading_types = truck_unloading_types
                            obj.truck_car_types = truck_car_types
                            obj.load_cargo_type = load_cargo_type
                            obj.load_weight = load_weight
                            obj.load_volume = load_volume
                            obj.loading_city = loading_city
                            obj.loading_region = loading_region
                            obj.unloading_city = unloading_city
                            obj.unloading_region = unloading_region
                            obj.rate_price_nds = rate_price_nds
                            obj.rate_price_nonds = rate_price_nonds
                            obj.rate_currency = rate_currency
                            obj.firm_id = firm_id
                            obj.firm_name = firm_name
                            obj.firm_fullname = firm_fullname
                            obj.firm_profile = firm_profile
                            obj.firm_city = firm_city
                            obj.firm_contacts = firm_contacts
                            obj.full_info = repr(load).decode("unicode_escape")
                            obj.parser = parser
                            obj.save()

                        parser.parsed_total = parser.parsed_total+1
                        parser.save()
                parser.combinations_done = region_count
                parser.combinations_left = region_combinations_total - region_count
                parser.save()

            except ValueError as e:
                print response.content
                print(e)

    parser.is_finished = True
    parser.finished = datetime.datetime.now()
    parser.save()
