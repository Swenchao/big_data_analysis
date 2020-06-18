'''
Created on 2020年5月21日

@author: 95108
'''
from database_process import *
import os
import re

head = 'number,region,community,deal_time,total_price(万元),unit_price(元/平),style,floor_height,' + \
'total_height,size(m2),orientation,build_year,decoration,property_time,elevator,' + \
'metro,park,school,dist_CBD,urban_rate,equipment,lat,lng,uid,info'

def write_info(file, filename, info):
    if not os.path.getsize(filename):
        file.write(head + "\n")
        file.flush()
    file.write(info + "\n")
    file.flush()
    
def get_info_from_db(number):
    print(number)
    a = locationinfo.get_or_none(number=number)
    print(a)
    if a:
        infos = locationinfo.select().where(locationinfo.number == number)
        for info in infos:
            flag = True
            
            region = info.region
            community = info.community
            deal_time = info.deal_time
            
            total_price = re.findall('(\d+)', info.total_price)
            if total_price:
                total_price = total_price[0]
            else:
                flag = False
            
            unit_price = re.findall('(\d+)',info.unit_price)
            if unit_price: unit_price = unit_price[0]
            else:
                flag = False
            
            style = info.style
            
            floor_info = info.floor
            floor_height = re.findall('([低中高])', floor_info)
            if floor_height:
                floor_height = floor_height[0]
            else:
                flag = False
            total_height = re.findall('(\d+)', floor_info)
            if total_height:
                total_height = total_height[0]
            else:
                flag = False
            
            size = re.findall('(\d+)', info.size)
            if size:
                size = size[0]
            else:
                flag = False
            
            orientation = info.orientation
            if orientation == "暂无数据":
                flag = False
            
            build_year = info.build_year
            if build_year == "未知":
                flag = False
            
            decoration = info.decoration
            property_time = info.property_time
            elevator = info.elevator
            if elevator == "暂无数据":
                flag = False
            
            metro = info.metro
            park = info.park
            school = info.school
            dist_CBD = info.dist_CBD
            urban_rate = info.urban
            equipment = info.equipment
            lat = info.lat
            lng = info.lng
            uid = info.uid
            information = info.info
            if flag == True:
                i = [number,region,community,deal_time,total_price,unit_price,style,floor_height,
                     total_height,size,orientation,build_year,decoration,property_time,elevator,
                     metro,park,school,dist_CBD,urban_rate,equipment,lat,lng,uid,information]
                return ','.join(map(str, i))
            else: return None
    else: return None
                
    
def process(input_filename, output_filename):
    file = open(input_filename,'r', encoding = 'utf-8-sig')
    out = open(output_filename, 'w+', encoding = 'utf-8-sig')
    while True:
        s = file.readline()
        if s == "":
            break
        house_info_entry = s.split(sep = ',', maxsplit = 15)
        number = house_info_entry[0]
        info = get_info_from_db(number)
        # print(number)
        if info:
            write_info(out, output_filename, info)
    out.close()

if __name__ == '__main__':
    # 两个参数，原来的csv文件（读入number，向db查询），新的csv文件（写入信息）
    process('locationinfo.csv', 'locationinfo_new.csv')