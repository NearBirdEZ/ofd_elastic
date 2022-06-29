from enum import Enum


class DocTypeEnum(int, Enum):

    def __new__(cls, value: int, description: str):
        obj: int = int.__new__(cls, value)
        obj._value_ = value
        obj._description = description
        return obj

    registration_report: "DocTypeEnum" = (1, "Отчет о регистрации")
    shift_opening_report: "DocTypeEnum" = (2, "Отчет об открытии смены")
    receipt: "DocTypeEnum" = (3, "Кассовый чек")
    strict_reporting_form: "DocTypeEnum" = (4, "Бланк строгой отчетности")
    shift_closing_report: "DocTypeEnum" = (5, "Отчёт о закрытии смены")
    fiscal_storage_closure_report: "DocTypeEnum" = (6, "Отчёт о закрытии фискального накопителя")
    report_on_changes_in_registration_parameters: "DocTypeEnum" = (11, "Отчёт об изменении параметров регистрации")
    report_on_current_status_of_calculations: "DocTypeEnum" = (21, "Отчёт о текущем состоянии расчетов")
    receipt_correction: "DocTypeEnum" = (31, "Кассовый чек коррекции")
    strict_reporting_form_correction: "DocTypeEnum" = (41, "Бланк строгой отчетности коррекции")

    unknown: "DocTypeEnum" = (-1, 'Тип документа не определен')

    @property
    def description(self) -> str:
        return self._description

    @classmethod
    def _missing_(cls, value) -> "DocTypeEnum":
        return DocTypeEnum.unknown

    def __str__(self) -> str:
        return f'{self.value}: {self.description}'
