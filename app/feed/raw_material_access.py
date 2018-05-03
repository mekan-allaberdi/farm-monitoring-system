# -*- coding: utf-8 -*-

from app import db

import datetime
import time

from app.constants import *
from app.models import RawMaterial, RawMaterialLog, FormulaRawMaterial
from app.cash import cash_access
from . import formula_access, feed_access

# get raw material
def get(name):
	q = RawMaterial.query.filter(RawMaterial.name == name)
	return q.first()

# add new raw material
def add(name, price):
	price = float(price)
	price = round(price, 5)
	amount = 0
	total_price = 0

	raw_material = RawMaterial(name, amount, price, total_price)
	db.session.add(raw_material)
	db.session.commit()
	return raw_material

# delete raw material
def delete(name):
	RawMaterial.query.filter(RawMaterial.name == name).delete()
	db.session.commit()

# check if raw material exists
def exists(name):
	q = RawMaterial.query.filter(RawMaterial.name == name)
	return q.count() > 0

#  get all raw material
def get_all():
	return RawMaterial.query.order_by(RawMaterial.id.asc()).all()

# check if enough raw material in store
def enough_raw_material(formula, weight):
	q = FormulaRawMaterial.query.filter(FormulaRawMaterial.formula == formula.name)
	formula_raw_materials = q.all() 

	enough = True
	for formula_raw_material in formula_raw_materials:
		raw_material = get(formula_raw_material.rm_name)
		needed_amount = weight * formula_raw_material.percentage / 100
		enough = enough and raw_material.amount >= needed_amount

	return enough

# decrease raw material amount from store
def decrease_amount(raw_material, amount):
	if amount > 0:
		avg_price = raw_material.total_price / raw_material.amount
		raw_material.amount -= amount
		raw_material.total_price -= avg_price * amount
		db.session.commit()

# update raw materials used in formula
def update_raw_material_store(formula, weight):
	q = FormulaRawMaterial.query.filter(FormulaRawMaterial.formula == formula.name)
	formula_raw_materials = q.all()

	for formula_raw_material in formula_raw_materials:
		raw_material = get(formula_raw_material.rm_name)
		amount = weight*formula_raw_material.percentage/100
		decrease_amount(raw_material, amount)

	db.session.commit()

def get_raw_material_amount_per_hen():
	raw_materials = get_all()
	hen_feed_ratios = feed_access.get_hen_feed_ratio_all()
	amount_per_hen = {}

	for raw_material in raw_materials:
		amount = 0
		for hen_feed_ratio in hen_feed_ratios:
			formula = formula_access.get(hen_feed_ratio.formula)
			
			if formula is not None:
				formula_raw_material = formula_access.get_frm_by_formula_and_rmname(formula, raw_material)
				amount += (formula_raw_material.percentage * hen_feed_ratio.weight)/100

		amount_per_hen[raw_material.name] = amount

	return amount_per_hen

#----------------------------------------------------------------------------------
#----------------------------- RAW MATERIAL LOG -----------------------------------
#----------------------------------------------------------------------------------

def get_log(id):
	return RawMaterialLog.query.get(id)

def get_log_all():
	return RawMaterialLog.query.order_by(RawMaterialLog.name.asc()).all()

def add_log(raw_material, amount):
	# add expense to main cash
	total_price = raw_material.price * amount
	cash_flow = cash_access.add_cash_flow(EXPENSE, raw_material.name, total_price)

	today = datetime.date.today()
	raw_material_log = RawMaterialLog(cash_flow.id, raw_material.name, amount, raw_material.price, today)
	db.session.add(raw_material_log)
	db.session.commit()

	return raw_material_log

def edit_log(raw_material_log, price, amount):
	raw_material = get(raw_material_log.name)
	
	# remove old amount
	raw_material.amount -= raw_material_log.amount
	raw_material.total_price -= raw_material_log.amount * raw_material_log.price
	#remove old expense from main cash
	cash_flow = cash_access.get(raw_material_log.cash_flow_id)
	cash_access.delete(cash_flow.id)
	cash_access.update_main_cash(cash_flow.amount)

	# add new amount
	raw_material_log.amount = amount
	raw_material_log.price = price
	raw_material.amount += amount
	# add expence to main cash
	total_price = raw_material_log.price * raw_material_log.amount
	raw_material.total_price += total_price
	cash_flow = cash_access.add_cash_flow("çykdaýjy", raw_material_log.name, total_price)
	raw_material_log.cash_flow_id = cash_flow.id

	db.session.commit()
