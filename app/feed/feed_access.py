# -*- coding: utf-8 -*-

from app import db

import datetime
import time

from app.constants import *
from app.models import Feed, HenFeedRatio, ReadyFeed
from app.cash import cash_access
from . import raw_material_access, formula_access

#update feed
def update(formula, weight):
	feed = get(formula.name)
	feed.weight += weight
	add_price = feed.unit_price*weight
	feed.price += add_price
	db.session.commit()

	add_ready_feed(feed.formula, weight, add_price)

	raw_material_access.update_raw_material_store(formula, weight)

	return feed

# get feed by formula name
def get(formula_name):
	q = Feed.query.filter(Feed.formula == formula_name)
	return q.first()

# update prices of feed
def update_feed_prices():
	feeds = get_all()

	for feed in feeds:
		formula = formula_access.get(feed.formula)
		if formula != None:
			new_price = formula.price / formula.weight
			feed.unit_price = new_price
	db.session.commit()

# update feed prices by formula
def update_feed_price_by_formula(formula):
	feed = get(formula.name)
	new_unit_price = formula.price / formula.weight
	feed.unit_price = new_unit_price
	db.session.commit()

# get not created formulas
def get_all_not_created():
	q = Feed.query.filter(Feed.unit_price <= 0).order_by(Feed.formula.asc())
	return q.all()

# get all feeds
def get_all():
	return Feed.query.order_by(Feed.formula.asc()).all()


def get_feed_ratio(formula):
	q = HenFeedRatio.query.filter(HenFeedRatio.formula == formula)
	return q.first()

# get all hen feed ratio 
def get_hen_feed_ratio_all():
	hen_feed_ratios = HenFeedRatio.query.order_by(HenFeedRatio.formula.asc()).all()
	for hen_feed_ratio in hen_feed_ratios:
		feed = get(hen_feed_ratio.formula)
		hen_feed_ratio.price = hen_feed_ratio.weight * feed.unit_price

	return hen_feed_ratios

# add ready feed log
def add_ready_feed(formula_name, weight, price):
	today = datetime.date.today()
	ready_feed = ReadyFeed(formula_name, weight, price, today)
	db.session.add(ready_feed)
	db.session.commit()

# get all ready feeds
def get_ready_feed_all():
	return ReadyFeed.query.order_by(ReadyFeed.date.desc()).all()