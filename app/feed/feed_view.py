import sys
from flask import render_template, Blueprint, request, redirect, url_for, flash, session

from app import db
from . import formula_access, feed_access, raw_material_access
from . import feed_bp

from sqlalchemy import func

from app.models import Formula, Feed, HenFeedRatio

import logging
log = logging.getLogger()

@feed_bp.route('/feeds')
def feeds():
    return render_template('feeds.html', 
    	feeds = feed_access.get_all(),
    	formulas = formula_access.get_all(),
    	hen_feed_ratios = feed_access.get_hen_feed_ratio_all())

@feed_bp.route('/new_feed', methods=['POST'])
def new_feed():
	if request.method == 'POST':
		formula_name= request.form['formula_selected']
		formula = formula_access.get(formula_name)
		weight = float(request.form['weight'])

		if raw_material_access.enough_raw_material(formula, weight) == False:
			flash(formula.name + ' iym yasamak ucin yeterlik çig mal yok', category='danger')
			return redirect(url_for('feed.feeds'))

		feed_access.update(formula, weight)

		log.debug("new_feed. Formula : %r, Weight : %r", formula_name, weight)
	else:
		log.error("new_feed. BAD REQUEST")
	return redirect(url_for('feed.feeds'))

@feed_bp.route('/hen_feed_ratios')
def hen_feed_ratios():
	hen_feed_ratios = feed_access.get_hen_feed_ratio_all()
	# total weight
	cursor = HenFeedRatio.query.with_entities(func.sum(HenFeedRatio.weight))
	total_weight = cursor.scalar()
	# total price
	total_price = 0
	for hen_feed_ratio in hen_feed_ratios:
		total_price += hen_feed_ratio.price	
	return render_template('hen_feed_ratio.html', 	hen_feed_ratios = hen_feed_ratios, total_price = total_price)

@feed_bp.route('/feed_ratio_change_weight/<string:name>', methods=['POST'])
def feed_ratio_change_weight(name):
	if request.method == 'POST':
		weight = request.form['weight']
		feed_ratio = feed_access.get_feed_ratio(name)
		feed_ratio.weight = weight
		db.session.commit()
		log.debug("feed_ratio_change_weight. Name : %r, Weight : %r", name, weight)
	else:
		log.error("feed_ratio_change_weight. BAD REQUEST.")
	return redirect(url_for('feed.hen_feed_ratios'))

@feed_bp.route('/ready_feeds')
def ready_feeds():
    return render_template('ready_feeds.html', ready_feeds = feed_access.get_ready_feed_all())
