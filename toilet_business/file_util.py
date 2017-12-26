#coding=utf-8
# 台北市公廁資訊 : http://www.dep-in.gov.taipei/epb/webservice/toilet.asmx/GetToiletData
from xml.etree import ElementTree as ET
from geopy.distance import vincenty
import os
import csv


def get_data(current_lat, current_lng, file_type):
    if str(file_type).upper() == "XML":
        return read_xml(current_lat, current_lng)
    elif str(file_type).upper() == "CSV":
        return read_csv(current_lat, current_lng)


def read_xml(current_lat, current_lng):
    print("XML")
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join("{}/static/datas/xml".format(this_folder), 'TaipeiPublicToilet.xml')

    taipei_tree = ET.parse(my_file)  # 讀取台北市公廁xml檔
    result_data = taipei_tree.findall('ToiletData')

    result_list = []

    for data in result_data:
        dict = {}

        number = data.find("Number").text       # 總座數
        rest = "是" if str(data.find("Restroom").text).upper() == 'Y' else "否"       # 場所提供行動不便者使用廁所
        child = "是" if str(data.find("Childroom").text).upper() == 'Y' else "否"     # 親子廁間
        kindly = "是" if str(data.find("Kindlyroom").text).upper() == 'Y' else "否"   # 貼心公廁

        name = data.find("DepName").text  # Public Toilet Name
        address = data.find("Address").text  # Public Toilet Address
        latitude = data.find("Lat").text  # 緯度
        longitude = data.find("Lng").text  # 經度

        dict = {"number": number,
                "rest": rest,
                "child": child,
                "kindly": kindly,
                "title": name,
                "latitude": latitude,
                "longitude": longitude}

        calulate_data = {"current_lat": float(current_lat),
                         "current_lng": float(current_lng),
                         "latitude": float(latitude),
                         "longitude": float(longitude)}

        distance = cal_distance(calulate_data)

        if distance < 0.5:
            # print(distance)
            result_list.append(dict)
            # print("地點:{}, 地址:{}, 經度:{}, 緯度:{}".format(name,address,latitude,longtitude))

    # for list in result_list:
    #     print("position is {} and title is {}".format(list['position'],list['title']))

    return result_list


def read_csv(current_lat, current_lng):
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
