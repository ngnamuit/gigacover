# -*- coding: utf-8 -*-
#!/usr/bin/python
from flask import Flask, request, abort
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



flask_app = Flask(__name__)
flask_app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://giga:1@localhost/giga' ## connect postgresql database
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True ## enable database debug logs
db = SQLAlchemy(flask_app)

## config to use swagger UI
app = Api(app = flask_app,
		  version = "1.0",
		  title = "RestAPIs UI",
		  description = "Manage routing of the application")
## Define TABLE
class Customers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	dob = db.Column(db.Date)
	updated_at = db.Column(db.DateTime)
## define routing
customer = app.namespace('customer', description='Customer')
@customer.route("/get/<int:id>", methods=['GET'])
class Customer(Resource):
	def get(self, id):
		try:
			customer = Customers.query.filter(Customers.id == id).first()
			if customer:
				return {
					'id': customer.id,
					'name': customer.name,
					'dob': customer.dob and customer.dob.strftime("%Y-%m-%d") or '',
					'updated_at': customer.updated_at and customer.updated_at.strftime("%Y-%m-%d") or ''
				}
			return abort(400, {'message': 'Can not find record in the system'})
		except KeyError as e:
			abort(500, str(e))
		except Exception as e:
			abort(400, str(e))


@customer.route("/update/<int:id>", methods=['POST'])
@customer.doc(params={'name': 'Customer\'s Name (char)', 'dob': 'Date of birthdate (format: %y-%m-%d)'})
class CustomerUpdate(Resource):
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
				'updated_at': customer.updated_at and customer.updated_at.strftime("%Y-%m-%d") or ''
			}
		except KeyError as e:
			abort(500, str(e))
		except Exception as e:
			abort(400, str(e))

if __name__ == "__main__":
	db.create_all()
	flask_app.run(debug=True)