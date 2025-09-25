import pytest
from sqlalchemy.orm import Session

from src.stats.models.stats import Stats
from tests.conftest import BaseTest


class TestCustomStats(BaseTest):
    ENDPOINT = 'api/stats/custom'

    @pytest.fixture(autouse=True)
    def prepare_database(self, session: Session):
        session.add_all(
            [
                Stats(column_1=1, column_2=2, column_3=3, column_4=4, column_5=5),
                Stats(column_1=10, column_2=20, column_3=30, column_4=40, column_5=50),
                Stats(column_1=100, column_2=200, column_3=300, column_4=400, column_5=500),
                Stats(column_1=1000, column_2=2000, column_3=3000, column_4=4000, column_5=5000),
            ]
        )
        session.commit()

    def test_custom_stats_invalid_input(self):
        # Empty input
        response = self.client.get(self.ENDPOINT, json={})
        assert response.status_code == 400
        assert response.json == {'error': 'Input data is required', 'error_code': 'INVALID_INPUT', 'error_details': {}}

        # Exceeding max length
        response = self.client.get(self.ENDPOINT, json={'formula': 'a' * 1001})
        assert response.status_code == 400
        assert response.json == {
            'error': [
                {
                    'input': 'a' * 1001,
                    'loc': ['formula'],
                    'msg': 'String should have at most 1000 characters',
                    'type': 'string_too_long',
                }
            ]
        }

        # Below min length
        response = self.client.get(self.ENDPOINT, json={'formula': 'a' * 16})
        assert response.status_code == 400
        assert response.json == {
            'error': [
                {
                    'input': 'a' * 16,
                    'loc': ['formula'],
                    'msg': 'String should have at least 17 characters',
                    'type': 'string_too_short',
                }
            ]
        }

        # Invalid operator
        response = self.client.get(self.ENDPOINT, json={'formula': 'column_1 % column_2'})
        assert response.status_code == 400
        assert response.json == {
            'error': [
                {
                    'input': 'Mod',
                    'loc': ['operation'],
                    'msg': "Input should be 'Add', 'Sub', 'Mult' or 'Div'",
                    'type': 'enum',
                }
            ]
        }

    def test_custom_stats(self):
        response = self.client.get(
            self.ENDPOINT,
            json={'formula': 'column_1 + column_1 + column_2 * column_3 + column_4 / column_5 - column_2 - column_3'},
        )
        assert response.status_code == 200
        assert response.json == [3, 570, 59700, 5997000]
