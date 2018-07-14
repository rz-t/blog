from flask import blueprints

web = blueprints.Blueprint('web', __name__)

from app.web import home
from app.web import wooyun
from app.web import error
from app.web import note