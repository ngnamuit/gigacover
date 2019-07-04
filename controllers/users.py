# -*- coding: utf-8 -*-
#!/usr/bin/python
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp
from flask_restplus import Namespace, Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from datetime import datetime

users = [
	{
		'id': 1,
		'user_name': 'admin',
		'password': 'admin',
	},
	{
		'id': 2,
		'user_name': 'user',
		'password': 'user',
	}
]
user = Namespace('user', description='You need to login to get JWT token')
@user.route("/login", methods=['POST'])
@user.doc(params={'username': 'user', 'password': 'user'})
class UserLogin(Resource):
	def post(self):
		try:
			data = request.json
			username = data.get('username', '')
			password = data.get('password', '')
			if not data:
				abort(400, {"msg": "Missing JSON in request"})
			if not username or not password:
				abort(400, {"msg": "Missing username or password parameter"})
			for user in users:
				if user['user_name'] == username and\
					safe_str_cmp(user['password'].encode('utf-8'), password.encode('utf-8')):
					return {'access_token': create_access_token(identity=username)}
			abort(401, {"msg": "Bad username or password"})
		except KeyError as e:
			abort(500, str(e))
		except Exception as e:
			abort(400, str(e))
