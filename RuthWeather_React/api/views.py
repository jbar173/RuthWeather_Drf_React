from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (CitySerializer,AmSerializer,PmSerializer,
                            EveSerializer,ReportSerializer,)
from .models import City,Am,Pm,Eve,Report

import requests
import datetime
from .precipitation import (api_call,precip_calculator,precip_am_pm,
                            precip_percentage,render_api_data,
                            create_daily_reports,get_city_from_name,
                            generate_new_city,api_call_new_city,)

# Create your views here.


@api_view(['GET',])
def apiOverview(request):
    api_urls = {
        'Weather report details':'/report-main/',
        'List of cities':'/city-list/',
        'City Detail view':'/city-detail/<str:pk>/',
        'Am detail view':'/am-detail/<str:pk>/',
        'Pm detail view':'/pm-detail/<str:pk>/',
        'Eve detail view':'/eve-detail/<str:pk>/',
    }
    return Response(api_urls)


@api_view(['GET','POST',])
def weather_today(request):

    if request.method == 'GET':
        x = api_call()
        z = x[1]
        a = x[0]
        b = precip_calculator(18,a)
        c = precip_am_pm(b)
        d = precip_percentage(c)
        e = render_api_data(d,z)
        reports = create_daily_reports(e)
        serializer = ReportSerializer(reports,many=False)
        return Response(serializer.data)

    if request.method == 'POST':
        city_name = request.data
        print(f"city_name *1: {city_name}")

        # try:
        city_update = get_city_from_name(city_name)

        if city_update:
            a = api_call_new_city(city_update)
            b = precip_calculator(18,a)
            c = precip_am_pm(b)
            d = precip_percentage(c)
            e = render_api_data(d,city_update)
            reports = create_daily_reports(e)
            serializer = ReportSerializer(reports,many=False)
            return Response(serializer.data)

        # except:
        else:
            x = generate_new_city(city_name)
            print(f"new_city(x): {x.name}, {type(x)}, id: {x.id}")
            a = api_call_new_city(x)
            b = precip_calculator(18,a)
            c = precip_am_pm(b)
            d = precip_percentage(c)
            e = render_api_data(d,x)
            reports = create_daily_reports(e)
            serializer = ReportSerializer(reports,many=False)
            return Response(serializer.data)


@api_view(['GET',])
def cityList(request):
    cities = City.objects.all().order_by('-id')
    serializer = CitySerializer(cities,many=True)
    return Response(serializer.data)


@api_view(['GET',])
def cityDetail(request,pk):
    cities = City.objects.get(id=pk)
    serializer = CitySerializer(cities,many=False)
    return Response(serializer.data)


@api_view(['GET',])
def amDetail(request,pk):
    ams = Am.objects.get(id=pk)
    serializer = AmSerializer(ams,many=False)
    return Response(serializer.data)


@api_view(['GET',])
def pmDetail(request,pk):
    pms = Pm.objects.get(id=pk)
    serializer = PmSerializer(pms,many=False)
    return Response(serializer.data)


@api_view(['GET',])
def eveDetail(request,pk):
    eves = Eve.objects.get(id=pk)
    serializer = EveSerializer(eves,many=False)
    return Response(serializer.data)
