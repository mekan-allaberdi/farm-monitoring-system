# -*- coding: utf-8 -*-

from app import db

import datetime
import time

from app.constants import *
from app.models import Employee, Salary, Cash, CashFlow

def get_employee(name):
	q = Employee.query.filter(Employee.name == name)
	return q.first()

def get_employee_all():
	return Employee.query.order_by(Employee.name.asc()).all()

def get_employee_salary(employee_name):
	q = Salary.query.filter(Salary.employee == employee_name)
	return q.order_by(Salary.date.asc()).all()

def exists(name):
	q = Employee.query.filter(Employee.name == name)
	return q.count() > 0
