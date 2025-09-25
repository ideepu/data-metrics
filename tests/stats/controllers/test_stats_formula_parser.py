from src.exceptions import AppInvalidInputException
from src.stats.controllers.stats_formula_parser import StatsFormulaParserController
from src.stats.schemas.sum_stats import AggregationType, StatsAggregatorOperationSchema
from tests.conftest import BaseTest


class TestStatsFormulaParser(BaseTest):
    def test_parse_formula_invalid(self):
        # Invalid syntax
        formula = 'column_1 + '
        with self.assert_raises(AppInvalidInputException):
            StatsFormulaParserController(formula).run()

        # Invalid schema
        formula = 'columns_1'
        with self.assert_raises(AppInvalidInputException):
            StatsFormulaParserController(formula).run()

        # Invalid expression
        formula = 'not column_1'
        with self.assert_raises(AppInvalidInputException):
            StatsFormulaParserController(formula).run()

    def test_parse_formula(self):
        formula = 'column_1 + column_2 * column_3'
        schema = StatsFormulaParserController(formula).run()
        mult_schema = StatsAggregatorOperationSchema(operation=AggregationType.MULT, operands=['column_2', 'column_3'])
        assert schema.operation == AggregationType.ADD
        assert schema.operands[0] == 'column_1'
        assert isinstance(schema.operands[1], StatsAggregatorOperationSchema)
        assert schema.operands[1].operation == mult_schema.operation
        assert schema.operands[1].operands == mult_schema.operands
        assert schema.model_dump(mode='json') == {
            'operation': 'Add',
            'operands': ['column_1', {'operation': 'Mult', 'operands': ['column_2', 'column_3']}],
        }
