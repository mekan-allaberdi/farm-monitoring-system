from flask import Blueprint

hencoop_bp = Blueprint('hencoop', __name__,
	template_folder='templates', url_prefix='/hencoop')

from .hencoop_view import *