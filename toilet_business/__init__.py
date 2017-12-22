# coding=utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from .views.home import home_blueprint
from flask_googlemaps import GoogleMaps


def create_app():
    # init Flask
    app = Flask(__name__)

    # install bootstrap extension
    Bootstrap(app)

    # Use application factory:
    # import blueprint and register it to app
    # defined the prefix url to separate each service
    app.register_blueprint(home_blueprint)

    # Initialize the extension and register
    GoogleMaps(app, key="AIzaSyCnJzJWFZEawx6AwTJiALRWa6MB0aLsvN8")

    return app

if __name__ == "__main__":
    create_app().run()
