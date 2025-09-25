from flask import Blueprint

from src.stats.router import stats_blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api_blueprint.register_blueprint(stats_blueprint)
