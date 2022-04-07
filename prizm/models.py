import random
import datetime

from prizm import db

#user model
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	account_number = db.Column(db.Integer, nullable=False)
	balance = db.Column(db.Integer, nullable=False)
	transactions = db.relationship('Transaction', backref='user', cascade='all, delete',lazy=True)


	def __init__(self,full_name,email,password):
		self.full_name = full_name
		self.email = email
		self.password = password
		self.account_number = self.create_account_number()
		self.balance = 0

	def create_account_number(self):
		random_account_number = random.randint(1,1000000000)
		return random_account_number


#Transaction model
class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sender = db.Column(db.String, nullable=False)
	reciever = db.Column(db.String, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date = db.Column(db.String, nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String, nullable=False)


	def __init__(self,sender,reciever,user_id,date,amount,description):
		self.sender = sender
		self.reciever = reciever
		self.user_id = user_id
		self.date = datetime.datetime.now()
		self.amount = amount
		self.description = description
