from src.base import BaseView
from src.exceptions import AppInvalidInputException
from src.stats.controllers.stats_aggregator import StatsAggregatorController
from src.stats.controllers.stats_formula_parser import StatsFormulaParserController
from src.stats.schemas.sum_stats import CustomStatsInputSchema


class CustomStatsView(BaseView):
    methods = ['GET']

    def run(self) -> list[int]:
        input_data = self._deserialize_data()
        stats_aggregator_operation = StatsFormulaParserController(input_data.formula).run()
        results = StatsAggregatorController([stats_aggregator_operation]).run()
        if results:
            return results[0]
        return []

    def _deserialize_data(self) -> CustomStatsInputSchema:
        if not self.request_data:
            raise AppInvalidInputException(error_message='Input data is required')

        return CustomStatsInputSchema.model_validate(self.request_data)
