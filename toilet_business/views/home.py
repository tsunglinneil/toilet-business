from flask import Blueprint, render_template

# Defined Blueprint
# Notice: the blueprint object name should not same with route def name
home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/')
def index():
    return render_template('home/index.html')


@home_blueprint.route('/map', methods=['POST'])
def map():
    return render_template('home/toiletMap.html')


@home_blueprint.route('/flaskmap', methods=['POST'])
def flaskmap():
    return render_template('home/flaskGoogleMap.html')
