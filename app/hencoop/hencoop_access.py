# -*- coding: utf-8 -*-

from app import db

import datetime
import time

from app.constants import *
from app.models import Hencoop, HencoopActivity, HencoopExpense, Feed
from app.cash import cash_access
from app.feed import feed_access

def get_all_hencoops():
	return Hencoop.query.order_by(Hencoop.start_date.asc()).all()

def get_hencoop(id):
	return Hencoop.query.get(id)

def get_hencoop_activity(hencoop, date):
	id = str(date)+str(hencoop.id)
	q = HencoopActivity.query.filter(HencoopActivity.id == id)
	
	if q.count() > 0:
		return q.first()

	return new_hencoop_activity(hencoop, date)

def get_hencoop_activity_all_by_name(hencoop):
	q = HencoopActivity.query.filter(HencoopActivity.hencoop_id == hencoop.id)
	return q.all()

def get_hencoop_activity_all():
	return HencoopActivity.query.order_by(HencoopActivity.date.asc()).all()


def get_hencoop_expense_all(hencoop):
	q = HencoopExpense.query.filter(HencoopExpense.hencoop_id == hencoop.id)
	return q.all()

def add_hencoop(name, hen_count, expenses, date):
	hencoop = Hencoop(name, hen_count, expenses, date)
	db.session.add(hencoop)
	db.session.commit()
	hencoop_expense = HencoopExpense(hencoop.id, hencoop.name, expenses, "Towuk", date)
	db.session.add(hencoop_expense)
	db.session.commit()
	cash_access.add_cash_flow(EXPENSE, hencoop.name + ":" + "Towuk", expenses)

	return hencoop

def new_hencoop_activity(hencoop, date):
	day_number = (date-hencoop.start_date).days
	hen_current = hencoop.hen_initial - hencoop.hen_died
	hencoop_activity = HencoopActivity(hencoop.id, hencoop.name, day_number, hen_current, date)
	db.session.add(hencoop_activity)
	db.session.commit()

	return hencoop_activity

def add_feed(hencoop, hencoop_activity, feed, amount, date):
	if feed.formula == FORMULA1:
		hencoop.formula1 += amount
		hencoop_activity.formula1 += amount
	elif feed.formula == FORMULA2:
		hencoop.formula2 += amount
		hencoop_activity.formula2 += amount
	elif feed.formula == FORMULA3:
		hencoop.formula3 += amount
		hencoop_activity.formula3 += amount

	feed.weight -= amount

	db.session.commit()

def get_performance(hencoop):
	hencoop_activities = get_hencoop_activity_all_by_name(hencoop)

	sum = 0
	for hencoop_activity in hencoop_activities:
		sum += hencoop_activity.egg_produced / hencoop_activity.hen_current

	num_ha = len(hencoop_activities)
	performance = sum / num_ha * 100
	performance = round(performance, 2)

	return performance