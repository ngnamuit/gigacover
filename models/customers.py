from datetime import datetime
from config import db

class Customers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256), nullable=False)
	dob = db.Column(db.Date)
	updated_at = db.Column(db.DateTime)

