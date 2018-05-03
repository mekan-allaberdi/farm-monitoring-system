# -*- coding: utf-8 -*-

import sys
from flask import render_template, Blueprint, request, redirect, url_for, flash, session

from app import db
from . import raw_material_access, formula_access, feed_access
from . import feed_bp

from app.models import Formula, FormulaRawMaterial

import logging
log = logging.getLogger()

@feed_bp.route('/new_formula')
def new_formula():
    return render_template('new_formula.html', raw_materials = raw_material_access.get_all(), 
        not_created_formulas = feed_access.get_all_not_created())

@feed_bp.route('/add_formula', methods=['POST'])
def add_formula():
	if request.method == 'POST':
	    raw_materials = raw_material_access.get_all()
	    totalWeight = 0
	    totalPrice = 0
	    name = request.form['formula_name']

	    formula = formula_access.get(name)
	    if formula is not None:
	    	flash('Bar bolan sort: ' + name, category='danger')
	    	log.debug("add_formula. Existing formula. Name : %r", name)
	    	return redirect(url_for('feed.new_formula'))
	    
	    for raw_material in raw_materials:
	        weight = float(request.form[raw_material.name])
	        totalWeight += weight

	    for raw_material in raw_materials:
	        weight = float(request.form[raw_material.name])
	        percentage = weight/totalWeight*100;
	        percentage = round(percentage, 2)
	        price = raw_material.price * weight
	        totalPrice += price
	        formula_access.add_raw_material(name, raw_material.name, weight, percentage, price)

	    totalPrice = round(totalPrice, 3)
	    formula_access.add(name, totalWeight, totalPrice)

	    log.debug("add_formula. Name : %r, Weight : %r, Price : %r", name, str(totalWeight), str(totalPrice))
	else:
		log.debug("add_formula. BAD REQUEST. ")

	return redirect(url_for('feed.new_formula'))

@feed_bp.route('/formula/<string:name>', methods=['GET', 'POST'])
def formula(name):
    formula = formula_access.get(name)

    if formula is None:
        flash(name + ' ýasalmadyk', "danger")
        log.debug("show_formula. No formula. Name : %r", name)
        return render_template('formulas.html', formulas = formula_access.get_all())

    q = FormulaRawMaterial.query.filter(FormulaRawMaterial.formula == formula.name)
    formula_raw_materials = q.all()
    return render_template('formula_view.html', formula = formula,
    	formula_raw_materials = formula_raw_materials)

@feed_bp.route('/formulas')
def formulas():
    return render_template('formulas.html', formulas = formula_access.get_all())

@feed_bp.route('/delete_formula/<string:name>', methods=['GET', 'POST'])
def delete_formula(name):
    formula_access.delete(name)
    log.debug("delete_formula. Name : %r", name)
    return redirect(url_for('show_formulas'))
