from typing import Optional, Union, Any
from datetime import datetime as dt


class SetterDefaultOrValue:

    @staticmethod
    def set_bool(value: Optional[bool]) -> bool:
        return not not value

    @staticmethod
    def set_date_time(value: Optional[Union[int, float]]) -> dt:
        return dt(1970, 1, 1) if value is None else dt.utcfromtimestamp(value)

    @staticmethod
    def set_number(value: Optional[Union[int, float]]) -> Union[int, float]:
        return 0 if value is None else value

    @staticmethod
    def set_rub(value: Optional[int]) -> float:
        validated_value: int = SetterDefaultOrValue.set_number(value)
        return round(validated_value / 100, 2)

    @staticmethod
    def set_list_to_str(value: Optional[Union[list[str], str]]) -> str:
        if value is None:
            return ''
        if isinstance(value, list):
            return ', '.join(value)
        return value

    @staticmethod
    def set_str(value: Optional[str]) -> str:
        return '' if value is None else value.strip()

    @staticmethod
    def set_obj_to_list_obj(value: Optional[Union[list[Any], Any]]) -> list[Any]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    @classmethod
    def set_union(cls, value: Any) -> Any:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, (int, float)):
            return cls.set_number(value)
