from sqlalchemy.orm import Session

from src.stats.models.stats import Stats
from tests.conftest import BaseTest


class TestStats(BaseTest):
    def test_stats_model(self):
        stat = Stats(
            column_1=1,
            column_2=2,
            column_3=3,
            column_4=4,
            column_5=5,
        )
        assert stat.column_1 == 1
        assert stat.column_2 == 2
        assert stat.column_3 == 3
        assert stat.column_4 == 4
        assert stat.column_5 == 5

    def test_stats_model_get_all(self, session: Session):
        session.add(
            Stats(
                column_1=1,
                column_2=2,
                column_3=3,
                column_4=4,
                column_5=5,
            )
        )
        session.commit()
        stats = Stats.get_all()
        assert len(stats) == 1
        assert stats[0].column_1 == 1
        assert stats[0].column_2 == 2
        assert stats[0].column_3 == 3
        assert stats[0].column_4 == 4
        assert stats[0].column_5 == 5
