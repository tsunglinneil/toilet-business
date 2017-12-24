# coding=utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from .views.home import home_blueprint
from .views.map import map_blueprint
from flask_googlemaps import GoogleMaps


def create_app():
    # init Flask
    app = Flask(__name__)

    # install bootstrap extension
    Bootstrap(app)

    # Use application factory:
    # import blueprint and register it to app
    # defined the prefix url to separate each service

    # Home Page
    app.register_blueprint(home_blueprint)
    # Map Page
    app.register_blueprint(map_blueprint)

    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Initialize the extension and register
    GoogleMaps(app, key="AIzaSyCnJzJWFZEawx6AwTJiALRWa6MB0aLsvN8")

    return app

if __name__ == "__main__":
    create_app().run()
