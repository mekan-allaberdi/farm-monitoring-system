from flask import Blueprint

feed_bp = Blueprint('feed', __name__,
	template_folder='templates', url_prefix='/feed')

from .raw_material_view import *
from .formula_view import *
from .feed_view import *