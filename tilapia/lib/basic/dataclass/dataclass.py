import json
from dataclasses import asdict, fields, replace
from decimal import Decimal
from typing import Set

from tilapia.lib.basic.functional.json import json_stringify


class DataClassMixin(object):
    def clone(self, **kwargs):
        # noinspection PyDataclass
        return replace(self, **kwargs)

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            data = dict()

        # noinspection PyArgumentList
        return cls(**data)

    def to_dict(self) -> dict:
        # noinspection PyDataclass
        return asdict(self)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str) if json_str else None
        data = cls._solve_decimal_fields(data)
        return cls.from_dict(data)

    @classmethod
    def _load_decimal_fields(cls) -> Set[str]:
        cache_name = "__decimal_fields"
        decimal_fields = getattr(cls, cache_name, None)

        if decimal_fields is None:
            # noinspection PyDataclass
            decimal_fields = {i.name for i in fields(cls) if i.type is Decimal}
            setattr(cls, cache_name, decimal_fields)

        return decimal_fields

    @classmethod
    def _solve_decimal_fields(cls, data: dict) -> dict:
        decimal_fields = cls._load_decimal_fields()

        if decimal_fields:
            data = {k: Decimal(v) if k in decimal_fields else v for k, v in data.items()}

        return data

    def to_json(self):
        return json_stringify(self.to_dict())
