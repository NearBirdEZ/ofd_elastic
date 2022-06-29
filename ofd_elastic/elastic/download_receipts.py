from copy import deepcopy
from math import ceil
from typing import Iterable

from .elastic import Elastic
from ofd_elastic.docs.receipt.receipt import Receipt
from ..exceptions.limit_size_exception import LimitSizeException


class DownloadReceipts:
    __slots__ = (
        "_elastic",
        "_index",
        "_unload_size",
        "_request",
        "_min_fd",
        "_max_fd",
        "_iteration",
        "_num_iter"
    )

    def __init__(self,
                 elastic: Elastic,
                 request: dict,
                 rnm: str,
                 fn: str,
                 index: str = '*',
                 size: int = 8000) -> None:
        self._elastic: Elastic = elastic
        self._index: str = index
        self._unload_size: int = self._set_size(size)
        self._request: dict = self._set_request(request, rnm, fn)
        self._min_fd: int = 0
        self._max_fd: int = 0
        self._iteration: int = 1
        self._num_iter: int = 0
        self._set_range_unload()

    @staticmethod
    def _set_size(size: int) -> int:
        if size > 10_000:
            raise LimitSizeException("Размер одной итерации ограничен 10_000 шт.")
        return size

    def _set_request(self, request: dict, rnm: str, fn: str) -> dict:
        el_request: dict = deepcopy(request)
        el_request['size'] = self._unload_size + 1
        el_request['query']['bool']['must'].append(
            {
                "term": {
                    "requestmessage.fiscalDriveNumber.raw": fn
                }
            }
        )
        el_request['query']['bool']['must'].append(
            {
                "term": {
                    "requestmessage.kktRegId.raw": rnm
                }
            }
        )
        return el_request

    @property
    def iteration(self) -> int:
        return self._iteration + 1

    @property
    def num_iteration(self) -> int:
        return self._num_iter

    def _set_range_unload(self) -> None:
        request: dict = deepcopy(self._request)
        request['aggs'] = {
            "stats": {
                "stats": {
                    "field": "requestmessage.fiscalDocumentNumber"
                }
            }
        }

        stats: dict = self._elastic.query(request, self._index)
        self._min_fd = stats['aggregations']['stats'].get('min') or 0
        self._max_fd = stats['aggregations']['stats'].get('max') or 0
        self._num_iter = 0
        self._iteration = ceil((self._max_fd - self._min_fd) / self._unload_size) or 1

    def _get_receipts(self) -> list[dict]:
        request: dict = deepcopy(self._request)
        request['query']['bool']['must'].append(
            {
                "range": {
                    "requestmessage.fiscalDocumentNumber": {
                        "gte": self._min_fd,
                        "lte": self._max_fd
                    }
                }
            }
        )
        request['sort'] = [
            {
                "requestmessage.fiscalDocumentNumber": {
                    "order": "asc"
                }
            }
        ]
        return self._elastic.query(request, self._index)['hits']['hits']

    def __iter__(self) -> Iterable:
        return iter(()) if self._max_fd + self._min_fd == 0 else self

    def _get_next(self) -> list[Receipt]:
        self._max_fd = self._min_fd + self._unload_size
        receipts: list[dict] = self._get_receipts()
        self._min_fd += (self._unload_size + 1)
        self._num_iter += 1
        if receipts:
            return [Receipt.parse_obj(receipt) for receipt in receipts]
        if self._max_fd + self._min_fd == 0:
            return []
        if self._num_iter == self._iteration:
            raise IndexError('Что-то пошло не так')
        return self._get_next()

    def __next__(self) -> list[Receipt]:
        if self._num_iter != self._iteration:
            return self._get_next()
        self._set_range_unload()
        raise StopIteration
