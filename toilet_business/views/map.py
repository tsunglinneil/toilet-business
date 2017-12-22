from flask import Blueprint, render_template, request, jsonify
from geopy.distance import vincenty

# About geopy:
# geopy makes it easy for Python developers to locate the coordinates of addresses, cities, countries,
# and landmarks across the globe using third-party geocoders and other data sources.

# Defined Blueprint
# Notice: the blueprint object name should not same with route def name
map_blueprint = Blueprint('map', __name__, url_prefix='/map')


@map_blueprint.route('/', methods=['POST'])
def map():
    # Calculate coordinate distance
    # Geopy can calculate geodesic distance between two points using the Vincenty distance or great-circle distance formulas
    newport_ri = (25.056334,121.543894)
    cleveland_oh = (25.055705,121.543832)
    print(vincenty(newport_ri, cleveland_oh).meters)

    return render_template('map/toiletMap.html')


@map_blueprint.route('/flaskmap', methods=['POST'])
def flaskmap():
    return render_template('map/flaskGoogleMap.html')


@map_blueprint.route('/flaskajax', methods=['POST'])
def flaskajax():
    json = request.get_json()
    first_name = json['first_name']
    last_name = json['last_name']
    return jsonify(first_name=first_name, last_name=last_name)
