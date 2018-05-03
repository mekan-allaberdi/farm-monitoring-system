from flask import Blueprint

egg_bp = Blueprint('egg', __name__,
	template_folder='templates', url_prefix='/egg')

from .egg_view import *
from .customer_view import *