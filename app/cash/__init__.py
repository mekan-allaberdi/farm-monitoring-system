from flask import Blueprint

cash_bp = Blueprint('cash', __name__,
	template_folder='templates', url_prefix='/cash')

from .cash_view import *
from .employee_view import *