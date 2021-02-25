
import requests
import datetime
from . import daily_report
from .models import Am,Pm,Eve,Report

url = "https://api.openweathermap.org/data/2.5/onecall?lat=53.9600&lon=1.0873&units=metric&exclude=current,minutely&appid=2ceb2c7d0e1944d0cde4c275144dfdde"
city = 'York, GB'
city_weather = requests.get(url.format(city)).json()


#######################################

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
        daily_report.create_daily_report()
        yest = False

    if yest == False:
        try:
            y = Report.objects.get(date=today)
        except:
            daily_report.create_daily_report()
            y = Report.objects.get(date=today)

    object = y

    return object



def precip_calculator(num,city_weather):

    precip_list = []
    x = 6
    while num > 0:
        precip_list.append(city_weather['hourly'][x]['pop'])
        x =+ 1
        num -= 1

    return precip_list


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


################################################



def weather_api_report():

        day = precip_percentage()

        weather = {
            'city' : city,
            'morning_temp':city_weather['daily'][0]['temp']['morn'],
            'afternoon_temp':city_weather['daily'][0]['temp']['day'],
            'description':city_weather['daily'][0]['weather'][0]['description'],
            'evening_temp':city_weather['daily'][0]['temp']['eve'],
            'precip_now_dt':city_weather['hourly'][0]['dt'],
            'precip_plus1_dt':city_weather['hourly'][1]['dt'],
        }
        precip = {
            'am': day[0],
            'pm': day[1],
            'eve': day[4],
        }
        times = {
            'precip_now_time': datetime.datetime.utcfromtimestamp(float(weather.get('precip_now_dt'))),
            'precip_plus1_time': datetime.datetime.utcfromtimestamp(float(weather.get('precip_plus1_dt'))),
        }
        context = {'weather':weather,'times':times,'precip':precip}
        return context
