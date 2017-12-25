from flask import Blueprint, render_template, request, jsonify
from toilet_business import file_util

# About geopy:
# geopy makes it easy for Python developers to locate the coordinates of addresses, cities, countries,
# and landmarks across the globe using third-party geocoders and other data sources.

# Defined Blueprint
# Notice: the blueprint object name should not same with route def name
map_blueprint = Blueprint('map', __name__, url_prefix='/map')


@map_blueprint.route('/', methods=['POST'])
def map():
    return render_template('map/toiletMap.html')


@map_blueprint.route('/flaskmap', methods=['POST'])
def flaskmap():
    return render_template('map/flaskGoogleMap.html')


@map_blueprint.route('/flaskajax', methods=['POST'])
def flaskajax():
    json = request.get_json()
    current_lat = json['latitude']
    current_lng = json['longitude']
    print("Now position is {},{}".format(current_lat, current_lng))

    # Test Data
    # result_list = [{"position": "{}".format("25.056334,121.543894"), "title": "post office"},
    #               {"position": "{}".format("25.055705,121.543832"), "title": "cafe"},
    #               {"position": "{}".format("25.055191,121.545222"), "title": "park"}]

    result_list = file_util.get_data(current_lat, current_lng)

    return jsonify(resultList=result_list)
