import sys
from flask import render_template, Blueprint, request, redirect, url_for, flash, session
import datetime

from app import db

from . import cash_bp
 
from app.models import Customer, Cash, CashFlow
from . import cash_access
from app.egg import egg_access, customer_access

from app.constants import *

import logging
log = logging.getLogger()

@cash_bp.route('/')
def cash():
	cash = cash_access.get_main_cash()
	cash_flows = cash_access.get_cash_flows_all()
	return render_template('cash.html',
		cash = cash, cash_flows = cash_flows, 
		EXPENSE = EXPENSE, CASH_IN = CASH_IN,
		CASH_TRANSER = CASH_TRANSER, PAYMENT = PAYMENT)

@cash_bp.route('/add_cash_flow', methods = ['POST'])
def add_cash_flow():
	if request.method == 'POST':
		title = request.form['title']
		description = request.form['description']
		amount = float(request.form['amount'])
		cash_flow = cash_access.add_cash_flow(title, description, amount)
		flash(title + ' ' + description + ' - ' + str(amount) , category='info')
		log.debug("add_cash_flow. TITLE : %r. DESCRIPTION : %r,  Amount : %r", title, description, amount)
	else:
		log.debug("add_cash_flow. BAD REQUEST")

	return redirect(url_for('cash.cash'))