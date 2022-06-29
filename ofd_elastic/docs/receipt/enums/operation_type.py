from enum import Enum


class OperationTypeEnum(int, Enum):

    def __new__(cls, value: int, description: str):
        obj: int = int.__new__(cls, value)
        obj._value_ = value
        obj._description = description
        return obj

    income: "OperationTypeEnum" = (1, 'Приход')
    return_income: "OperationTypeEnum" = (2, 'Возврат прихода')
    expenditure: "OperationTypeEnum" = (3, 'Расход')
    return_expenditure: "OperationTypeEnum" = (4, 'Возврат расхода')

    unknown: "OperationTypeEnum" = (-1, 'Тип операции не определен')

    @property
    def description(self) -> str:
        return self._description

    @classmethod
    def _missing_(cls, value) -> "OperationTypeEnum":
        return OperationTypeEnum.unknown

    def __str__(self) -> str:
        return f'{self.value}: {self.description}'
