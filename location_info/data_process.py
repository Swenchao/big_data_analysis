'''
Created on 2020年5月20日

@author: 95108
'''
from database_process import *
from toolfunc_gaode import *
import re
from time import sleep

'''
getting data
'''
def get_info(file):
    i = 0
    city_gov = {}
    # s = file.readline()
    while True:
        s = file.readline()
        if s == '':
            break
        house_info_entry = s.split(sep = ',', maxsplit = 15)
        # print(house_info_entry[:-1])
        number, region, community, deal_time, total_price,\
        unit_price, style, floor, size, orientation, \
        build_year, decoration, property_time, elevator, info = house_info_entry[:-1]

        if LocationInfo.get_or_none(number = number):
            continue
        print(s)
        
        city = re.findall('\w+', region)[0] + "市"
        address = region.replace('-','市') + community
        loc = get_loc_from_address(address)
        lat, lng = loc
        
        metro = find_underground(*loc)
        park = find_park(*loc)
        school = find_school(*loc)
        urban = get_ATM_number(*loc)
        
#         uid = get_uid(address, *loc)
#         if uid != "None":
#             equipement = check_equipment(uid)
#         else:
#             equipement = '无'
        
        if not city in city_gov.keys():
            city_gov[city] = get_government_place(city)
        dist_CBD = dist(loc, city_gov[city])
        
#         print(i, number, region, community, deal_time, total_price)
#         print(unit_price, style, floor, size, orientation)
#         print(build_year, decoration, property_time, elevator, info)
#         print(lat, lng, uid)
#         print(metro, park, school, urban, equipement, dist_CBD)

        LocationInfo.create(region = region, community = community, number=number,
                          deal_time = deal_time, total_price = total_price, 
                          unit_price = unit_price, style = style,
                          floor=floor, size = size, orientation = orientation,
                          build_year = build_year, decoration = decoration,
                          property_time = property_time, elevator = elevator, 
                          info = info, lat = str(lat), lng = str(lng), uid = "NULL",
                          metro = metro, park = park, school = school,
                          dist_CBD = str(dist_CBD), equipment = "NULL", urban = str(urban))
        sleep(0.2)
        i += 1
        if i == 6000: break
        

if __name__ == '__main__':
    '''
    先从爬下来的文件中获取基本的信息，然后获得地址，得到区位信息
    '''
    file = open('house_info2.csv','r', encoding = 'utf-8-sig')
    get_info(file)