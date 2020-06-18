'''
Created on 2020年5月20日

@author: 95108
'''
import requests
from bs4 import BeautifulSoup
import re
from math import sin, cos, acos, radians

class Par:
    key = 'd6dc92e38d2128b344099691d5464313'
    R = 6371

def get_detail(url):
    html = requests.get(url)
    detail = BeautifulSoup(html.text, 'lxml')
    return str(detail)

def get_loc_from_address(address):
    key = Par.key
    url = 'https://restapi.amap.com/v3/geocode/geo?key=' + key +\
    '&address=' + address
    detail = get_detail(url)
    loc = re.findall('"location":"([.\d]+),([.\d]+)"', detail)[0]
    lng, lat = loc
    return float(lat), float(lng)
    
def find_underground(lat, lng):
    key = Par.key
    url = 'https://restapi.amap.com/v3/place/around?key=' + key +\
    '&location=' + str(lng) + ',' + str(lat) + '&types=地铁站&radius=1000'
    detail = get_detail(url)
    if re.findall('"name"', detail):
        return True
    else:
        return False
    
def find_park(lat, lng):
    '''
    find park in 1km
    '''
    key = Par.key
    url = 'https://restapi.amap.com/v3/place/around?key=' + key +\
    '&location=' + str(lng) + ',' + str(lat) + '&types=公园|公园广场&radius=1000'
    detail = get_detail(url)
    if re.findall('"name"', detail):
        return True
    else:
        return False
    
def find_school(lat, lng):
    '''
    find school in 1km
    '''
    key = Par.key
    url = 'https://restapi.amap.com/v3/place/around?key=' + key +\
    '&location=' + str(lng) + ',' + str(lat) + '&types=幼儿园|小学|中学&radius=1000'
    detail = get_detail(url)
    if re.findall('"name"', detail):
        return True
    else:
        return False

def get_government_place(city):
    '''
    find the place of government as CBD
    '''
    address = city + "人民政府"
    loc = get_loc_from_address(address)
    return loc

def get_ATM_number(lat, lng):
    key = Par.key
    url = 'https://restapi.amap.com/v3/place/around?key=' + key +\
    '&location=' + str(lng) + ',' + str(lat) + '&types=160100|160300&radius=1000'
    detail = get_detail(url)
    ATM_num = re.findall('"count":"(\d+)"', detail)
    if ATM_num:
        return ATM_num[0]
    else: return 0

def get_uid(address, lat, lng):
    ak = Par.key
    url = 'http://api.map.baidu.com/place/v2/search?query=' + address + \
    '&location=' + str(lat) + ',' + str(lng) + '&output=json&page_size=1&ak=' + ak
    detail = get_detail(url)
    uid = re.findall('"uid":"(\w+)"', detail)
    if uid:
        return uid[0]
    else:
        return "None"

def check_equipment(lat, lng):
    '''
    To check a residence if it is well equipped, using its uid
    '''
    key = Par.key
    url = 'https://restapi.amap.com/v3/place/around?key=' + key +\
    '&location=' + str(lng) + ',' + str(lat) + '&types=120300&radius=100'
    detail = get_detail(url)
    print(detail)
    if re.findall('配套齐全', detail):
        return '配套齐全'
    else:
        return '无'

def dist(loc1, loc2):
    lat1, lng1 = loc1
    lat2, lng2 = loc2
    lat1, lng1 = radians(lat1), radians(lng1)
    lat2, lng2 = radians(lat2), radians(lng2)
    alpha = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lng1 - lng2)
    distance = Par.R * acos(alpha)
    return distance

if __name__ == '__main__':
    pass
#     lat = 23.129029707055655
#     lng = 113.31888505165307
#     print(check_equipment(lat, lng))
    
#     address = "东莞市虎门镇虎门一号"
#     print(get_loc_from_address(address))