from django.urls import path
from . import views

urlpatterns = [

    path('',views.apiOverview, name = "api-overview"),
    path('report-main',views.weather_today, name = "report-main"),

    path('am-detail/<str:pk>/',views.amDetail, name = "am-detail"),
    path('pm-detail/<str:pk>/',views.pmDetail, name = "pm-detail"),
    path('eve-detail/<str:pk>/',views.eveDetail, name = "eve-detail"),

]
