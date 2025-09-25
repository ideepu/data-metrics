import ast
from typing import Any

from src.base import BaseController
from src.exceptions import AppInvalidInputException
from src.stats.schemas.sum_stats import StatsAggregatorOperationSchema


# Build a better parse to group the operands with same operations together
# Have an option to allow ( and ) to group the operands together
class StatsFormulaParserController(BaseController):
    def __init__(self, formula: str):
        super().__init__()
        self.formula = formula

    def run(self) -> StatsAggregatorOperationSchema:
        return self._parse_formula_to_schema()

    def _parse_formula_to_schema(self) -> StatsAggregatorOperationSchema:
        """
        Parses a formula string like "column_1 + column_2 * column_3"
        into a nested StatsAggregatorOperationSchema as per operator precedence.
        """
        expr = self._parse_formula(self.formula)
        schema = self._parse_to_schema(expr)
        if not isinstance(schema, StatsAggregatorOperationSchema):
            raise AppInvalidInputException(error_message='Invalid formula', field_name='formula')
        return schema

    def _parse_formula(self, formula: str) -> ast.AST:
        try:
            return ast.parse(formula, mode='eval').body
        except SyntaxError as e:
            raise AppInvalidInputException(error_message='Invalid formula syntax', field_name='formula') from e

    def _parse_to_schema(self, node: ast.AST) -> Any:
        if isinstance(node, ast.BinOp):
            return StatsAggregatorOperationSchema(
                operation=type(node.op).__name__,
                operands=[self._parse_to_schema(node.left), self._parse_to_schema(node.right)],
            )
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        raise AppInvalidInputException(error_message='Unsupported formula', field_name='formula')
