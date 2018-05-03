import sys
from flask import render_template, Blueprint, request, redirect, url_for, flash, session
import datetime

from app import db

from . import cash_bp
 
from app.models import Employee, Salary, Cash, CashFlow
from . import cash_access, employee_access

from app.constants import *

import logging
log = logging.getLogger()

@cash_bp.route('/employee')
def employee():
	employees = employee_access.get_employee_all()
	return render_template('employee.html', employees = employees)

@cash_bp.route('/new_employee', methods=['POST'])
def new_employee():
	if request.method == 'POST':
		name = request.form['name']
		role = request.form['role']
		today = datetime.date.today()

		if employee_access.exists(name):
			flash(name + ' bar bolan işgär', category='danger')
			log.debug("new_employee. Exists. Name : %r.", name)
			return redirect(url_for('cash.employee'))

		employee = Employee(name, role, today)
		db.session.add(employee)
		db.session.commit()

		flash(name + '-' + role + ' işgär goşuldy', category='success')
		log.debug("new_employee. Name : %r. Role : %r." % (name, role))

	return redirect(url_for('cash.employee'))

@cash_bp.route('/employee_info/<string:employee_name>')
def employee_info(employee_name):
	employee = employee_access.get_employee(employee_name)
	salaries = employee_access.get_employee_salary(employee_name)
	return render_template('employee_info.html', 
		employee = employee, salaries = salaries)

@cash_bp.route('/salary/<string:employee_name>', methods=['POST'])
def salary(employee_name):
	if request.method == 'POST':
		title = request.form['title']
		amount = float(request.form['amount'])
		today = datetime.date.today()
		employee = employee_access.get_employee(employee_name)

		salary = Salary(employee.name, title, amount, today)
		db.session.add(salary)
		db.session.commit()

		employee.balance += amount
		db.session.commit()

		cash_access.add_cash_flow(EXPENSE, employee_name + ":" + title, amount)

		flash(employee_name + '-' + title + ' aýlyk ' + str(amount) + 'TMT berildi.', category='info')
		log.debug("salary. Name : %r. Title : %r. Amount : %r" % (employee_name, title, amount))
	else:
		log.debug('salary. BAD REQUEST.')

	return redirect(url_for('cash.employee_info', employee_name = employee_name))