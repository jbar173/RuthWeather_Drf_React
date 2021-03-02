import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'RuthWeather.settings')

import django
django.setup()

import requests
import datetime

from .models import City,Am,Pm,Eve,Report


def generate_or_display():
    y_date = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
    today = datetime.date.today()
    yest = False

    try:
        x = Report.objects.get(date=y_date)
        a = Am.objects.get(date=y_date)
        p = Pm.objects.get(date=y_date)
        e = Eve.objects.get(date=y_date)
        yest = True
    except:
        yest = False

    if yest == True:
        x.delete()
        a.delete()
        p.delete()
        e.delete()
        create_daily_report()
        yest = False

    if yest == False:
        try:
            y = Report.objects.get(date=today)
        except:
            create_daily_report()
            y = Report.objects.get(date=today)

    object = y

    return object


def create_daily_report():

    date_today = datetime.date.today()
    api_report = weather_api_report() ## returns context dictionary
    temps = api_report.get('weather')
    precs = api_report.get('precip')
    times = api_report.get('times')

    am_temp = temps.get('morning_temp')
    pm_temp = temps.get('afternoon_temp')
    day_outlook = temps.get('description')
    current_city = times.get('current_city')
    city_name = times.get('city_name')
    eve = temps.get('evening_temp')

    am_prec = precs.get('am')
    pm_prec = precs.get('pm')
    eve_prec = precs.get('eve')

    am_obj = Am.objects.get_or_create(date=date_today,temp=am_temp,prec=am_prec)[0]
    pm_obj = Pm.objects.get_or_create(date=date_today,temp=pm_temp,prec=pm_prec)[0]
    eve_obj = Eve.objects.get_or_create(date=date_today,temp=eve,prec=eve_prec)[0]

    daily_report = Report.objects.get_or_create(date=date_today,city=current_city,outlook=day_outlook,eve_temp=eve,am=am_obj,pm=pm_obj,eve=eve_obj)[0]
    daily_report.save()

    return(print(f"Report for {date_today} generated"))


##### Generated before a Report is generated (on api/report-main/):

def get_city(a,b):
    x = City.objects.get(latitude=a,longitude=b)
    return x

def weather_api_report():
    day = precip_percentage()

    weather = {
        'lat' : city_weather['lat'],
        'lon' : city_weather['lon'],
        'morning_temp':city_weather['daily'][0]['temp']['morn'],
        'afternoon_temp':city_weather['daily'][0]['temp']['day'],
        'description':city_weather['daily'][0]['weather'][0]['description'],
        'evening_temp':city_weather['daily'][0]['temp']['eve'],
        'precip_now_dt':city_weather['hourly'][0]['dt'],
        'precip_plus1_dt':city_weather['hourly'][1]['dt'],
    }

    la = weather.get('lat')
    lo = weather.get('lon')
    current_city = get_city(la,lo)
    city_name = current_city.name

    precip = {
        'am': day[0],
        'pm': day[1],
        'eve': day[4],
    }
    times = {
        'current_city': current_city,
        'city_name': city_name,
        'precip_now_time': datetime.datetime.utcfromtimestamp(float(weather.get('precip_now_dt'))),
        'precip_plus1_time': datetime.datetime.utcfromtimestamp(float(weather.get('precip_plus1_dt'))),
    }
    context = {'weather':weather,'times':times,'precip':precip}
    return context


def precip_percentage():

    day = precip_am_pm()
    am = day[0]
    pm = day[1]
    eve = day[2]

    am_av = 0
    pm_av = 0
    eve_av = 0

    for x in am:
        am_av+=x

    am_av /= len(am)

    for x in pm:
        pm_av+=x

    pm_av /= len(pm)

    for x in eve:
        eve_av+=x

    eve_av /= len(eve)

    return (am_av,pm_av,am,pm,eve_av,eve)


def precip_am_pm():

    day = precip_calculator(18,city_weather)
    i = 0
    am = []
    pm = []
    eve = []
    while i < 18:
        if i < 6:
            am.append(day[i])
            i += 1
        elif i >= 6 and i < 12:
            pm.append(day[i])
            i += 1
        else:
            eve.append(day[i])
            i += 1

    return (am,pm,eve)


def precip_calculator(num,city_weather):

    precip_list = []
    x = 6
    while num > 0:
        precip_list.append(city_weather['hourly'][x]['pop'])
        x =+ 1
        num -= 1

    return precip_list


url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=current,minutely&appid=2ceb2c7d0e1944d0cde4c275144dfdde"
# report = generate_or_display()
# city = report.city
city  = City.objects.get(id=1)
lat = city.latitude
lon = city.longitude
city_weather = requests.get(url.format(lat,lon)).json()
