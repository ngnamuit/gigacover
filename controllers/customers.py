# -*- coding: utf-8 -*-
#!/usr/bin/python
from flask import request, abort
from flask_restplus import Namespace, Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from datetime import datetime
from models.customers import Customers

customer_model = Customers()
customer = Namespace('customer', description='Customer')
@customer.route("/get/<int:id>", methods=['GET'])
class Customer(Resource):
	@jwt_required
	def get(self, id):
		try:
			customer = customer_model.query.filter(Customers.id == id).first()
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
			customer = customer_model.query.filter(Customers.id == id).first()
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
			customer = customer_model.query.filter(Customers.id == id).first()
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
			customer = customer_model(name="%s"%(name), dob="%s"%(dob), updated_at="%s"%(updated_at))
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
