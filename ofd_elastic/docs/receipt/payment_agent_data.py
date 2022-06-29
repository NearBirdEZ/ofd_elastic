from typing import Union, Optional
from pydantic import validator, Field

from .custom_base_model import CustomBaseModel
from .setter_default_or_value import SetterDefaultOrValue


class PaymentAgentData(CustomBaseModel):
    transfer_operator_phone: Optional[str] = Field(alias='transferOperatorPhone',
                                                   description='Телефон оператора перевода. Тэг 1075',
                                                   allow_mutation=False)
    payment_agent_operation: Optional[str] = Field(alias='paymentAgentOperation',
                                                   description='Операция платежного агента. Тэг 1044',
                                                   allow_mutation=False)
    payment_agent_phone: Optional[str] = Field(alias='paymentAgentPhone',
                                               description='Телефон платежного агента. Тэг 1073',
                                               allow_mutation=False)
    payment_operator_phone: Optional[str] = Field(alias='paymentOperatorPhone',
                                                  description='Телефон оператора по приему платежей. Тэг 1074',
                                                  allow_mutation=False)
    transfer_operator_name: Optional[str] = Field(alias='transferOperatorName',
                                                  description='Наименование оператора перевода. Тэг 1026',
                                                  allow_mutation=False)
    transfer_operator_address: Optional[str] = Field(alias='transferOperatorAddress',
                                                     description='Адрес оператора перевода. Тэг 1005',
                                                     allow_mutation=False)
    transfer_operator_inn: Optional[str] = Field(alias='transferOperatorInn',
                                                 description='ИНН оператора перевода. Тэг 1016',
                                                 allow_mutation=False)

    @validator(
        "transfer_operator_phone",
        "payment_agent_operation",
        "payment_agent_phone",
        "payment_operator_phone",
        "transfer_operator_name",
        "transfer_operator_address",
        "transfer_operator_inn",
        pre=True,
        always=True,
        check_fields=False)
    def _set_list_to_string_fields(cls, value: Optional[Union[list[str], str]]) -> str:
        return SetterDefaultOrValue.set_list_to_str(value)
