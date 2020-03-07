from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from vlabs.config import Development, Production
import os

app = Flask(__name__)

# class BaseConfig(object):
#     DEBUG = True
#     ENV = 'development'
#     SECRET_KEY = 'd88d1dcd84d6794a855a7a9812df0fb7'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     UPLOAD_FOLDER = os.path.join(app.root_path + '/static/labs/')

# class Development(BaseConfig):
#     DEBUG = True
#     ENV = 'development'
#     SECRET_KEY = 'd88d1dcd84d6794a855a7a9812df0fb7'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     UPLOAD_FOLDER = os.path.join(app.root_path + '/static/labs/')

# class Production(BaseConfig):
#     DEBUG = False
#     ENV = 'production'
#     SECRET_KEY = 'c3620fe2c86c18919291b3b20b74be64'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     UPLOAD_FOLDER = os.path.join(app.root_path + '/static/labs/')

from vlabs.config import BaseConfig, Development, Production

app.config.from_object(Development)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You need to be logged in to access that page.'
login_manager.login_message_category = 'blue'

from vlabs import routes