from sqlalchemy.orm import Session

from src.stats.controllers.stats_aggregator import StatsAggregatorController
from src.stats.models.stats import Stats
from src.stats.schemas.sum_stats import AggregationType, StatsAggregatorOperationSchema
from tests.conftest import BaseTest


class TestStatsAggregator(BaseTest):
    def test_stats_aggregator_general_operations(self, session: Session):
        session.add_all(
            [
                Stats(
                    column_1=1,
                    column_2=2,
                    column_3=3,
                    column_4=4,
                    column_5=5,
                ),
                Stats(
                    column_1=6,
                    column_2=7,
                    column_3=8,
                    column_4=9,
                    column_5=10,
                ),
                Stats(
                    column_1=11,
                    column_2=12,
                    column_3=13,
                    column_4=14,
                    column_5=15,
                ),
            ]
        )
        session.commit()
        results = StatsAggregatorController(
            [StatsAggregatorOperationSchema(operation=AggregationType.ADD, operands=['column_1', 'column_2'])]
        ).run()
        assert results[0] == [3, 13, 23]

        results = StatsAggregatorController(
            [
                StatsAggregatorOperationSchema(
                    operation=AggregationType.MULT, operands=['column_1', 'column_3', 'column_5']
                )
            ]
        ).run()
        assert results[0] == [15, 480, 2145]

        # Multiple operations
        results = StatsAggregatorController(
            [
                StatsAggregatorOperationSchema(operation=AggregationType.ADD, operands=['column_1', 'column_5']),
                StatsAggregatorOperationSchema(
                    operation=AggregationType.MULT,
                    operands=['column_2', 'column_4', 'column_5'],
                ),
            ]
        ).run()
        assert results[0] == [6, 16, 26]
        assert results[1] == [40, 630, 2520]

        # Complex Operations
        group_1 = StatsAggregatorOperationSchema(operation=AggregationType.SUB, operands=['column_1', 'column_5'])
        group_2 = StatsAggregatorOperationSchema(operation=AggregationType.MULT, operands=['column_2', 'column_3'])
        group_3 = StatsAggregatorOperationSchema(operation=AggregationType.ADD, operands=[group_1, 'column_1', group_2])
        group_4 = StatsAggregatorOperationSchema(operation=AggregationType.DIV, operands=[group_1, group_2])
        grouped = StatsAggregatorOperationSchema(operation=AggregationType.ADD, operands=[group_3, group_4, 'column_4'])
        results = StatsAggregatorController([grouped]).run()
        assert results[0] == [7, 67, 177]

    def test_stats_aggregator_large_dataset(self, session: Session):
        stats = [Stats(column_1=12, column_2=2, column_3=45, column_4=-14, column_5=56) for _ in range(1000)]
        session.add_all(stats)
        session.commit()
        results = StatsAggregatorController(
            [StatsAggregatorOperationSchema(operation=AggregationType.ADD, operands=['column_1', 'column_2'])]
        ).run()
        assert results[0] == [14] * 1000

        results = StatsAggregatorController(
            [
                StatsAggregatorOperationSchema(
                    operation=AggregationType.MULT, operands=['column_1', 'column_3', 'column_4']
                )
            ]
        ).run()
        assert results[0] == [-7560] * 1000

    def test_stats_aggregator_zero_division(self, session: Session):
        session.add_all(
            [
                Stats(column_1=0, column_2=2, column_3=3, column_4=4, column_5=5),
            ]
        )
        session.commit()
        results = StatsAggregatorController(
            [StatsAggregatorOperationSchema(operation=AggregationType.DIV, operands=['column_2', 'column_1'])]
        ).run()
        assert results[0] == [0]
