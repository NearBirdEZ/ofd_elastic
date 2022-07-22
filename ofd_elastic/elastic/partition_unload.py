from copy import deepcopy
from math import ceil
from typing import Optional, Generator

from ofd_elastic.elastic import PartitionAgg
from ofd_elastic import Elastic


class PartitionUnload:
    __slots__ = ('_elastic',
                 '_parts_size',
                 '_request',
                 '_index',
                 '_head_agg',
                 '_sub_agg',
                 '_data')

    def __init__(self,
                 elastic: Elastic,
                 elastic_request: dict,
                 index: str,
                 head_agg: str,
                 sub_agg: Optional[str]):
        self._elastic: Elastic = elastic
        self._parts_size: int = 100
        self._request: dict = deepcopy(elastic_request)
        self._index: str = index
        self._head_agg: str = head_agg
        # Second aggs have default 20 size
        self._sub_agg: Optional[str] = sub_agg
        self._data: list[PartitionAgg] = self._create_data()

    @property
    def data(self):
        return self._data

    def to_dict(self) -> dict:
        return {agg.head_agg: agg.sub_aggs for agg in self._data}

    def _create_data(self) -> list[PartitionAgg]:
        data: list[PartitionAgg] = []
        for aggregation in self._get_generator():
            data += aggregation
        return data

    def _get_generator(self) -> Generator[list[PartitionAgg], None, None]:
        parts: int = self._get_count_parts()
        return (self._parsing_aggregations(self._get_aggregation_part(num_part, parts)) for num_part in range(parts))

    @staticmethod
    def _parsing_aggregations(aggs: dict) -> list[PartitionAgg]:
        return [PartitionAgg.parse_obj(agg) for agg in aggs['name1']['buckets']]

    def _get_count_parts(self) -> int:
        agg_value: int = self._elastic.count_unique_per_agg(self._request, self._index)
        return ceil(agg_value / self._parts_size)

    def _get_aggregation_part(self, num_part: int, parts: int) -> dict:
        self._request['aggs'] = {
            "name1": {
                "terms": {
                    "field": self._head_agg,
                    "include": {
                        "partition": num_part,
                        "num_partitions": parts
                    },
                    "size": self._parts_size
                }
            }
        }
        if self._sub_agg:
            self._request['aggs']['name1']['aggs'] = {
                "name2": {
                    "terms": {
                        "field": self._sub_agg,
                        "size": 20
                    }
                }
            }
        return self._elastic.query(self._request, self._index)['aggregations']
