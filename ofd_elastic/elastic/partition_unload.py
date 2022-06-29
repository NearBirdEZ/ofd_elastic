from copy import deepcopy
from math import ceil
from typing import NamedTuple, Optional, Generator

from ofd_elastic.elastic.elastic import Elastic


class ResultAggregations(NamedTuple):
    head_agg: str
    sub_agg: Optional[str]


class PartitionUnload:
    __slots__ = ('_elastic',
                 '_parts_size',
                 '_request',
                 '_index',
                 '_head_agg',
                 '_sub_agg')

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

    def get(self) -> list[ResultAggregations]:
        collection: list[ResultAggregations] = []
        for aggregation in self.get_generator():
            collection += aggregation
        return collection

    def get_generator(self) -> Generator[list[ResultAggregations], None, None]:
        parts: int = self._get_count_parts()
        return (self._parsing_aggregations(self._get_aggregation_part(num_part, parts)) for num_part in range(parts))

    def _parsing_aggregations(self, aggs: dict) -> list[ResultAggregations]:
        parsing_list: list[ResultAggregations] = []
        for value_1 in aggs['name1']['buckets']:
            if self._sub_agg:
                parsing_list.extend(
                    ResultAggregations(value_1['key'], value_2['key']) for value_2 in value_1['name2']['buckets'])
            else:
                parsing_list.append(
                    ResultAggregations(value_1['key'], None)
                )
        return parsing_list

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
