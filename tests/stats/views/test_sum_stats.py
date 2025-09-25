import pytest
from sqlalchemy.orm import Session

from src.stats.models.stats import Stats
from tests.conftest import BaseTest


class TestSumStats(BaseTest):
    ENDPOINT = 'api/stats/sum'

    @pytest.fixture(autouse=True)
    def prepare_database(self, session: Session):
        session.add_all(
            [
                Stats(column_1=1, column_2=2, column_3=3, column_4=4, column_5=5),
            ]
        )
        session.commit()

    def test_sum_stats(self):
        response = self.client.get(
            self.ENDPOINT, json={'first_column_name': 'column_1', 'second_column_name': 'column_5'}
        )
        assert response.status_code == 200
        assert response.json == [6]

    def test_sum_stats_invalid_input(self):
        # Empty input
        response = self.client.get(self.ENDPOINT, json={})
        assert response.status_code == 400
        assert response.json == {'error': 'Input data is required', 'error_code': 'INVALID_INPUT', 'error_details': {}}

        # Invalid column name
        response = self.client.get(
            self.ENDPOINT, json={'first_column_name': 'invalid', 'second_column_name': 'column_5'}
        )
        assert response.status_code == 400
        assert response.json == {
            'error': [
                {
                    'input': 'invalid',
                    'loc': ['first_column_name'],
                    'msg': "Input should be 'column_1', 'column_2', 'column_3', 'column_4' or 'column_5'",
                    'type': 'literal_error',
                }
            ]
        }
