import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'RuthWeather_React.settings')

import django
django.setup()

import urllib.parse
import requests
from RuthWeather_React.settings import K



def keys():
    file = open(K,'r')
    x = file.readlines()
    o_c_1 = x[0]
    o_w_1 = x[1]

    o_c = o_c_1[:32]
    o_w = o_w_1[:32]

    file.close()
    return (o_c,o_w)



def generate_new_city(new_city_name):
    key = keys()
    ckey = key[0]
    city_encoded = urllib.parse.quote(new_city_name)
    print(f"****city_encoded: {city_encoded}")

    url = 'https://api.opencagedata.com/geocode/v1/json?q={}countrycode=gb&key={}'
    city_data = requests.get(url.format(city_encoded,ckey)).json()

    return(print(city_data))



if __name__ == '__main__':
    generate_new_city('Great Yarmouth')
