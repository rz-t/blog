from flask import blueprints

upload = blueprints.Blueprint('upload', __name__)

from app.upload import image