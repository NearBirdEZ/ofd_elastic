from typing import Optional, Union

from pydantic import Field, validator

from .custom_base_model import CustomBaseModel
from .labeled_prod_fractional_quantity import LabeledProdFractionalQuantity as Fract
from .payment_agent_data import PaymentAgentData as PaymentAgent
from .product_code_new import ProductCodeNew as ProdCodeNew
from .provider_data import ProviderData
from .setter_default_or_value import SetterDefaultOrValue


class Item(CustomBaseModel):
    quantity: Optional[float] = Field(alias='quantity',
                                      description='Количество. Тэг 1023',
                                      allow_mutation=False)
    price_rub: Optional[float] = Field(alias='price',
                                       description='Цена за единицу. Тэг 1079',
                                       allow_mutation=False)
    name: Optional[str] = Field(alias='name',
                                description='Наименование товара. Тэг 1030',
                                allow_mutation=False)
    sum_rub: Optional[float] = Field(alias='sum',
                                     description='Стоимость предмета расчета с учетом скидок и наценок. Тэг 1043',
                                     allow_mutation=False)
    payment_type: Optional[int] = Field(alias='paymentType',
                                        description='Признак способа расчета. Тэг 1214',
                                        allow_mutation=False)
    unit_nds_rub: Optional[float] = Field(alias='unitNds',
                                          description='Размер НДС за единицу предмета расчета. Тэг 1198',
                                          allow_mutation=False)
    nds18118_rub: Optional[float] = Field(alias='nds18118',
                                          description='Сумма НДС чека по расч. Ставке 18/118.'
                                                      'Тэг 1106 (Вероятно тэга в items нет)',
                                          allow_mutation=False)
    nds18_rub: Optional[float] = Field(alias='nds18',
                                       description='НДС итога чека со ставкой 18%. Тэг 1102',
                                       allow_mutation=False)
    nds_sum_rub: Optional[float] = Field(alias='ndsSum',
                                         description='Сумма НДС за предмет расчета. Тэг 1200',
                                         allow_mutation=False)
    nds10_rub: Optional[float] = Field(alias='nds10',
                                       description='НДС итога чека со ставкой 10%. Тэг 1103',
                                       allow_mutation=False)
    unit: Optional[str] = Field(alias='unit',
                                description='Единица измерения предмета расчета. Тэг 1197',
                                allow_mutation=False)
    product_code: Optional[str] = Field(alias='productCode',
                                        description='Код товара. Тэг 1162',
                                        allow_mutation=False)
    product_type: Optional[int] = Field(alias='productType',
                                        description='Признак предмета расчета. 1212',
                                        allow_mutation=False)
    payment_agent_by_product_type: Optional[int] = Field(alias='paymentAgentByProductType',
                                                         description='Признак агента по предмету расчета. Тэг 1222',
                                                         allow_mutation=False)
    provider_inn: Optional[str] = Field(alias='providerInn',
                                        description='ИНН поставщика. Тэг 1226',
                                        allow_mutation=False)
    payment_agent_data: Optional[list[PaymentAgent]] = Field(alias='paymentAgentData',
                                                             description='Данные агента. Тег 1223',
                                                             allow_mutation=False)
    provider_data: Optional[ProviderData] = Field(alias='providerData',
                                                  description='Данные поставщика. Тэг 1224',
                                                  allow_mutation=False)
    # TODO раньше брался первый элемент!
    product_code_new: Optional[list[ProdCodeNew]] = Field(alias='productCodeNew',
                                                          description='Код товара. Тэг 1163',
                                                          allow_mutation=False)
    labeled_prod_fractional_quantity: Optional[list[Fract]] = Field(alias='labeledProdFractionalQuantity',
                                                                    description='Дробное количество маркированного '
                                                                                'товара. Тэг 1291',
                                                                    allow_mutation=False)

    @validator("price_rub",
               "sum_rub",
               "unit_nds_rub",
               "nds18118_rub",
               "nds18_rub",
               "nds_sum_rub",
               "nds10_rub",
               pre=True,
               always=True,
               check_fields=False)
    def _set_rub_fields(cls, value: Optional[int]) -> float:
        return SetterDefaultOrValue.set_rub(value)

    @validator("unit",
               "product_code",
               "provider_inn",
               "name",
               pre=True,
               always=True,
               check_fields=False)
    def _set_string_fields(cls, value: Optional[str]) -> str:
        return SetterDefaultOrValue.set_str(value)

    @validator("product_type",
               "payment_type",
               "payment_agent_by_product_type",
               pre=True,
               always=True,
               check_fields=False)
    def _set_int_fields(cls, value: Optional[int]) -> int:
        return SetterDefaultOrValue.set_number(value)

    @validator("quantity", pre=True, always=True, check_fields=False)
    def _set_quantity(cls, value: Optional[int]) -> float:
        return SetterDefaultOrValue.set_number(value)

    @validator("payment_agent_data", pre=True, always=True, check_fields=False)
    def _set_payment_agent_data(cls, value: Optional[Union[PaymentAgent, list[PaymentAgent]]]) -> list[PaymentAgent]:
        return SetterDefaultOrValue.set_obj_to_list_obj(value)

    @validator("provider_data", pre=True, always=True, check_fields=False)
    def _set_provider_data(cls, value: Optional[ProviderData]) -> ProviderData:
        return ProviderData.parse_obj({}) if value is None else value

    @validator("product_code_new", pre=True, always=True, check_fields=False)
    def _set_product_code_new(cls, value: Optional[Union[ProdCodeNew, list[ProdCodeNew]]]) -> list[ProdCodeNew]:
        return SetterDefaultOrValue.set_obj_to_list_obj(value)

    @validator("labeled_prod_fractional_quantity", pre=True, always=True, check_fields=False)
    def _set_labeled_prod_fractional_quantity(cls, value: Optional[Union[list[Fract], Fract]]) -> list[Fract]:
        return SetterDefaultOrValue.set_obj_to_list_obj(value)

    @property
    def total_nds(self) -> float:
        """Кастомное поле для получения общего НДС за товар"""
        return round(self.unit_nds_rub + self.nds18118_rub + self.nds18_rub + self.nds_sum_rub + self.nds10_rub, 2)
