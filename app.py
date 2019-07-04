# -*- coding: utf-8 -*-
#!/usr/bin/python
from flask_restplus import Api, Resource
from controllers.users import user
from controllers.customers import customer
from datetime import datetime
from config import flask_app, db

## define to use swagger UI
app = Api(app = flask_app,
		  version = "1.0",
		  title = "sample-python-api UI",
		  description = "Manage routing of the application")

## define routing
app.add_namespace(user)
app.add_namespace(customer)

if __name__ == "__main__":
	db.create_all()
	flask_app.run(debug=True)
