# -*- coding: utf-8 -*-

from app import db

import datetime
import time

from app.constants import *
from app.models import Cash, CashFlow

def update_main_cash(amount):
	cash = get_main_cash()
	cash.date = datetime.date.today()
	cash.amount += amount
	cash.amount = round(cash.amount, 2) 
	db.session.commit()

def get_main_cash():
	return Cash.query.filter(Cash.title == MAIN_CASH).first()

def get_cash_flows_all():
	return CashFlow.query.order_by(CashFlow.date.asc()).all()

def add_cash_flow(title, description, amount):
	today = datetime.date.today()
	cash_flow = CashFlow(title, description, amount, today)
	db.session.add(cash_flow)
	db.session.commit()

	print(title)

	if title == EXPENSE or title == CASH_TRANSER:
		amount *= -1
	
	update_main_cash(amount)

	return cash_flow

def get(id):
	return CashFlow.query.get(id)
	
def get_all_cash_flows():
	return CashFlow.query.order_by(CashFlow.date.asc()).all()

def delete(id):
	CashFlow.query.filter(CashFlow.id == id).delete()
	db.session.commit()
