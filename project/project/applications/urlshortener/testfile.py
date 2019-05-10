import requests
import json

url2 = 'http://api.sypexgeo.net/json/94.143.45.141'
url = 'http://94.143.45.141.ip-adress.com'
url3 = 'http://ip-api.com/json/94.143.45.141'

data = requests.get(url3)

print(data.json())


def simple_map():
    yapi = 'https://static-maps.yandex.ru/1.x/?l=map&size=450,150&z=10&pt='
    yamark = 'flag'
    url2 = 'http://api.sypexgeo.net/json/94.143.45.141'
    url3 = 'http://ip-api.com/json/94.143.45.141'
    data = requests.get(url3).json()
    lat = data['lat']
    lng = data['lon']
    url = yapi + str(lng) + ',' + str(lat) + ',' + yamark
    print(url)
    return mark_safe('<img src="%s" width="600" height="450" />' % url)


simple_map.allow_tags = True
simple_map.short_description = 'Карта'