# -*- coding: utf-8 -*-

from app import db

import datetime
import time

from app.constants import *
from app.models import Egg, EggIn, EggOut, Customer, CustomerPayment, Cash, CashFlow

def get_customer(name):
	q = Customer.query.filter(Customer.name == name)
	return q.first()

def exists(name):
	q = Customer.query.filter(Customer.name == name)
	return q.count() > 0

def get_customer_all():
	return Customer.query.order_by(Customer.name.asc()).all()

def get_customer_payments(name):
	q = CustomerPayment.query.filter(CustomerPayment.customer == name)
	return q.order_by(CustomerPayment.date.asc()).all()