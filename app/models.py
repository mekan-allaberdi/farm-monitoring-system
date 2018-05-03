# -*- coding: utf-8 -*-

from app import db
from flask_sqlalchemy import event
from sqlalchemy import DDL
import datetime

from app.constants import *

class Cash(db.Model):
	__tablename__ = 'cash'
	title = db.Column(db.String(20), primary_key=True)
	amount = db.Column(db.Float)
	date = db.Column(db.Date)

	def __init__(self, title, amount, date):
	    self.title = title
	    self.amount = amount
	    self.date = date

class CashFlow(db.Model):
	__tablename__ = 'cash_flow'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(20))
	description = db.Column(db.String(60))
	amount = db.Column(db.Float)
	date = db.Column(db.Date)

	def __init__(self, title, description, amount, date):
	    self.title = title
	    self.amount = amount
	    self.description = description
	    self.date = date

class User(db.Model):
	__tablename__ = 'user'
	username = db.Column(db.String(50), primary_key=True)
	password = db.Column(db.String(30))
	role = db.Column(db.String(50))
	last_login = db.Column(db.DateTime)

	def __init__(self, username, password, role):
	    self.username = username
	    self.password = password
	    self.role = role

class RawMaterial(db.Model):
	__tablename__ = 'raw_materials'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique=True)
	amount = db.Column(db.Float)
	price = db.Column(db.Float)
	total_price = db.Column(db.Float)

	def __init__(self, name, amount, price, total_price):
	    self.name = name
	    self.amount = amount
	    self.price = price
	    self.total_price = total_price

class RawMaterialLog(db.Model):
	__tablename__ = 'raw_material_logs'
	id = db.Column(db.Integer, primary_key = True)
	cash_flow_id = db.Column(db.Integer)
	name = db.Column(db.String(100), db.ForeignKey(RawMaterial.__tablename__ + '.name'), nullable=False)
	price =  db.Column(db.Float)
	amount = db.Column(db.Float)
	date = db.Column(db.Date)

	def __init__(self, cash_flow_id, name, amount, price, date):
		self.cash_flow_id = cash_flow_id
		self.name = name
		self.price = price
		self.amount = amount
		self.date = date

class Formula(db.Model):
	__tablename__ = 'formula'
	name = db.Column(db.String(50), primary_key=True)
	weight = db.Column(db.Float)
	price = db.Column(db.Float)

	def __init__(self, name, weight, price):
	    self.name = name
	    self.weight = weight
	    self.price = price

class FormulaRawMaterial(db.Model):
	__tablename__ = 'formula_rm'
	id = db.Column(db.Integer, primary_key = True)
	formula = db.Column(db.String(50), db.ForeignKey(Formula.__tablename__ + '.name'), nullable=False)
	rm_name = db.Column(db.String(100), db.ForeignKey(RawMaterial.__tablename__ + '.name'), nullable=False)
	weight = db.Column(db.Float)
	percentage = db.Column(db.Float)
	price = db.Column(db.Float)

	def __init__(self, formula, rm_name, weight, percentage, price):
	    self.formula = formula
	    self.rm_name = rm_name
	    self.weight = weight
	    self.percentage = percentage
	    self.price = price

class Feed(db.Model):
	__tablename__ = 'feed'
	formula = db.Column(db.String(50), primary_key=True)
	weight = db.Column(db.Float)
	price = db.Column(db.Float)
	unit_price = db.Column(db.Float)

	def __init__(self, formula, weight, price, unit_price):
	    self.formula = formula
	    self.weight = weight
	    self.price = price
	    self.unit_price = unit_price

class ReadyFeed(db.Model):
	__tablename__ = 'ready_feed'
	id = db.Column(db.Integer, primary_key = True)
	formula = db.Column(db.String(50))
	weight = db.Column(db.Float)
	price = db.Column(db.Float)
	date = db.Column(db.Date)

	def __init__(self, formula, weight, price, date):
	    self.formula = formula
	    self.weight = weight
	    self.price = price
	    self.date = date

class HenFeedRatio(db.Model):
	__tablename__ = 'hen_feed_ratio'
	id = db.Column(db.Integer, primary_key = True)
	formula = db.Column(db.String(50), db.ForeignKey(Feed.__tablename__ + '.formula'), nullable=False)
	weight = db.Column(db.Float)
	price = db.Column(db.Float)

	def __init__(self, formula, weight, price):
	    self.formula = formula
	    self.weight = weight
	    self.price = price

class Hencoop(db.Model):
	__tablename__ = 'hencoop'
	id = db.Column(db.Integer, primary_key = True)	
	name = db.Column(db.String(30))
	hen_initial = db.Column(db.Integer)
	hen_current = db.Column(db.Integer)
	hen_died = db.Column(db.Integer)
	egg_produced = db.Column(db.Integer)
	egg_broken = db.Column(db.Integer)
	formula1 = db.Column(db.Float)
	formula2 = db.Column(db.Float)
	formula3 = db.Column(db.Float)
	formula4 = db.Column(db.Float)
	expenses = db.Column(db.Float)
	start_date = db.Column(db.Date)
	last_updated = db.Column(db.Date)
	closed = db.Column(db.Boolean)

	def __init__(self, name, hen_initial, expenses, start_date):
		self.name = name
		self.hen_initial = hen_initial
		self.hen_current = hen_initial
		self.hen_died = 0
		self.egg_produced = 0
		self.egg_broken = 0
		self.formula1 = 0
		self.formula2 = 0
		self.formula3 = 0
		self.formula4 = 0
		self.expenses = expenses
		self.start_date = start_date
		self.last_updated = start_date
		self.closed = False


class HencoopActivity(db.Model):
	__tablename__ = 'hencoop_activity'
	id = db.Column(db.String(40), primary_key = True)
	hencoop_id = db.Column(db.Integer, db.ForeignKey(Hencoop.__tablename__ + '.id'), nullable=False)
	hencoop_name = db.Column(db.String(30), db.ForeignKey(Hencoop.__tablename__ + '.name'), nullable=False)
	day_number = db.Column(db.String(5))
	hen_current = db.Column(db.Integer)
	hen_died = db.Column(db.Integer)
	egg_produced = db.Column(db.Integer)
	egg_broken = db.Column(db.Integer)
	formula1 = db.Column(db.Float)
	formula2 = db.Column(db.Float)
	formula3 = db.Column(db.Float)
	formula4 = db.Column(db.Float)
	date = db.Column(db.Date)

	def __init__(self, hencoop_id, hencoop_name, day_number, hen_current, date):
		self.id = str(date)+str(hencoop_id)
		self.hencoop_id = hencoop_id
		self.hencoop_name = hencoop_name
		self.day_number = day_number
		self.hen_current = hen_current
		self.hen_died = 0
		self.egg_produced = 0
		self.egg_broken = 0
		self.formula1 = 0
		self.formula2 = 0
		self.formula3 = 0
		self.formula4 = 0
		self.expense = 0
		self.date = date

class HencoopExpense(db.Model):
	__tablename__ = 'hencoop_expense'
	id = db.Column(db.Integer, primary_key = True)	
	hencoop_id = db.Column(db.Integer, db.ForeignKey(Hencoop.__tablename__ + '.id'), nullable=False)
	hencoop_name = db.Column(db.String(30), db.ForeignKey(Hencoop.__tablename__ + '.name'), nullable=False)
	amount = db.Column(db.Float)
	title = db.Column(db.String(30))
	date = db.Column(db.Date)

	def __init__(self, hencoop_id, hencoop_name, amount, title, date):
		self.hencoop_id = hencoop_id
		self.hencoop_name = hencoop_name
		self.amount = amount
		self.title = title
		self.date = date

class Customer(db.Model):
	__tablename__ = 'customer'
	name = db.Column(db.String(40), primary_key = True)
	phone = db.Column(db.String(30))
	debt = db.Column(db.Float)
	received_amount = db.Column(db.Float)	
	balance = db.Column(db.Float)	

	def __init__(self, name, phone):
		self.name = name
		self.phone = phone
		self.debt = 0
		self.received_amount = 0
		self.balance = 0

class CustomerPayment(db.Model):
	__tablename__ = 'customer_payment'
	id = db.Column(db.Integer, primary_key = True)
	customer = db.Column(db.String(60), db.ForeignKey(Customer.__tablename__ + '.name'), nullable=False)
	amount = db.Column(db.Float)	
	date = db.Column(db.Date)

	def __init__(self, customer, amount, date):
	    self.customer = customer
	    self.amount = amount
	    self.date = date


class Egg(db.Model):
	__tablename__ = 'egg'
	id = db.Column(db.String(20), primary_key = True)	
	egg_count =  db.Column(db.Integer)
	broken_count =  db.Column(db.Integer)
	last_updated = db.Column(db.Date)

	def __init__(self, id, egg_count, broken_count, last_updated):
		self.id = id
		self.egg_count = egg_count
		self.broken_count = broken_count
		self.last_updated = last_updated

class EggIn(db.Model):
	__tablename__ = 'egg_in'
	id = db.Column(db.Integer, primary_key = True)	
	hencoop_id = db.Column(db.Integer, db.ForeignKey(Hencoop.__tablename__ + '.id'), nullable=False)
	count =  db.Column(db.Integer)
	date = db.Column(db.Date)

	def __init__(self, hencoop_id, count, date):
		self.hencoop_id = hencoop_id
		self.count = count
		self.date = date

class EggOut(db.Model):
	__tablename__ = 'egg_out'
	id = db.Column(db.Integer, primary_key = True)	
	customer = db.Column(db.Integer, db.ForeignKey(Customer.__tablename__ + '.name'), nullable=False)
	count =  db.Column(db.Integer)
	price = db.Column(db.Float)
	date = db.Column(db.Date)

	def __init__(self, customer, count, price, date):
		self.customer = customer
		self.count = count
		self.price = price
		self.date = date

class Employee(db.Model):
	__tablename__ = 'employee'
	name = db.Column(db.String(40), primary_key = True)
	role = db.Column(db.String(30))
	balance = db.Column(db.Float)
	start_date = db.Column(db.Date)

	def __init__(self, name, role, start_date):
		self.name = name
		self.role = role
		self.balance = 0
		self.start_date = start_date

class Salary(db.Model):
	__tablename__ = 'salary'
	id = db.Column(db.Integer, primary_key = True)
	employee = db.Column(db.String(40), db.ForeignKey(Employee.__tablename__ + '.name'), nullable=False)
	title = db.Column(db.String(20))
	amount = db.Column(db.Float)	
	date = db.Column(db.Date)

	def __init__(self, employee, title, amount, date):
	    self.employee = employee
	    self.title = title
	    self.amount = amount
	    self.date = date
#-----------------------------------------------------------------------------------------
#-------------------------------- DEFAULTS------------------------------------------------
#-----------------------------------------------------------------------------------------

@event.listens_for(User.__table__, 'after_create')
def dbDefaultUsers(*args, **kwargs):    
    # admin user
    admin = User("admin", "Merw.2017", ROLES['admin'])
    db.session.add(admin)
    yazberdi = User("yazberdi", "Merw.2017", ROLES['inspector'])
    db.session.add(yazberdi)
    rowshen = User("aydogdy", "Merw.2017", ROLES['employee'])
    db.session.add(rowshen)
    db.session.commit()

@event.listens_for(Cash.__table__, 'after_create')
def dbDefaultCash(*args, **kwargs):
    # total hen count
    cash = Cash(MAIN_CASH, 0, datetime.date.today())
    db.session.add(cash)
    db.session.commit()

@event.listens_for(Egg.__table__, 'after_create')
def dbDefaultEgg(*args, **kwargs):
    # total hen count
    egg = Egg('total', 0, 0, datetime.date.today())
    db.session.add(egg)
    db.session.commit()

@event.listens_for(Feed.__table__, 'after_create')
def dbDefaultFeeds(*args, **kwargs):
    # formulas in feed
    for formula in FORMULAS:
    	feed_formula = Feed(formula, 0, 0, 0)
    	db.session.add(feed_formula)

    db.session.commit()

@event.listens_for(HenFeedRatio.__table__, 'after_create')
def dbDefaultHenFeedRatio(*args, **kwargs):
    feed_ratio1 = HenFeedRatio(FORMULA1, 0.45, 0)
    feed_ratio2 = HenFeedRatio(FORMULA2, 1.75, 0)
    feed_ratio3 = HenFeedRatio(FORMULA3, 2.20, 0)
    feed_ratio4 = HenFeedRatio(FORMULA4, 0, 0)
    db.session.add(feed_ratio1)
    db.session.add(feed_ratio2)
    db.session.add(feed_ratio3)
    db.session.add(feed_ratio4)
    db.session.commit()

@event.listens_for(RawMaterial.__table__, 'after_create')
def dbDefaultRawMaterials(*args, **kwargs):
	primeks = RawMaterial("Primeks", 0, 2.85, 0)
	soya = RawMaterial("Soýa", 0, 3.4, 0)
	bugday = RawMaterial("Bugdaý", 0, 0.95, 0)
	mekge = RawMaterial("Mekge", 0, 0.8, 0)
	balykgulak = RawMaterial("Balykgulak", 0, 5, 0)
	yag = RawMaterial("Ýag", 0, 2.7, 0)
	duz = RawMaterial("Duz", 0, 3.5, 0)
	db.session.add(primeks)
	db.session.add(soya)
	db.session.add(bugday)
	db.session.add(mekge)
	db.session.add(balykgulak)
	db.session.add(yag)
	db.session.add(duz)
	db.session.commit()