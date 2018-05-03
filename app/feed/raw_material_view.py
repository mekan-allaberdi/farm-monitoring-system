# -*- coding: utf-8 -*-

import sys
from flask import render_template, Blueprint, request, redirect, url_for, flash, session

from app import db
from . import raw_material_access, formula_access, feed_access
from . import feed_bp

from app.models import RawMaterial, FormulaRawMaterial

import logging
log = logging.getLogger()

@feed_bp.route('/raw_materials')
def raw_materials():
    return render_template('raw_materials.html', raw_materials = raw_material_access.get_all())


@feed_bp.route('/add_raw_material', methods=['POST'])
def add_raw_material():
	if request.method == 'POST':
	    name = request.form['name']
	    price = request.form['price']
		
	    if raw_material_access.exists(name):
	        flash('Bar bolan çig mal', category='danger')
	        log.error("add_raw_material. Name : %r. Bar bolan çig mal", name)
	        return redirect(url_for('feed.raw_materials'))

	    raw_material = raw_material_access.add(name, price)
	    flash(raw_material.name + ' çig mal goşuldy', category='success')
	    log.debug("add_raw_material. Name : %r.", name)
	else:
	    log.debug("add_raw_material. BAD REQUEST. ")
	return redirect(url_for('feed.raw_materials'))


@feed_bp.route('/increase_raw_material/<string:name>', methods=['POST'])
def increase_raw_material(name):
	if request.method == 'POST':
		amount = float(request.form['new_amount'])
		raw_material = raw_material_access.get(name)
		raw_material.amount += amount
		raw_material.total_price += amount * raw_material.price
		db.session.commit()
		raw_material_access.add_log(raw_material, amount)
		flash(raw_material.name + ' çig maly '+ str(amount)+' KG goşuldy', category='info')
		log.debug("increase raw_material. Name : %r, Amount : %r" % (raw_material.name, amount))
	else:
		log.error("increase raw_material. BAD REQUEST")

	return render_template('raw_materials.html', raw_materials = raw_material_access.get_all())


@feed_bp.route('/change_price/<string:name>', methods=['POST'])
def change_price(name):
	if request.method == 'POST':
	    new_price = float(request.form['new_price'])
	    # update raw material
	    raw_material = raw_material_access.get(name)
	    raw_material.price = new_price
	    #update formula's raw material price
	    q = FormulaRawMaterial.query.filter(FormulaRawMaterial.rm_name==raw_material.name)
	    q.update(dict(price=new_price*FormulaRawMaterial.weight))
	    # update formulas
	    formula_access.update_formula_prices()
	    #update feeds
	    feed_access.update_feed_prices()
	    db.session.commit()
	    flash(name + ' bahasy üýtgedi :  ' + str(new_price) , 'warning')
	    log.debug("change_price. Name : %r, NewPrice : %r", name, new_price)
	else:
		log.debug("change_price. BAD REQUEST")
	return redirect(url_for('feed.raw_materials'))


@feed_bp.route('/delete_raw_material/<string:name>', methods=['GET', 'POST'])
def delete_raw_material(name):
        raw_material_access.delete(name)
        flash(name+' çig maly pozuldy', "info")
        log.debug("delete_raw_material. Name : %r", name)
        return redirect(url_for('feed.raw_materials'))

@feed_bp.route('/raw_material_balance')
def raw_material_balance():
    raw_materials = raw_material_access.get_all()
    amount_per_hen = raw_material_access.get_raw_material_amount_per_hen()
    return render_template('raw_material_balance.html',
        raw_materials=raw_materials, amount_per_hen=amount_per_hen)

#-------------------------------------------------------------------------------
#---------------------------------- RAW MATERIAL LOG ---------------------------
#-------------------------------------------------------------------------------

@feed_bp.route('/raw_material_logs')
def raw_material_logs():
	raw_material_logs = raw_material_access.get_log_all()
	return render_template('raw_material_logs.html', raw_material_logs=raw_material_logs)

@feed_bp.route('/edit_raw_material_log/<int:id>', methods=['POST'])
def edit_raw_material_log(id):
    price = float(request.form['price'])
    amount = float(request.form['amount'])
    raw_material_log = raw_material_access.get_log(id)
    raw_material_access.edit_log(raw_material_log, price, amount)
    flash(raw_material_log.name + ' üýtgedildi ' + str(amount) +' KG, ' + str(price) +' TM', 'info')
    log.debug("increase_raw_material. Name : %r, Weight : %r, Price %r", raw_material_log.name, amount, price)
    return redirect(url_for('feed.raw_material_logs'))
