import os
from vlabs import app

class BaseConfig(object):
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'd88d1dcd84d6794a855a7a9812df0fb7'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(app.root_path + '/static/labs/')

class Development(BaseConfig):
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'd88d1dcd84d6794a855a7a9812df0fb7'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(app.root_path + '/static/labs/')

class Production(BaseConfig):
    DEBUG = False
    ENV = 'production'
    SECRET_KEY = 'c3620fe2c86c18919291b3b20b74be64'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(app.root_path + '/static/labs/')