from functools import reduce
from typing import Iterable


class TotalFdSumRub:

    def __init__(self,
                 *,
                 total_sum: float,
                 cash_total_sum: float,
                 ecash_total_sum: float,
                 prepaid_sum: float,
                 credit_sum: float,
                 provision_sum: float) -> None:
        self._total_sum: float = round(total_sum, 2)
        self._cash_total_sum: float = round(cash_total_sum, 2)
        self._ecash_total_sum: float = round(ecash_total_sum, 2)
        self._prepaid_sum: float = round(prepaid_sum, 2)
        self._credit_sum: float = round(credit_sum, 2)
        self._provision_sum: float = round(provision_sum, 2)

    @staticmethod
    def sum(iterable: Iterable) -> "TotalFdSumRub":
        return reduce((lambda x, y: x + y), iterable)

    def invert_values(self) -> None:
        """Функция для инвертирования значений. Используется в случае, если тип операции равен 2 или 3"""
        self._total_sum *= (-1)
        self._cash_total_sum *= (-1)
        self._ecash_total_sum *= (-1)
        self._prepaid_sum *= (-1)
        self._credit_sum *= (-1)
        self._provision_sum *= (-1)

    def __add__(self, other: "TotalFdSumRub") -> "TotalFdSumRub":
        return TotalFdSumRub(
            total_sum=self._total_sum + other.total_sum,
            cash_total_sum=self._cash_total_sum + other.cash_total_sum,
            ecash_total_sum=self._ecash_total_sum + other.ecash_total_sum,
            prepaid_sum=self._prepaid_sum + other.prepaid_sum,
            credit_sum=self._credit_sum + other.credit_sum,
            provision_sum=self._provision_sum + other.provision_sum
        )

    def __repr__(self) -> str:
        return str([
            self._total_sum,
            self._cash_total_sum,
            self._ecash_total_sum,
            self._prepaid_sum,
            self._credit_sum,
            self._provision_sum
        ])

    def __str__(self) -> str:
        return f"{self._total_sum}\n" \
               f"{self._cash_total_sum}\n" \
               f"{self._ecash_total_sum}\n" \
               f"{self._prepaid_sum}\n" \
               f"{self._credit_sum}\n" \
               f"{self._provision_sum}"

    @property
    def total_sum(self) -> float:
        return self._total_sum

    @property
    def cash_total_sum(self) -> float:
        return self._cash_total_sum

    @property
    def ecash_total_sum(self) -> float:
        return self._ecash_total_sum

    @property
    def prepaid_sum(self) -> float:
        return self._prepaid_sum

    @property
    def credit_sum(self) -> float:
        return self._credit_sum

    @property
    def provision_sum(self) -> float:
        return self._provision_sum
