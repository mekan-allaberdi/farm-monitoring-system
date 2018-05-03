# -*- coding: utf-8 -*-

from app import db

import datetime
import time

from sqlalchemy import func

from app.constants import *
from app.models import RawMaterial, Formula, FormulaRawMaterial
from app.cash import cash_access
from . import raw_material_access, feed_access

def add(name, weight, price):
	formula = Formula(name, weight, price)
	db.session.add(formula)
	db.session.commit()

	# update feed unit price
	feed = feed_access.get(formula.name)
	new_unit_price = formula.price / formula.weight
	feed.unit_price = new_unit_price
	db.session.commit()

	return formula

def add_raw_material(formula, raw_material_name, weight, percentage, price):
	formula_rm = FormulaRawMaterial(formula, raw_material_name, weight, percentage, price)
	db.session.add(formula_rm)
	db.session.commit()
	return formula_rm

def get(name):
	q = Formula.query.filter(Formula.name == name)
	return q.first()

def get_all():
	return Formula.query.order_by(Formula.name.asc()).all()

def delete(name):
	Formula.query.filter(Formula.name == name).delete()
	db.session.commit()
	delete_rm_by_formula(name)
	feed_access.feed_not_created(name)

def update_formula_prices():
	formulas = get_all()
	for formula in formulas:
		cursor = FormulaRawMaterial.query.with_entities(func.sum(FormulaRawMaterial.price)).filter(FormulaRawMaterial.formula==formula.name)
		price = cursor.scalar()
		formula.price = price
	db.session.commit()

def get_frm_by_formula_and_rmname(formula, raw_material):
	q = FormulaRawMaterial.query.filter(FormulaRawMaterial.formula == formula.name)
	q = q.filter(FormulaRawMaterial.rm_name == raw_material.name)
	return q.first()

	