from flask import Blueprint, render_template

# Defined Blueprint
# Notice: the blueprint object name should not same with route def name
home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/')
def index():
    return render_template('home/index.html')
