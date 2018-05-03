# -*- coding: utf-8 -*-

from app import db

import datetime
import time

from app.constants import *
from app.models import Egg, EggIn, EggOut, Customer

def update_total_egg(count):
	q = Egg.query.filter(Egg.id == 'total')

	if (q.count() > 0):
		egg_total = q.first()
		egg_total.egg_count += count
		db.session.commit()

def update_total_egg_broken(count):
	q = Egg.query.filter(Egg.id == 'total')

	if (q.count() > 0):
		egg_total = q.first()
		egg_total.broken_count += count
		db.session.commit()

def new_egg_in(count, hencoop):
	update_total_egg(count)
	egg_in = EggIn(hencoop.id, count, datetime.date.today())
	db.session.add(egg_in)
	db.session.commit()
	return egg_in

def new_egg_out(count, price, customer):
	update_total_egg(-1 * count)
	egg_out = EggOut(customer.name, count, price, datetime.date.today())
	db.session.add(egg_out)
	db.session.commit()
	return egg_out

def new_egg_broken_in(count, hencoop):
	update_total_egg_broken(count)

def get_total_egg():
	return Egg.query.filter(Egg.id == 'total').first()

def get_egg_out_all():
	return EggOut.query.order_by(EggOut.date.asc()).all()

def get_egg_out_by_customer(customer_name):
	q = EggOut.query.filter(EggOut.customer == customer_name)
	return q.order_by(EggOut.date.asc()).all()
	