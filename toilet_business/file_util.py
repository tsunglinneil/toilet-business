#coding=utf-8
# 台北市公廁資訊 : http://www.dep-in.gov.taipei/epb/webservice/toilet.asmx/GetToiletData
from xml.etree import ElementTree as ET
from geopy.distance import vincenty
import os
import csv


def get_data(current_lat, current_lng, room_type, file_type):
    if str(file_type).upper() == "XML":
        return read_xml(current_lat, current_lng, room_type)
    elif str(file_type).upper() == "CSV":
        return read_csv(current_lat, current_lng, room_type)


def read_xml(current_lat, current_lng, room_type):
    print("XML")
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join("{}/static/datas/xml".format(this_folder), 'TaipeiPublicToilet.xml')

    taipei_tree = ET.parse(my_file)  # 讀取台北市公廁xml檔
    result_data = taipei_tree.findall('ToiletData')

    # recorde distance with key("latitude,longitude")
    distance_list = {}
    result_list = []

    for data in result_data:
        dict = {}

        number = data.find("Number").text       # 總座數
        rest = data.find("Restroom").text       # 場所提供行動不便者使用廁所
        child = data.find("Childroom").text     # 親子廁間
        kindly = data.find("Kindlyroom").text   # 貼心公廁

        name = data.find("DepName").text  # Public Toilet Name
        address = data.find("Address").text  # Public Toilet Address
        latitude = data.find("Lat").text  # 緯度
        longitude = data.find("Lng").text  # 經度

        dict = {"number": number,
                "rest": str(rest).upper(),
                "child": str(child).upper(),
                "kindly": str(kindly).upper(),
                "title": name,
                "latitude": latitude,
                "longitude": longitude}

        calulate_data = {"current_lat": float(current_lat),
                         "current_lng": float(current_lng),
                         "latitude": float(latitude),
                         "longitude": float(longitude)}

        distance = cal_distance(calulate_data)

        if check_rule(distance, room_type, dict):
            key = "{},{}".format(dict["latitude"], dict["longitude"])
            distance_list[key] = distance
            dict['rest'] = "是" if str(rest).upper() == 'Y' else "否"
            dict['child'] = "是" if str(child).upper() == 'Y' else "否"
            dict['kindly'] = "是" if str(kindly).upper() == 'Y' else "否"
            dict['distance'] = distance
            result_list.append(dict)
            # print("地點:{}, 地址:{}, 經度:{}, 緯度:{}".format(name,address,latitude,longtitude))

    min_key = min(distance_list.keys(), key=(lambda k: distance_list[k]))
    print(min_key)
    print(distance_list[min_key])

    # for list in result_list:
    #     print("position is {} and title is {}".format(list['position'],list['title']))

    return result_list, min_key


def check_rule(distance, room_type, dict):
    if distance < 0.5:
        if 'rest' == room_type:
            return True if dict['rest'] == 'Y' else False
        elif 'child' == room_type:
            return True if dict['child'] == 'Y' else False
        elif 'kindly' == room_type:
            return True if dict['kindly'] == 'Y' else False
        elif 'ALL' == room_type:
            return True;
    else:
        return False


def read_csv(current_lat, current_lng, room_type):
    print("CSV")
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join("{}/static/datas/csv".format(this_folder), 'toilets.csv')
    with open(my_file, newline='', encoding='big-5') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)


def cal_distance(data):
    # Calculate coordinate distance
    # Geopy can calculate geodesic distance between two points using the Vincenty distance or great-circle distance formulas
    newport_ri = (data['current_lat'], data['current_lng'])
    cleveland_oh = (data['latitude'], data['longitude'])
    # print(vincenty(newport_ri, cleveland_oh).kilometers)
    return vincenty(newport_ri, cleveland_oh).kilometers
