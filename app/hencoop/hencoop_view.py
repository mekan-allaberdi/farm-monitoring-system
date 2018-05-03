# -*- coding: utf-8 -*-

import sys
from flask import render_template, Blueprint, request, redirect, url_for, flash, session
import datetime

from app import db

from . import hencoop_bp
 
from app.models import Hencoop, HencoopActivity, HencoopExpense
from . import hencoop_access
from app.egg import egg_access
from app.feed import feed_access
from app.cash import cash_access

from app.constants import *

import logging
log = logging.getLogger()

@hencoop_bp.route('/')
def hencoops():
	return render_template('hencoops.html',
		hencoops = hencoop_access.get_all_hencoops())


@hencoop_bp.route('/add_hencoop', methods=['POST'])
def add_hencoop():
	if request.method == 'POST':
		name = request.form['name']
		hen_count = int(request.form['hen_count'])
		hen_price = float(request.form['hen_price'])
		start_date = request.form['start_date']
		start_date_obj = datetime.datetime.strptime(start_date, '%d/%m/%Y').date()
		expense = float(hen_count) * hen_price

		hencoop = hencoop_access.add_hencoop(name, hen_count, expense, start_date_obj)
		flash(hencoop.name + ' goşuldy', category='success')
		log.debug("add_hencoop. Name : %r.", hencoop.name)
	else:
	    log.debug("add_hencoop. BAD REQUEST. ")

	return render_template('hencoops.html',
		hencoops = hencoop_access.get_all_hencoops())

@hencoop_bp.route('/info/<int:hencoop_id>')
def info(hencoop_id):
	hencoop = hencoop_access.get_hencoop(hencoop_id)
	today = datetime.date.today()
	hencoop_activity = hencoop_access.get_hencoop_activity(hencoop, today)
	hencoop_activities = hencoop_access.get_hencoop_activity_all_by_name(hencoop)
	hencoop_expenses = hencoop_access.get_hencoop_expense_all(hencoop)
	performance = hencoop_access.get_performance(hencoop)
	return render_template('hencoop_info.html', hencoop = hencoop, 
		hencoop_activity = hencoop_activity, hencoop_activities = hencoop_activities,
		hencoop_expenses = hencoop_expenses, performance = performance)


@hencoop_bp.route('/new_hen_died/<int:hencoop_id>', methods=['POST'])
def new_hen_died(hencoop_id):
	if request.method == 'POST':
		count = int(request.form['hen_count'])
		hencoop = hencoop_access.get_hencoop(hencoop_id)
		today = datetime.date.today()
		
		hencoop_activity = hencoop_access.get_hencoop_activity(hencoop, today)
		hencoop_activity.hen_died += count
		hencoop_activity.hen_current -= count
		hencoop.hen_died += count
		db.session.commit()
		flash(hencoop.name + ' ' + str(count)+' towuk gyryldy', category='info')
		log.debug("new_hen_died. hencoop : %r, count : %r" % (hencoop.name, count))
	else:
	    log.debug("new_hen_died. BAD REQUEST. ")

	return redirect(url_for('hencoop.info', hencoop_id = hencoop_id))


@hencoop_bp.route('/new_hen_expense/<int:hencoop_id>', methods=['POST'])
def new_hen_expense(hencoop_id):
	if request.method == 'POST':
		title = request.form['expense_title']
		amount = float(request.form['expense_amount'])
		hencoop = hencoop_access.get_hencoop(hencoop_id)
		today = datetime.date.today()
		
		hencoop_expense = HencoopExpense(hencoop.id, hencoop.name, amount, title, today)
		db.session.add(hencoop_expense)
		hencoop.expenses += amount
		db.session.commit()

		cash_flow = cash_access.add_cash_flow(EXPENSE, hencoop.name + ":" + title, amount)
		
		flash(hencoop.name + ' ' + title + '-' +str(amount)+' çykdaýjy goşuldy', category='info')
		log.debug("new_hen_expense. hencoop : %r, title : %r, amount : %r." % (hencoop.name, title, amount))
	else:
	    log.debug("new_hen_expense. BAD REQUEST. ")

	return redirect(url_for('hencoop.info', hencoop_id = hencoop_id))


@hencoop_bp.route('/new_egg_production/<int:hencoop_id>', methods=['POST'])
def new_egg_production(hencoop_id):
	if request.method == 'POST':
		count = int(request.form['egg_produced'])
		hencoop = hencoop_access.get_hencoop(hencoop_id)
		today = datetime.date.today()
		
		hencoop_activity = hencoop_access.get_hencoop_activity(hencoop, today)
		hencoop_activity.egg_produced += count
		hencoop.egg_produced += count
		db.session.commit()

		egg_access.new_egg_in(count, hencoop)
		
		flash(hencoop.name + ' ' + str(count) + ' yumurtga goşuldy', category='info')
		log.debug("new_egg_production. hencoop : %r, count : %r." % (hencoop.name, count))
	else:
	    log.debug("new_egg_production. BAD REQUEST. ")

	return redirect(url_for('hencoop.info', hencoop_id = hencoop_id))


@hencoop_bp.route('/new_egg_broken/<int:hencoop_id>', methods=['POST'])
def new_egg_broken(hencoop_id):
	if request.method == 'POST':
		count = int(request.form['egg_broken'])
		hencoop = hencoop_access.get_hencoop(hencoop_id)
		today = datetime.date.today()
		
		hencoop_activity = hencoop_access.get_hencoop_activity(hencoop, today)
		hencoop_activity.egg_broken += count
		hencoop.egg_broken += count
		db.session.commit()
		
		egg_access.new_egg_broken_in(count, hencoop)

		flash(hencoop.name + ' ' + str(count) + ' yumurtga dowuldi', category='info')
		log.debug("new_egg_broken. hencoop : %r, count : %r." % (hencoop.name, count))
	else:
	    log.debug("new_egg_broken. BAD REQUEST. ")

	return redirect(url_for('hencoop.info', hencoop_id = hencoop_id))


@hencoop_bp.route('/new_feed/<int:hencoop_id>', methods=['POST'])
def new_feed(hencoop_id):
	if request.method == 'POST':
		formula = request.form['formula_selected']
		amount = float(request.form['feed_amount'])
		hencoop = hencoop_access.get_hencoop(hencoop_id)
		today = datetime.date.today()
		hencoop_activity = hencoop_access.get_hencoop_activity(hencoop, today)
		feed = feed_access.get(formula)

		if feed.weight < amount:
			flash(hencoop.name + ' ' + formula + '-' +str(amount)+' Yeterli iym yok', category='warning')
			log.debug("Not enough feed. new_feed. hencoop : %r, formula : %r, amount : %r." % (hencoop.name, formula, amount))
			return redirect(url_for('hencoop.info', hencoop_id = hencoop_id))

		hencoop_access.add_feed(hencoop, hencoop_activity, feed, amount, today)
		
		flash(hencoop.name + ' ' + formula + '-' +str(amount)+' iým goşuldy', category='info')
		log.debug("new_feed. hencoop : %r, formula : %r, amount : %r." % (hencoop.name, formula, amount))
	else:
	    log.debug("new_hen_expense. BAD REQUEST. ")

	return redirect(url_for('hencoop.info', hencoop_id = hencoop_id))
