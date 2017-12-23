from xml.etree import ElementTree as ET
from geopy.distance import vincenty
# 台北市公廁資訊 : http://www.dep-in.gov.taipei/epb/webservice/toilet.asmx/GetToiletData

def get_data(current_lat, current_long):
    taipei_tree = ET.parse("./static/TaipeiPublicToilet.xml")  # 讀取台北市公廁xml檔
    result_data = taipei_tree.findall('ToiletData')

    result_list = []

    for data in result_data:
        dict = {}

        name = data.find("DepName").text  # Public Toilet Name
        address = data.find("Address").text  # Public Toilet Address
        latitude = data.find("Lat").text  # 緯度
        longtitude = data.find("Lng").text  # 經度
        dict = {"position": "{},{}".format(latitude,longtitude), "title": name}
        calulate_data = {"current_lat": float(current_lat),
                         "current_long": float(current_long),
                         "latitude": float(latitude),
                         "longtitude": float(longtitude)}

        distance = cal_distance(calulate_data)

        if distance < 0.5:
            # print(distance)
            result_list.append(dict)
        # print("地點:{}, 地址:{}, 經度:{}, 緯度:{}".format(name,address,latitude,longtitude))

    # for list in result_list:
    #     print("position is {} and title is {}".format(list['position'],list['title']))

    return result_list


def cal_distance(data):
    # Calculate coordinate distance
    # Geopy can calculate geodesic distance between two points using the Vincenty distance or great-circle distance formulas
    newport_ri = (data['current_lat'], data['current_long'])
    cleveland_oh = (data['latitude'], data['longtitude'])
    # print(vincenty(newport_ri, cleveland_oh).kilometers)
    return vincenty(newport_ri, cleveland_oh).kilometers

