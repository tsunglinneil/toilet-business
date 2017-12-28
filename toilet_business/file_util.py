#coding=utf-8
# 台北市公廁資訊 : http://www.dep-in.gov.taipei/epb/webservice/toilet.asmx/GetToiletData
from xml.etree import ElementTree as ET
from geopy.distance import vincenty
from toilet_business import leveldb_util
from datetime import datetime
import os, csv, requests

time_form = "%Y-%m-%d"
today = datetime.today().strftime(time_form)

def get_data(current_lat, current_lng, room_type, file_type):
    # init database
    db = leveldb_util.init('toilet_db')

    db_data = None

    try:
        db_data = leveldb_util.search(db, today)
    except:
        db_data = None

    if db_data is None:
        print("XML SEARCH")
        if str(file_type).upper() == "XML":
            return read_xml(db, current_lat, current_lng, room_type)
        elif str(file_type).upper() == "CSV":
            return read_csv(db, current_lat, current_lng, room_type)
    else:
        print("DB SEARCH")
        return read_db(db_data, current_lat, current_lng, room_type)


def read_db(db_data, current_lat, current_lng, room_type):
    data = eval(db_data)

    # recorde distance with key("latitude,longitude")
    distance_list = {}
    result_list = []
    min_key = ""

    for dict in data:
        distance, dict = data_process(current_lat, current_lng, dict, room_type)

        if distance is not None and dict is not None:
            key = "{},{}".format(dict["latitude"], dict["longitude"])
            distance_list[key] = distance
            result_list.append(dict)

    if distance_list:
        min_key = min(distance_list.keys(), key=(lambda k: distance_list[k]))

    return result_list, min_key

def read_xml(db, current_lat, current_lng, room_type):
    # recorde distance with key("latitude,longitude")
    distance_list = {}
    result_list = []
    db_list = []
    min_key = ""

    # get xml file from websit
    parse_data()

    # when prefixes are used in the document, must be registered.
    xsi = "http://www.w3.org/2001/XMLSchema-instance"
    xsd = "http://www.w3.org/2001/XMLSchema"
    gov = "http://www.dep-in.taipei.gov.tw/epb2010/"

    find_namespace = '{}{}{}'.format("{", gov, "}")

    ns = {"xmlns:xsi": xsi, "xmlns:xsd": xsd}
    for attr, uri in ns.items():
        ET.register_namespace(attr.split(":")[1], uri)

    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join("{}/static/datas/xml".format(this_folder), 'TaipeiPublicToilet.xml')

    # read xml file
    taipei_tree = ET.parse(my_file)
    # find xml tags
    result_data = taipei_tree.findall("{}ToiletData".format(find_namespace))

    for data in result_data:
        dict = {}

        number = data.find("{}Number".format(find_namespace)).text       # 總座數
        rest = data.find("{}Restroom".format(find_namespace)).text       # 場所提供行動不便者使用廁所
        child = data.find("{}Childroom".format(find_namespace)).text     # 親子廁間
        kindly = data.find("{}Kindlyroom".format(find_namespace)).text   # 貼心公廁

        name = data.find("{}DepName".format(find_namespace)).text  # Public Toilet Name
        address = data.find("{}Address".format(find_namespace)).text  # Public Toilet Address
        latitude = data.find("{}Lat".format(find_namespace)).text  # 緯度
        longitude = data.find("{}Lng".format(find_namespace)).text  # 經度

        dict = {"number": number,
                "rest": str(rest).upper(),
                "child": str(child).upper(),
                "kindly": str(kindly).upper(),
                "title": name,
                "latitude": latitude,
                "longitude": longitude}

        db_list.append(dict)

        distance, dict = data_process(current_lat, current_lng, dict, room_type)

        if distance is not None and dict is not None:
            key = "{},{}".format(dict["latitude"], dict["longitude"])
            distance_list[key] = distance
            result_list.append(dict)

    if distance_list:
        min_key = min(distance_list.keys(), key=(lambda k: distance_list[k]))

    db_str = str(db_list)
    leveldb_util.insert(db, today, db_str)

    return result_list, min_key


def data_process(current_lat, current_lng, dict, room_type):
    calulate_data = {"current_lat": float(current_lat),
                     "current_lng": float(current_lng),
                     "latitude": float(dict['latitude']),
                     "longitude": float(dict['longitude'])}

    distance = cal_distance(calulate_data)

    if check_rule(distance, room_type, dict):

        dict['rest'] = "是" if str(dict['rest']).upper() == 'Y' else "否"
        dict['child'] = "是" if str(dict['child']).upper() == 'Y' else "否"
        dict['kindly'] = "是" if str(dict['kindly']).upper() == 'Y' else "否"
        dict['distance'] = distance

        return distance, dict

    return None, None

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


def read_csv(db, current_lat, current_lng, room_type):
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


def parse_data():
    URL = "http://www.dep-in.gov.taipei/epb/webservice/toilet.asmx/GetToiletData"
    response = requests.get(URL)
    # print(response)
    with open('static/datas/xml/TaipeiPublicToilet.xml', 'wb') as file:
        file.write(response.content)

    return file


if __name__ == '__main__':
    # data = parseData()
    # print(data)
    get_data(25.026158300000002,121.54270929999998,'ALL', 'xml')