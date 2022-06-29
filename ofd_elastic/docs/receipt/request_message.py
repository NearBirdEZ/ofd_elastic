from typing import Optional, Union, Any
from datetime import datetime as dt
from pydantic import validator, Field

from .buyer_information import BuyerInformation
from .custom_base_model import CustomBaseModel
from .enums.doc_type import DocTypeEnum
from .enums.operation_type import OperationTypeEnum
from .enums.system_tax import SystemTaxEnum
from .item import Item
from .setter_default_or_value import SetterDefaultOrValue


class Requestmessage(CustomBaseModel):
    user: Optional[str] = Field(alias='user',
                                description='Наименование пользователя. Тэг 1048',
                                allow_mutation=False)
    user_inn: Optional[str] = Field(alias='userInn',
                                    description='ИНН пользователя. Тэг 1018',
                                    allow_mutation=False)
    retail_place_address: Optional[str] = Field(alias='retailPlaceAddress',
                                                description='Адрес расчетов. Тэг 1009 (аналог с retailAddress)',
                                                allow_mutation=False)
    retail_place: Optional[str] = Field(alias='retailPlace',
                                        description='Mесто расчетов. Тэг 1187',
                                        allow_mutation=False)
    retail_address: Optional[str] = Field(alias='retailAddress',
                                          description='Адрес расчетов. Тэг 1009 (аналог с retailPlaceAddress)',
                                          allow_mutation=False)
    kkt_reg_id: Optional[str] = Field(alias='kktRegId',
                                      description='Регистрационный номер ККТ. Тэг 1037',
                                      allow_mutation=False)
    fiscal_drive_number: Optional[str] = Field(alias='fiscalDriveNumber',
                                               description='Заводской номер фискального накопителя. Тэг 1041',
                                               allow_mutation=False)
    code: Optional[DocTypeEnum] = Field(alias='code',
                                        description='Код документа. Тэг 3, 4',
                                        allow_mutation=False)
    shift_number: Optional[int] = Field(alias='shiftNumber',
                                        description='Номер смены. Тэг 1038',
                                        allow_mutation=False)
    request_number: Optional[int] = Field(alias='requestNumber',
                                          description='Номер чека за смену. Тэг 1042',
                                          allow_mutation=False)
    fiscal_document_number: Optional[int] = Field(alias='fiscalDocumentNumber',
                                                  description='Порядковый номер фискального документа. Тэг 1040',
                                                  allow_mutation=False)
    date_time: Optional[dt] = Field(alias='dateTime',
                                    description='Дата чека. Тэг 1012',
                                    allow_mutation=False)
    operation_type: Optional[OperationTypeEnum] = Field(alias='operationType',
                                                        description='Признак расчета. Тэг 1054',
                                                        allow_mutation=False)
    applied_taxation_type: Optional[SystemTaxEnum] = Field(alias='appliedTaxationType',
                                                           description='Применяемая система налогообложения.'
                                                                       'Тэг 1055 (taxationType)',
                                                           allow_mutation=False)
    taxation_type: Optional[SystemTaxEnum] = Field(alias='taxationType',
                                                   description='Применяемая система налогообложения.'
                                                               'Тэг 1055 (appliedTaxationType)',
                                                   allow_mutation=False)
    total_sum_rub: Optional[float] = Field(alias='totalSum',
                                           description='Итог. Тэг 1020',
                                           allow_mutation=False)
    correction_sum_rub: Optional[float] = Field(alias='correctionSum',
                                                description='Unknown',
                                                allow_mutation=False)
    cash_total_sum_rub: Optional[float] = Field(alias='cashTotalSum',
                                                description='Форма расчета — наличными. Тэг 1031',
                                                allow_mutation=False)
    ecash_total_sum_rub: Optional[float] = Field(alias='ecashTotalSum',
                                                 description='Форма расчета — электронными. Тэг 1081',
                                                 allow_mutation=False)
    nds18_rub: Optional[float] = Field(alias='nds18',
                                       description='НДС итога чека со ставкой 18%. Тэг 1102')
    nds20_rub: Optional[float] = Field(alias='nds20',
                                       description='Custom field')
    nds18118_rub: Optional[float] = Field(alias='nds18118',
                                          description='Сумма НДС чека по расч. Ставке 20/120.'
                                                      'Тэг 1106 (взаимозаменяемы с ndsCalculated18)')
    nds20120_rub: Optional[float] = Field(alias='nds20120',
                                          description='Custom field')
    nds10110_rub: Optional[float] = Field(alias='nds10110',
                                          description='Сумма НДС чека по расч. Ставке 10/110.'
                                                      'Тэг 1107 (взаимозаменяемы с ndsCalculated10)')
    nds_calculated10_rub: Optional[float] = Field(alias='ndsCalculated10',
                                                  description='Сумма НДС чека по расч. Ставке 10/110.'
                                                              'Тэг 1107 (взаимозаменяемы с ndsCalculated10)',
                                                  allow_mutation=False)
    nds_calculated18_rub: Optional[float] = Field(alias='ndsCalculated18',
                                                  description='Сумма НДС чека по расч. Ставке 20/120.'
                                                              'Тэг 1106 (взаимозаменяемы с nds18118)')
    nds10_rub: Optional[float] = Field(alias='nds10',
                                       description='НДС итога чека со ставкой 10%. Тэг 103')

    nds0_rub: Optional[float] = Field(alias='nds0',
                                      description='НДС итога чека со ставкой 0%. Тэг 1104',
                                      allow_mutation=False)
    nds_no_rub: Optional[float] = Field(alias='ndsNo',
                                        description='Сумма расчета по чеку без НДС. Тэг 1105',
                                        allow_mutation=False)
    prepaid_sum_rub: Optional[float] = Field(alias='prepaidSum',
                                             description='Сумма по чеку (БСО) предоплатой (зачетом аванса и (или)'
                                                         'предыдущих платежей). Тэг 1215',
                                             allow_mutation=False)
    credit_sum_rub: Optional[float] = Field(alias='creditSum',
                                            description='Сумма по чеку (БСО) постоплатой (в кредит). Тэг 1216',
                                            allow_mutation=False)
    provision_sum_rub: Optional[float] = Field(alias='provisionSum',
                                               description='Сумма по чеку (БСО) встречным предоставлением. Тэг 1217',
                                               allow_mutation=False)
    buyer_phone_or_address: Optional[str] = Field(alias='buyerPhoneOrAddress',
                                                  description='Адрес покупателя. Тэг 1008',
                                                  allow_mutation=False)
    buyer: Optional[str] = Field(alias='buyer',
                                 description='Покупатель. Тэг 1227',
                                 allow_mutation=False)
    buyer_inn: Optional[str] = Field(alias='buyerInn',
                                     description='ИНН покупателя. Тэг 1228',
                                     allow_mutation=False)
    operator: Optional[str] = Field(alias='operator',
                                    description='Кассир. Тэг 1021',
                                    allow_mutation=False)
    operator_inn: Optional[str] = Field(alias='operatorInn',
                                        description='ИНН кассира. Тэг 1203',
                                        allow_mutation=False)
    fiscal_sign: Optional[int] = Field(alias='fiscalSign',
                                       description='Фискальный признак документа. Тэг 1077',
                                       allow_mutation=False)
    items: Optional[list[Item]] = Field(alias='items',
                                        description='Предметы расчета. Тэг 1059',
                                        allow_mutation=False)

    fiscal_document_format_ver: Optional[int] = Field(alias='fiscalDocumentFormatVer',
                                                      description='Номер версии ФФД. Тэг 1209',
                                                      allow_mutation=False)
    payment_agent_phone: Optional[str] = Field(alias='paymentAgentPhone',
                                               description='Телефон платежного агента. Тэг 1073',
                                               allow_mutation=False)
    payment_operator_phone: Optional[str] = Field(alias='paymentOperatorPhone',
                                                  description='Телефон оператора по приему платежей. Тэг 1074',
                                                  allow_mutation=False)
    transfer_operator_phone: Optional[str] = Field(alias='transferOperatorPhone',
                                                   description='Телефон оператора перевода. Тэг 1075',
                                                   allow_mutation=False)
    checking_labeled_prod_result: Optional[int] = Field(alias='checkingLabeledProdResult',
                                                        description='Результаты проверки маркированных товаров. '
                                                                    'Тэг 2107',
                                                        allow_mutation=False)

    # TODO раньше бралось первое значение, поэтому тип BuyerInformation
    buyer_information: Optional[list[BuyerInformation]] = Field(alias='buyerInformation',
                                                                description='Сведения о покупателе (клиенте). Тэг 1256',
                                                                allow_mutation=False)

    @validator(
        "user",
        "user_inn",
        "retail_place_address",
        "retail_place",
        "retail_address",
        "kkt_reg_id",
        "fiscal_drive_number",
        "buyer_phone_or_address",
        "buyer",
        "buyer_inn",
        "operator",
        "operator_inn",
        "transfer_operator_phone",
        pre=True,
        always=True,
        check_fields=False)
    def _set_string_fields(cls, value: Optional[str]) -> str:
        return SetterDefaultOrValue.set_str(value)

    @validator("shift_number",
               "request_number",
               "fiscal_document_number",
               "fiscal_sign",
               "fiscal_document_format_ver",
               "checking_labeled_prod_result",
               pre=True,
               always=True,
               check_fields=False)
    def _set_int_fields(cls, value: Optional[int]) -> int:
        return SetterDefaultOrValue.set_number(value)

    @validator(
        "total_sum_rub",
        "correction_sum_rub",
        "cash_total_sum_rub",
        "ecash_total_sum_rub",
        "nds18_rub",
        "nds20_rub",
        "nds18118_rub",
        "nds20120_rub",
        "nds10110_rub",
        "nds_calculated10_rub",
        "nds_calculated18_rub",
        "nds10_rub",
        "nds_no_rub",
        "prepaid_sum_rub",
        "credit_sum_rub",
        "provision_sum_rub",
        pre=True,
        always=True,
        check_fields=False)
    def _set_rub_fields(cls, value: Optional[int]) -> float:
        return SetterDefaultOrValue.set_rub(value)

    @validator("applied_taxation_type",
               "taxation_type",
               pre=True,
               always=True,
               check_fields=False)
    def _set_system_tax(cls, value: Optional[int]) -> SystemTaxEnum:
        return SystemTaxEnum(value)

    @validator("operation_type",
               pre=True,
               always=True,
               check_fields=False)
    def _set_operation_type(cls, value: Optional[int]) -> OperationTypeEnum:
        return OperationTypeEnum(value)

    @validator("payment_agent_phone",
               "payment_operator_phone",
               pre=True,
               always=True,
               check_fields=False)
    def _set_list_to_string_fields(cls, value: Optional[Union[list[str], str]]) -> str:
        return SetterDefaultOrValue.set_list_to_str(value)

    @validator("code",
               pre=True,
               always=True,
               check_fields=False)
    def _set_code(cls, value: Optional[int]) -> DocTypeEnum:
        return DocTypeEnum(value)

    @validator("date_time", pre=True, always=True, check_fields=False)
    def _set_date_time(cls, value: Optional[int]) -> dt:
        return SetterDefaultOrValue.set_date_time(value)

    @validator("items", pre=True, always=True, check_fields=False)
    def _set_items(cls, value: Optional[Union[list[Item], Item]]) -> list[Item]:
        return SetterDefaultOrValue.set_obj_to_list_obj(value)

    @validator("buyer_information", pre=True, always=True, check_fields=False)
    def _set_buyer_information(cls, value: Optional[Union[list[Item], Item]]) -> list[BuyerInformation]:
        return SetterDefaultOrValue.set_obj_to_list_obj(value)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._nds_setter()

    def _nds_setter(self) -> None:
        date_20_percent_nds: dt = dt(2019, 1, 1, 0, 0, 0)
        if self.date_time >= date_20_percent_nds:
            self.nds20_rub = self.nds18_rub
            self.nds18_rub = 0
            self.nds20120_rub = self.nds18118_rub or self.nds_calculated18_rub
            self.nds18118_rub = 0
            self.nds10110_rub = self.nds10110_rub or self.nds_calculated10_rub

    @property
    def system_tax(self) -> SystemTaxEnum:
        if self.applied_taxation_type is not SystemTaxEnum.unknown:
            return self.applied_taxation_type
        return self.taxation_type

    def address(self) -> str:
        if self.retail_place_address:
            return self.retail_place_address
        if self.retail_address:
            return self.retail_address
        if self.retail_place:
            return self.retail_place
