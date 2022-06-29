from typing import Optional, Union
from pydantic import validator, Field

from .custom_base_model import CustomBaseModel
from .setter_default_or_value import SetterDefaultOrValue


class ProviderData(CustomBaseModel):
    provider_name: Optional[str] = Field(alias='providerName',
                                         description='Телефон поставщика. Тэг 1171',
                                         allow_mutation=False)
    provider_phone: Optional[str] = Field(alias='providerPhone',
                                          description='Наименование поставщика. Тэг 1225',
                                          allow_mutation=False)

    @validator("provider_name", pre=True, always=True, check_fields=False)
    def _set_provider_name(cls, value: Optional[str]) -> str:
        return SetterDefaultOrValue.set_str(value)

    @validator("provider_phone", pre=True, always=True, check_fields=False)
    def _set_provider_phone(cls, value: Optional[Union[list[str], str]]) -> str:
        return SetterDefaultOrValue.set_list_to_str(value)
