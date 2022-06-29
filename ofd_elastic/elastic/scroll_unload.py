import re
from json import loads, dumps
from math import ceil
from pydantic import BaseModel
from typing import Type
from copy import deepcopy

from .elastic import Elastic, QueryElasticTypeEnum


class ScrollUnload:
    __slots__ = (
        "_elastic",
        "_request",
        "_model",
        "_unload_size",
        "_index",
        "_sid",
        "_count_receipt",
        "_window_time"
    )

    def __init__(self,
                 elastic: Elastic,
                 request: dict,
                 doc_model: Type[BaseModel],
                 index='*',
                 unload_size: int = 100) -> None:
        self._unload_size: int = unload_size
        self._elastic: Elastic = elastic
        self._request: dict = loads(dumps(request))
        self._model: Type[BaseModel] = doc_model
        self._index: str = index
        self._sid: str = ''
        self._count_receipt: int = self._set_count_receipt()
        self._window_time: str = '1m'

    @property
    def window_time(self) -> str:
        """Время открытия окна для выполнения запроса."""
        return self._window_time

    @window_time.setter
    def window_time(self, value) -> None:
        if isinstance(value, str) and re.match(r'\d{1,5}([smhd]|ms|micros|nanos)', value):
            self._window_time = value
        else:
            raise TypeError('window_time will be have pattern "{int}{[nanos/micros/ms/s/m/h/d]}"')

    def _set_count_receipt(self) -> int:
        request: dict = deepcopy(self._request)
        request.pop('size')
        count: int = self._elastic.query(request, self._index, QueryElasticTypeEnum.count)['count']
        self._request['size'] = self._unload_size
        return count

    def __iter__(self) -> "ScrollUnload":
        return self

    def __next__(self) -> list[BaseModel]:
        response: dict = self._elastic.scroll(self._request, self._index, self._sid, self.window_time)
        self._sid = response['_scroll_id']
        if receipts := response['hits']['hits']:
            return [self._model.parse_obj(receipt) for receipt in receipts]
        raise StopIteration

    def __len__(self) -> int:
        """Возвращает количество предстоящих итераций"""
        return ceil(self._count_receipt / self._unload_size)

    @property
    def count_receipts(self) -> int:
        """Возвращает количество чеков, попавших под выборку"""
        return self._count_receipt

