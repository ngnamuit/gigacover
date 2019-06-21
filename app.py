# -*- coding: utf-8 -*-
#!/usr/bin/python
from flask import Flask, request, abort
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp
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

flask_app = Flask(__name__)
flask_app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
flask_app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://sample_python_api:1@35.232.87.105/sample_python_api' ## connect postgresql database
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True ## enable database debug logs
flask_app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(flask_app)
db = SQLAlchemy(flask_app)

## define to use swagger UI
app = Api(app = flask_app,
		  version = "1.0",
		  title = "sample-python-api UI",
		  description = "Manage routing of the application")
## Define TABLE
class Customers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256), nullable=False)
	dob = db.Column(db.Date)
	updated_at = db.Column(db.DateTime)
## define routing
customer = app.namespace('customer', description='Customer')
user = app.namespace('user', description='You need to login to get JWT token')

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

@customer.route("/get/<int:id>", methods=['GET'])
class Customer(Resource):
	@jwt_required
	def get(self, id):
		try:
			customer = Customers.query.filter(Customers.id == id).first()
			if customer:
				return {
					'id': customer.id,
					'name': customer.name,
					'dob': customer.dob and customer.dob.strftime("%Y-%m-%d") or '',
					'updated_at': customer.updated_at and customer.updated_at.strftime("%Y-%m-%d %H:%M:%S") or ''
				}
			return abort(400, {'message': 'Can not find record in the system'})
		except KeyError as e:
			abort(500, str(e))
		except Exception as e:
			abort(400, str(e))


@customer.route("/update/<int:id>", methods=['POST'])
@customer.doc(params={'name': 'Customer\'s Name (char)', 'dob': 'Date of birthdate (format: %y-%m-%d)'})
class CustomerUpdate(Resource):
	@jwt_required
	def post(self, id):
		try:
			data = request.json
			updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			customer = Customers.query.filter(Customers.id == id).first()
			if 'name' not in data and 'dob' not in data:
				return abort(400, {'message': 'Can not find name, dob payload '})
			if not customer:
				return abort(400, {'message': 'Can not find record in the system'})
			if 'name' in data:
				customer.name = data['name']
			if 'dob' in data:
				customer.dob = data['dob']
			customer.updated_at = updated_at
			db.session.commit()
			return {
				'id': customer.id,
				'message': 'Record updated is success'
			}
		except KeyError as e:
			abort(500, str(e))
		except Exception as e:
			abort(400, str(e))

@customer.route("/delete/<int:id>", methods=['DELETE'])
class CustomerDelete(Resource):
	@jwt_required
	def delete(self, id):
		try:
			customer = Customers.query.filter(Customers.id == id).first()
			if customer:
				db.session.delete(customer)
				db.session.commit()
				return {'message':'Delete is sucess'}
			return abort(400, {'message': 'Can not find record in the system'})
		except KeyError as e:
			abort(500, str(e))
		except Exception as e:
			abort(400, str(e))

@customer.route("/add", methods=['PUT'])
@customer.doc(params={'name': 'Customer\'s Name (char)', 'dob': 'Date of birthdate (format: %y-%m-%d)'})
class CustomerAdd(Resource):
	@jwt_required
	def put(self):
		try:
			data = request.json
			name = data.get('name','')
			dob = data.get('dob','')
			updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			if not name:
				return {'message': 'name is required'}
			customer = Customers(name="%s"%(name), dob="%s"%(dob), updated_at="%s"%(updated_at))
			db.session.add(customer)
			db.session.commit()
			return {
				'id': customer.id,
				'name': customer.name,
				'dob': customer.dob and customer.dob.strftime("%Y-%m-%d") or '',
				'updated_at': customer.updated_at and customer.updated_at.strftime("%Y-%m-%d %H:%M:%S") or ''
			}
		except KeyError as e:
			abort(500, str(e))
		except Exception as e:
			abort(400, str(e))


if __name__ == "__main__":
	db.create_all()
	flask_app.run(debug=True)
