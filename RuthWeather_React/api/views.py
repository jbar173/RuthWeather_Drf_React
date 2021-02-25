from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AmSerializer,PmSerializer,EveSerializer,ReportSerializer
from .models import Am,Pm,Eve,Report

import requests
import datetime
from .precipitation import generate_or_display
from . import daily_report

# Create your views here.

@api_view(['GET',])
def apiOverview(request):
    api_urls = {
        'Weather report details':'/report-main/',
        'Am detail view':'/am-detail/<str:pk>/',
        'Pm detail view':'/pm-detail/<str:pk>/',
        'Eve detail view':'/eve-detail/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET',])
def weather_today(request):

    if request.method == 'GET':
        reports = generate_or_display()
        serializer = ReportSerializer(reports,many=False)

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
