from typing import Optional
from pydantic import validator, Field

from .custom_base_model import CustomBaseModel
from .setter_default_or_value import SetterDefaultOrValue


class LabeledProdFractionalQuantity(CustomBaseModel):
    fractional_part: Optional[str] = Field(alias='fractionalPart',
                                           description='Дробная часть. Тэг 1292',
                                           allow_mutation=False)
    numerator: Optional[int] = Field(alias='numerator',
                                     description='Числитель. Тэг 1293',
                                     allow_mutation=False)
    denominator: Optional[int] = Field(alias='denominator',
                                       description='Знаменатель. Тэг 1294',
                                       allow_mutation=False)

    @validator("fractional_part", pre=True, always=True, check_fields=False)
    def _set_fractional_part(cls, value: Optional[str]) -> str:
        return SetterDefaultOrValue.set_str(value)

    @validator("numerator",
               "denominator",
               pre=True,
               always=True,
               check_fields=False)
    def _set_int_fields(cls, value: Optional[int]) -> int:
        return SetterDefaultOrValue.set_number(value)
