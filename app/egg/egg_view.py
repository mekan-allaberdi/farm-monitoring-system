import sys
from flask import render_template, Blueprint, request, redirect, url_for, flash, session
import datetime

from app import db

from . import egg_bp
 
from app.models import Egg, EggOut, Hencoop, HencoopActivity, Customer
from . import egg_access, customer_access
from app.hencoop import hencoop_access
from app.cash import cash_access

from app.constants import *

import logging
log = logging.getLogger()

@egg_bp.route('/')
def egg_store():
	egg = egg_access.get_total_egg()
	hencoop_activities = hencoop_access.get_hencoop_activity_all()
	return render_template('egg_store.html',
		hencoop_activities = hencoop_activities, egg = egg)

@egg_bp.route('/sale')
def egg_sale():
	egg = egg_access.get_total_egg()
	egg_outs = egg_access.get_egg_out_all()
	customers = customer_access.get_customer_all()
	return render_template('egg_out.html', 
		customers = customers, egg = egg, egg_outs = egg_outs)

@egg_bp.route('/new_sale', methods=['POST'])	
def new_sale():
	name = request.form['customer']
	count = int(request.form['count'])
	price = float(request.form['price'])
	customer = customer_access.get_customer(name)
	today = datetime.date.today()

	# new egg sale
	egg_out = EggOut(customer.name, count, price, today)
	db.session.add(egg_out)
	db.session.commit()

	# update total egg
	egg = egg_access.get_total_egg()
	egg.egg_count -= count
	# update customer balance
	total_price = float(count) * price 
	customer.debt += total_price
	customer.balance -= total_price
	
	db.session.commit()

	return redirect(url_for('egg.egg_sale'))