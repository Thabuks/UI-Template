"""This base start"""

from flask import Flask

APP=Flask(__name__)

from app.api.v1.views.user_views import USERVIEW
APP.register_blueprint(USERVIEW)