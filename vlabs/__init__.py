from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os

app = Flask(__name__)

from vlabs.config import BaseConfig, Development, Production

app.config.from_object(Development)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You need to be logged in to access that page.'
login_manager.login_message_category = 'blue'

from vlabs import routes