from django.shortcuts import render

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers
from . import models

# Create your views here.

@api_view(['GET',])
def apiOverview(request):
    api_urls = {
        'Create am':'/create-am/',
        'Am detail view':'/am-detail/<str:pk>/',
        'Create pm':'/create-pm/',
        'Pm detail view':'/pm-detail/<str:pk>/',
        'Create eve':'/create-eve/',
        'Eve detail view':'/eve-detail/<str:pk>/',
        'Create report':'/create-report/',
        'Report detail view':'/report-detail/<str:pk>/',
        'Delete Report':'/report-delete/<str:pk>',
    }
    return Response(api_urls)

## GET requests:

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

@api_view(['GET',])
def reportDetail(request,pk):
    reports = Report.objects.get(id=pk)
    serializer = ReportSerializer(reports,many=False)
    return Response(serializer.data)

######################

## POST requests:

# creates:

@api_view(['POST',])
def amCreate(request):
    serializer = AmSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST',])
def pmCreate(request):
    serializer = PmSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST',])
def eveCreate(request):
    serializer = EveSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST',])
def reportCreate(request):
    serializer = reportSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

# deletes:

@api_view(['DELETE',])
def amDelete(request,pk):
    am = Am.objects.get(id=pk)
    am.delete()

    return Response(f"Am {am.id} deleted")

@api_view(['DELETE',])
def pmDelete(request,pk):
    pm = Pm.objects.get(id=pk)
    pm.delete()

    return Response(f"Pm {pm.id} deleted")

@api_view(['DELETE',])
def eveDelete(request,pk):
    eve = Eve.objects.get(id=pk)
    eve.delete()

    return Response(f"Eve {eve.id} deleted")

@api_view(['DELETE',])
def reportDelete(request,pk):
    report = Report.objects.get(id=pk)
    report.delete()

    return Response(f"Report {report.id} deleted")
