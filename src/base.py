import datetime as dt
from collections import defaultdict
from typing import Any, Iterable, Self, Sequence, TypeVar

from flask import Response, jsonify, request
from flask.views import View
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.db import db_session_manager

T = TypeVar('T', bound='BaseModelSchema')


# Helper methods to operate on list of models
class SchemaList(list[T]):
    def group_values_by_keys(self, keys: set[Any] | None = None) -> dict[Any, list[Any]]:
        grouped_values = defaultdict(list)
        for obj in self:
            for key, value in obj.model_dump(include=keys).items():
                grouped_values[key].append(value)
        return grouped_values


class BaseController:
    def __init__(self) -> None:
        # Handle any context loading here to make it available for all the controllers
        pass

    def run(self) -> Any:
        raise NotImplementedError()


class BaseSchema(PydanticBaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        revalidate_instances='always',
    )


class BaseModelSchema(BaseSchema):
    id: PositiveInt
    created_at: dt.datetime
    updated_at: dt.datetime

    @classmethod
    def model_validate_many(cls, objs: Iterable[Any], **kwargs: Any) -> SchemaList[Self]:
        return SchemaList[Self]([cls.model_validate(obj, **kwargs) for obj in objs])


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[dt.datetime] = mapped_column(
        index=True,
        nullable=False,
        insert_default=lambda: dt.datetime.now(tz=dt.UTC),
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        index=True,
        nullable=False,
        insert_default=lambda: dt.datetime.now(tz=dt.UTC),
        onupdate=lambda: dt.datetime.now(tz=dt.UTC),
    )

    @classmethod
    def get_all(cls) -> Sequence[Self]:
        # Create a cache layer to store the results in the context of the request
        # The subsequent similar requests will use the cached results unless forced to reload
        with db_session_manager.session() as session:
            return session.execute(select(cls)).scalars().all()


class BaseView(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.request_data: dict = request.get_json(silent=True) or {}

    @classmethod
    def view(cls, name: str | None = None):
        return super().as_view(name or cls.__name__)

    def dispatch_request(self, **kwargs: Any) -> Response:
        del kwargs
        return jsonify(self.run())

    def run(self) -> Any:
        raise NotImplementedError()
