from typing import Optional
from pydantic import Field, validator

from .custom_base_model import CustomBaseModel
from .setter_default_or_value import SetterDefaultOrValue


class ProductCodeNew(CustomBaseModel):
    undefined: Optional[str] = Field(alias='undefined',
                                     description='Нераспознанный код товара. Тэг 1300',
                                     allow_mutation=False)
    ean8: Optional[str] = Field(alias='ean8',
                                description='КТ EAN-8. Тэг 1301',
                                allow_mutation=False)
    ean13: Optional[str] = Field(alias='ean13',
                                 description='КТ EAN-13. Тэг 1302',
                                 allow_mutation=False)
    itf14: Optional[str] = Field(alias='itf14',
                                 description='КТ ITF-14. Тэг 1303',
                                 allow_mutation=False)
    gs1: Optional[str] = Field(alias='gs1',
                               description='КТ GS1.0. Тэг 1304',
                               allow_mutation=False)
    gs1m: Optional[str] = Field(alias='gs1m',
                                description='КТ GS1.М. Тэг 1305',
                                allow_mutation=False)
    kmk: Optional[str] = Field(alias='kmk',
                               description='КТ КМК. Тэг 1306',
                               allow_mutation=False)
    mi: Optional[str] = Field(alias='mi',
                              description='КТ МИ. Тэг 1307',
                              allow_mutation=False)
    egais2: Optional[str] = Field(alias='egais2',
                                  description='КТ ЕГАИС-2.0. Тэг 1308',
                                  allow_mutation=False)
    egais3: Optional[str] = Field(alias='egais3',
                                  description='КТ ЕГАИС-3.0. Тэг 1309',
                                  allow_mutation=False)

    @validator("undefined",
               "ean8",
               "ean13",
               "itf14",
               "gs1",
               "gs1m",
               "kmk",
               "mi",
               "egais2",
               "egais3",
               pre=True,
               always=True,
               check_fields=False)
    def _set_string_fields(cls, value: Optional[str]) -> str:
        return SetterDefaultOrValue.set_str(value)
