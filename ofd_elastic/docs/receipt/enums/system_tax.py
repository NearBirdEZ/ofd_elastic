from enum import Enum


class SystemTaxEnum(int, Enum):

    def __new__(cls, value: int, description: str):
        obj: int = int.__new__(cls, value)
        obj._value_ = value
        obj._description = description
        return obj

    general_taxation_system: "SystemTaxEnum" = (1, 'ОСН')
    simplified_taxation_system_income: "SystemTaxEnum" = (2, 'УСН доход')
    simplified_taxation_system_income_expense: "SystemTaxEnum" = (4, 'УСН доход-расход')
    unified_tax_on_imputed_income: "SystemTaxEnum" = (8, 'ЕНВД')
    unified_agricultural_tax: "SystemTaxEnum" = (16, 'ЕСХН')
    patent: "SystemTaxEnum" = (32, 'Патент')

    unknown: "SystemTaxEnum" = (-1, 'Система налогообложения не определена')

    @property
    def description(self) -> str:
        return self._description

    @classmethod
    def _missing_(cls, value) -> "SystemTaxEnum":
        return SystemTaxEnum.unknown

    def __str__(self) -> str:
        return f'{self.value}: {self.description}'

    def __repr__(self) -> str:
        return f'{self.value}: {self.description}'
