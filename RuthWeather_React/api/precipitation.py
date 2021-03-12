import requests
import datetime
import urllib.parse

from .models import City,Am,Pm,Eve,Report
from RuthWeather_React.settings import K


def create_daily_reports(api_report):

    date_today = datetime.date.today()
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

    daily_report = Report.objects.get_or_create(date=date_today,city=current_city,
    outlook=day_outlook,eve_temp=eve,am=am_obj,pm=pm_obj,eve=eve_obj)[0]

    daily_report.save()
    print(f"Report for {date_today} generated")

    return daily_report


def render_api_data(day,city):

    city_weather = day[6]

    weather = {
        'lat':city_weather['lat'],
        'lon':city_weather['lon'],
        'morning_temp':city_weather['daily'][0]['temp']['morn'],
        'afternoon_temp':city_weather['daily'][0]['temp']['day'],
        'description':city_weather['daily'][0]['weather'][0]['description'],
        'evening_temp':city_weather['daily'][0]['temp']['eve'],
        'precip_now_dt':city_weather['hourly'][0]['dt'],
        'precip_plus1_dt':city_weather['hourly'][1]['dt'],
    }

    current_city = city
    city_name = current_city.name

    precip = {
        'am': day[0],
        'pm': day[1],
        'eve': day[4],
    }
    times = {
        'current_city': current_city,
        'city_name': city_name,
        'precip_now_time':
        datetime.datetime.utcfromtimestamp(float(weather.get('precip_now_dt'))),
        'precip_plus1_time':
        datetime.datetime.utcfromtimestamp(float(weather.get('precip_plus1_dt'))),
    }
    context = {'weather':weather,'times':times,'precip':precip}

    return context

def delete_cities():
    r = Report.objects.all()
    res = r[0]
    keep = res.city
    print(f"res.city: {res.city}")
    x = City.objects.all()
    for city in x:
        if city == res.city:
            print(f"city (res): {city}")
            continue
        else:
            print(f"city (not res): {city}")
            city.delete()

def get_city(a,b):
    x = City.objects.get(latitude=a,longitude=b)
    return x

def get_city_from_name(name):
    w = name['city']
    try:
        x = City.objects.get(name=w)
        return x
    except:
        return False

def precip_percentage(day):

    am = day[0]
    pm = day[1]
    eve = day[2]
    city_weather = day[3]

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

    return (am_av,pm_av,am,pm,eve_av,eve,city_weather)


def precip_am_pm(day1):

    day = day1[0]
    city_weather = day1[1]
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
    return (am,pm,eve,city_weather)


def precip_calculator(num,city_weather):

    precip_list = []
    x = 6
    while num > 0:
        precip_list.append(city_weather['hourly'][x]['pop'])
        x =+ 1
        num -= 1
    return (precip_list,city_weather)


def generate_new_city(new_city_name):
    print(f"new_city_name: {new_city_name}, type(new_city_name): {type(new_city_name)}")
    city_name = new_city_name['city']
    print(f"city_name: {city_name}")
    key = keys()
    ckey = key[0]
    city_encoded = urllib.parse.quote(city_name)
    print(f"urlencoded city_encoded: {city_encoded}")

    url = 'https://api.opencagedata.com/geocode/v1/json?q={}&key={}'
    city_data = requests.get(url.format(city_encoded,ckey)).json()

    new_lat = city_data['results'][0]['geometry']['lat']
    new_lon = city_data['results'][0]['geometry']['lng']
    x = City.objects.create(name=city_name,latitude=new_lat,longitude=new_lon)
    print(f"x.name: {x.name},x.latitude: {x.latitude},x.longitude: {x.longitude}, type(x): {type(x)}")
    return x


###### Api Call functions: ######

#### POST (accept new city):

def api_call_new_city(city):

    c = City.objects.get(id=city.id)
    lat = c.latitude
    lon = c.longitude

    try:
        x = Report.objects.all()
        z = x[0]
        z.delete()
        a = Am.objects.all()
        b = a[0]
        b.delete()
        p = Pm.objects.all()
        q = p[0]
        q.delete()
        e = Eve.objects.all()
        f = e[0]
        f.delete()
    except:
        print("No prev reports found")

    key = keys()
    wkey = key[1]


    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=current,minutely&appid={}"

    city_weather = requests.get(url.format(lat,lon,wkey)).json()

    return city_weather

#### GET (Use prev. report's city):

def api_call():
    prev = False
    key = keys()
    wkey = key[1]
    try:
        x = Report.objects.all()
        z = x[0]
        r_city = z.city
        a = Am.objects.all()
        b = a[0]
        p = Pm.objects.all()
        q = p[0]
        e = Eve.objects.all()
        f = e[0]
        prev = True
    except:
        prev = False

    if prev == True:
        z.delete()
        b.delete()
        q.delete()
        f.delete()
        prev = False

    if prev == False:
        c = r_city
        # c_list = City.objects.all()
        # c = c_list[0]
        lat = c.latitude
        lon = c.longitude

        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=current,minutely&appid={}"

        city_weather = requests.get(url.format(lat,lon,wkey)).json()

    return (city_weather,c)


def keys():
    file = open(K,'r')
    x = file.readlines()
    o_c_1 = x[0]
    o_w_1 = x[1]

    o_c = o_c_1[:32]
    o_w = o_w_1[:32]

    file.close()
    return (o_c,o_w)
