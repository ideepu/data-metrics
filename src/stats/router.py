from flask import Blueprint

from src.stats.views.custom_stats import CustomStatsView
from src.stats.views.sum_stats import SumStatsView

stats_blueprint = Blueprint('stats', __name__, url_prefix='/stats')

stats_blueprint.add_url_rule('/sum', view_func=SumStatsView.view())
stats_blueprint.add_url_rule('/custom', view_func=CustomStatsView.view())
