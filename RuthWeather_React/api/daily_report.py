# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'RuthWeather.settings')
#
# import django
# django.setup()
#
# from api.models import City,Report,Am,Pm,Eve
#
# from . import precipitation
# import datetime
#
# 
# def create_daily_report():
#
#     date_today = datetime.date.today()
#     api_report = precipitation.weather_api_report() ## returns context dictionary
#     temps = api_report.get('weather')
#     precs = api_report.get('precip')
#
#     am_temp = temps.get('morning_temp')
#     pm_temp = temps.get('afternoon_temp')
#     day_outlook = temps.get('description')
#     eve = temps.get('evening_temp')
#
#     am_prec = precs.get('am')
#     pm_prec = precs.get('pm')
#     eve_prec = precs.get('eve')
#
#     am_obj = Am.objects.get_or_create(date=date_today,temp=am_temp,prec=am_prec)[0]
#     pm_obj = Pm.objects.get_or_create(date=date_today,temp=pm_temp,prec=pm_prec)[0]
#     eve_obj = Eve.objects.get_or_create(date=date_today,temp=eve,prec=eve_prec)[0]
#
#     daily_report = Report.objects.get_or_create(date=date_today,outlook=day_outlook,eve_temp=eve,am=am_obj,pm=pm_obj,eve=eve_obj)[0]
#     daily_report.save()
#
#     return(print(f"Report for {date_today} generated"))
