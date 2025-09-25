from random import randint

from src.base import BaseModel
from src.db import db_session_manager
from src.stats.models.stats import Stats

MIN = -10
MAX = 100


def prepare_database() -> None:
    BaseModel.metadata.create_all(db_session_manager.engine)
    with db_session_manager.session() as session:
        if Stats.get_all():
            return

        stats = [
            Stats(
                column_1=randint(MIN, MAX),
                column_2=randint(MIN, MAX),
                column_3=randint(MIN, MAX),
                column_4=randint(MIN, MAX),
                column_5=randint(MIN, MAX),
            )
            for _ in range(10)
        ]
        session.add_all(stats)
        session.commit()
