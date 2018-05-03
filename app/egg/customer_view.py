import sys
from flask import render_template, Blueprint, request, redirect, url_for, flash, session
import datetime

from app import db

from . import egg_bp
 
from app.models import Egg, Hencoop, HencoopActivity, Customer, CustomerPayment
from . import egg_access, customer_access
from app.hencoop import hencoop_access
from app.cash import cash_access

from app.constants import *

import logging
log = logging.getLogger()

@egg_bp.route('/customers')
def customers():
	customers = customer_access.get_customer_all()
	return render_template('customer.html', customers = customers)

@egg_bp.route('/new_customer' , methods=['POST'])
def new_customer():
	if request.method == 'POST':
		name = request.form['name']
		phone = request.form['phone']

		if customer_access.exists(name):
			flash(name + ' bar bolan müşderi', category='danger')
			log.debug("new_customer. Exists. Name : %r.", name)
			return redirect(url_for('egg.customers'))

		customer = Customer(name, phone)
		db.session.add(customer)
		db.session.commit()

		flash(name + ' müşderi goşuldy', category='success')
		log.debug("new_customer. Name : %r.", name)
	else:
		log.debug("new_customer. BAD REQUEST")
	return redirect(url_for('egg.customers'))

@egg_bp.route('/customer_info/<string:customer_name>')
def customer_info(customer_name):
	customer = customer_access.get_customer(customer_name)
	customer_payments = customer_access.get_customer_payments(customer_name)
	egg_outs = egg_access.get_egg_out_by_customer(customer_name)
	return render_template('customer_info.html', customer = customer,
		customer_payments = customer_payments, egg_outs = egg_outs)

@egg_bp.route('/add_payment/<string:customer_name>', methods=['POST'])
def add_payment(customer_name):
	if request.method == 'POST':
		amount = float(request.form['amount'])
		today = datetime.date.today()
		customer = customer_access.get_customer(customer_name)
		# add payment
		customer_payment = CustomerPayment(customer.name, amount, today)
		db.session.add(customer_payment)
		db.session.commit()
		# update customer balance
		customer.balance += amount
		customer.received_amount += amount
		db.session.commit()
		# update main cash
		cash_access.add_cash_flow(PAYMENT, customer_name, amount)

		flash(customer_name + ' ' + str(amount) + ' TMT töledi', category='info')
		log.debug("add_payment. Name : %r. Amount : %r", customer_name, amount)
	else:
		log.debug("add_payment. BAD REQUEST")

	return redirect(url_for('egg.customer_info', customer_name = customer_name))
