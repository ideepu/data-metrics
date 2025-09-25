from functools import reduce
from operator import add, mul, sub, truediv
from typing import Callable

from src.base import BaseController
from src.stats.models.stats import Stats
from src.stats.schemas.sum_stats import AggregationType, StatsAggregatorOperationSchema, SumStatsModelSchema


class StatsAggregatorController(BaseController):
    def __init__(self, aggregator_groups: list[StatsAggregatorOperationSchema]):
        super().__init__()
        self.aggregator_groups = aggregator_groups
        self.stats = Stats.get_all()
        self.stats_by_column = SumStatsModelSchema.model_validate_many(
            self.stats,
            from_attributes=True,
        ).group_values_by_keys()
        # TODO: Use polymorphism to handle the operations of each type
        self.operation_maps = {
            AggregationType.ADD: add,
            AggregationType.SUB: sub,
            AggregationType.MULT: mul,
            AggregationType.DIV: truediv,
        }

    def run(self) -> list[list[int]]:
        return self._aggregate_stats_per_operation()

    def _aggregate_stats_per_operation(self) -> list[list[int]]:
        result: list[list[int]] = []
        for group in self.aggregator_groups:
            result.append(self._aggregate_stats_per_group(group))
        return result

    def _safe_reduce(self, op: Callable, values: tuple[float, ...]) -> int:
        try:
            return int(reduce(op, values))
        except ZeroDivisionError:
            return 0

    def _aggregate_stats_per_group(self, group: StatsAggregatorOperationSchema) -> list[int]:
        values_to_aggregate = []
        for column_name in group.operands:
            if isinstance(column_name, StatsAggregatorOperationSchema):
                values_to_aggregate.append(self._aggregate_stats_per_group(column_name))
            else:
                values_to_aggregate.append(self.stats_by_column[column_name])

        return [self._safe_reduce(self.operation_maps[group.operation], values) for values in zip(*values_to_aggregate)]
