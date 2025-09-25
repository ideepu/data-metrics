import ast
from enum import Enum
from typing import Literal, Self

from pydantic import Field

from src.base import BaseModelSchema, BaseSchema


class SumStatsModelSchema(BaseModelSchema):
    column_1: int
    column_2: int
    column_3: int
    column_4: int
    column_5: int


SumStatsModelColumn = Literal['column_1', 'column_2', 'column_3', 'column_4', 'column_5']


class AggregationType(Enum):
    ADD = ast.Add.__name__
    SUB = ast.Sub.__name__
    MULT = ast.Mult.__name__
    DIV = ast.Div.__name__


# The nested self references is hard to parse and serialize. Needs a better schema definition
class StatsAggregatorOperationSchema(BaseSchema):
    operation: AggregationType
    operands: list[SumStatsModelColumn | Self] = Field(min_length=2)


class SumStatsInputSchema(BaseSchema):
    first_column_name: SumStatsModelColumn
    second_column_name: SumStatsModelColumn


class CustomStatsInputSchema(BaseSchema):
    formula: str = Field(min_length=17, max_length=1000)
