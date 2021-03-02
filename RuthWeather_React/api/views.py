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
from .precipitation import (generate_or_display, create_daily_report)


# Create your views here.

@api_view(['GET',])
def apiOverview(request):
    api_urls = {
        'Weather report details':'/report-main/',
        'City Detail view':'/city-detail/<str:pk>/',
        'Am detail view':'/am-detail/<str:pk>/',
        'Pm detail view':'/pm-detail/<str:pk>/',
        'Eve detail view':'/eve-detail/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET','POST',])
def weather_today(request):
    form = forms.CityForm

    if request.method == 'GET':
        reports = generate_or_display()
        serializer = ReportSerializer(reports,many=False)
    # if request.method == 'POST':
    #

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
