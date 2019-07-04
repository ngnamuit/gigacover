# -*- coding: utf-8 -*-
#!/usr/bin/python
from flask import Flask, request, abort
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from datetime import datetime
import ConfigParser as configparser

config = configparser.ConfigParser()
config.read('config.ini')
DatabaseHost = config.get('DEFAULT', 'DatabaseHost') or ''
DatabaseName = config.get('DEFAULT', 'DatabaseName') or ''
DatabaseUserName = config.get('DEFAULT', 'DatabaseUserName') or ''
DatabasePassword = config.get('DEFAULT', 'DatabasePassword') or ''


flask_app = Flask(__name__)
flask_app.config.SWAGGER_UI_DOC_EXPANSION = config.get('DEFAULT', 'SWAGGER_UI_DOC_EXPANSION') or ''
flask_app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://%s:%s@%s/%s'%(
    DatabaseUserName, DatabasePassword, DatabaseHost, DatabaseName)
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.get('DEFAULT', 'SQLALCHEMY_TRACK_MODIFICATIONS') or False ## enable database debug logs
flask_app.config['JWT_SECRET_KEY'] = config.get('DEFAULT', 'JWT_SECRET_KEY') or ''
db = SQLAlchemy(flask_app)
jwt = JWTManager(flask_app)
