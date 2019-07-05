# -*- coding: utf-8 -*-
#!/usr/bin/python
from flask import request, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp
from flask_restplus import Namespace, Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from datetime import datetime
from passlib.context import CryptContext

users = [
	{
		'id': 1,
		'user_name': 'admin',
		'password': 'admin',
	},
	{
		'id': 2,
		'user_name': 'user',
		'password': '$pbkdf2-sha256$30000$ASAk5DxnzJmzNuacc651bg$HlwuY/SjdoWkT1OMP5k3VkDegU21s0M7lw5rY0QoCDA',
	}
]
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)
def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)

user = Namespace('user', description='You need to login to get JWT token')
@user.route("/login", methods=['POST'])
@user.doc(params={'username': 'user', 'password': 'user'})
class UserLogin(Resource):
	def post(self):
		try:
			data = request.json
			username = data.get('username', '')
			password = data.get('password', '')
			if not username or not password:
				abort(401, {"msg": "Bad username or password"})
			if not data:
				abort(400, {"msg": "Missing JSON in request"})
			if not username or not password:
				abort(400, {"msg": "Missing username or password parameter"})
			for user in users:
				if user['user_name'] == username and check_encrypted_password(password, user['password']):
					return {'access_token': create_access_token(identity=username)}
			abort(401, {"msg": "Username or password incorrect"})
		except KeyError as e:
			abort(500, str(e))
		except Exception as e:
			abort(400, str(e))
