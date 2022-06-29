from __future__ import annotations
from datetime import datetime as dt
from typing import Optional
from pydantic import BaseModel, Field

from ofd_elastic.docs.receipt.item import Item
from .enums.doc_type import DocTypeEnum
from .enums.operation_type import OperationTypeEnum
from .enums.system_tax import SystemTaxEnum
from .source import Source
from .total_fd_sum import TotalFdSumRub


class Receipt(BaseModel):
    """https://sbis.ru/help/ofd/api/json/ Смотреть описание чеков тут"""
    index: Optional[str] = Field(..., alias='_index')
    id: Optional[str] = Field(..., alias='_id')
    type: Optional[str] = Field(..., alias='_type')
    source: Source = Field(..., alias='_source')

    @property
    def rnm(self):
        return self.source.requestmessage.kkt_reg_id

    @property
    def fn(self):
        return self.source.requestmessage.fiscal_drive_number

    @property
    def fd(self):
        return self.source.requestmessage.fiscal_document_number

    @property
    def date_time(self) -> dt:
        """
        Дата формирования чека
        """
        return self.source.requestmessage.date_time

    @property
    def receive_datetime(self) -> dt:
        """
        Дата получения чека
        """
        return self.source.meta.receive_time

    @property
    def system_tax(self) -> SystemTaxEnum:
        """
        Применяемая система налогообложения
        """
        return self.source.requestmessage.system_tax

    @property
    def type_doc(self) -> DocTypeEnum:
        """
        Тип документа
        """
        return self.source.requestmessage.code

    @property
    def operation_type(self) -> OperationTypeEnum:
        """
        Тип операции документа
        """
        return self.source.requestmessage.operation_type

    def get_total_fd_sum(self) -> TotalFdSumRub:
        total_fd_sum: TotalFdSumRub = TotalFdSumRub(
            total_sum=(self.source.requestmessage.total_sum_rub or self.source.requestmessage.correction_sum_rub),
            cash_total_sum=self.source.requestmessage.cash_total_sum_rub,
            ecash_total_sum=self.source.requestmessage.ecash_total_sum_rub,
            prepaid_sum=self.source.requestmessage.prepaid_sum_rub,
            credit_sum=self.source.requestmessage.credit_sum_rub,
            provision_sum=self.source.requestmessage.provision_sum_rub
        )
        if self.operation_type in (OperationTypeEnum.return_income, OperationTypeEnum.expenditure):
            total_fd_sum.invert_values()
        return total_fd_sum

    @property
    def item_names(self) -> list[str]:
        return [item.name for item in self.items if item.name]

    @property
    def items(self) -> list[Item]:
        return self.source.requestmessage.items


if __name__ == '__main__':
    pass
