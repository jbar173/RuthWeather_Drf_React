from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (CitySerializer,AmSerializer,PmSerializer,
                            EveSerializer,ReportSerializer,)
from .models import City,Am,Pm,Eve,Report
from . import forms

import requests
import datetime
from .precipitation import (api_call,precip_calculator,precip_am_pm,
                            precip_percentage,render_api_data,
                            create_daily_reports,)

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
    create_city = forms.CreateCityForm

    if request.method == 'GET':
        a = api_call()
        b = precip_calculator(18,a)
        c = precip_am_pm(b)
        d = precip_percentage(c)
        e = render_api_data(d)
        reports = create_daily_reports(e)
        serializer = ReportSerializer(reports,many=False)

    # if request.method == 'POST':
    #     city_selected = forms.ChooseCity (onclick citylist item?)
    #
    #     create_city = forms.CreateCityForm
    #
    #     if city_selected:
            # city_object = get_city_from_name(name)
            # if city_object:
               # a = api_call_new_city(city_object)
    #     else:
            # if create_city.data.is_valid():
                # create_city.name = new_city_name
                # a = api_call_new_city(new_city_name)

    #     b = precip_calculator(18,a)
    #     c = precip_am_pm(b)
    #     d = precip_percentage(c)
    #     e = render_api_data(d)
    #     reports = create_daily_reports(e)
    #     serializer = ReportSerializer(reports,many=False)

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
