from flask import Blueprint
from flask_login import login_required

compose_bp = Blueprint('compose', __name__)

@compose_bp.route('/compose')
@login_required
def compose():
  pass
