from typing import Optional
from pydantic import validator, Field

from .custom_base_model import CustomBaseModel
from .setter_default_or_value import SetterDefaultOrValue


class BuyerInformation(CustomBaseModel):
    buyer: Optional[str] = Field(alias='buyer',
                                 description='покупатель (клиент). Тэг 1227',
                                 allow_mutation=False)
    buyer_inn: Optional[str] = Field(alias='buyerInn',
                                     description='ИНН покупателя (клиента). Тэг 1228',
                                     allow_mutation=False)
    buyer_address: Optional[str] = Field(alias='buyerAddress',
                                         description='Адрес покупателя (клиента). Тэг 1254',
                                         allow_mutation=False)
    buyer_birthday: Optional[str] = Field(alias='buyerBirthday',
                                          description='',
                                          allow_mutation=False)
    buyer_document_code: Optional[str] = Field(alias='buyerDocumentCode',
                                               description='',
                                               allow_mutation=False)

    @validator(
        "buyer",
        "buyer_inn",
        "buyer_address",
        "buyer_birthday",
        "buyer_document_code",
        pre=True,
        always=True,
        check_fields=False)
    def _set_string_fields(cls, value: Optional[str]) -> str:
        return SetterDefaultOrValue.set_str(value)
