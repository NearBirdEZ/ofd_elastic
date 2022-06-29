from copy import deepcopy
from enum import Enum
from typing import Optional

import requests
import re
from re import Pattern

from requests import Response

from ofd_elastic.exceptions import NotValidUrlException
from ofd_elastic.exceptions.singleton_exist_exception import SingletonExistException


class QueryElasticTypeEnum(Enum):
    search: str = "_search"
    count: str = "_count"

    def __str__(self):
        return self._value_


class Elastic:
    __slots__ = ("__url", "__params")

    def __init__(self, url: str, login: str = None, password: str = None):
        self.__url: str = self.check_pattern_url(url)
        self.__params: dict = {
            'headers': {'Content-Type': 'application/json', },
            'params': (('pretty', ''),),
            'auth': (login, password) if all((login, password)) else (),
            'timeout': 60
        }

    @staticmethod
    def check_pattern_url(url: str) -> str:
        if url is None:
            raise NotValidUrlException("The url cannot be None")
        simple_regex: str = r"^https?://(www.)?\S{1,256}(\.|:)[a-zA-Z0-9]{2,10}/"
        pattern: Pattern = re.compile(simple_regex)
        if pattern.match(url):
            return url
        raise NotValidUrlException(
            "Uncorrected url. The url should look like 'http(s)://0.0.0.0:1234/' or 'http(s)//site.ru/"
        )

    def query(self, data: dict, index: str = '*', type_: QueryElasticTypeEnum = QueryElasticTypeEnum.search) -> dict:
        url: str = f'{self.__url}{index}/{type_}'
        response: Response = requests.post(url=url, **self.__params, json=data)
        return response.json()

    def put(self, data: dict, index: str, doc_type: str, id_doc: str) -> None:
        url: str = f'{self.__url}{index}/{doc_type}/{id_doc}'
        requests.put(url=url, **self.__params, json=data)

    def count_unique_per_agg(self, data: dict, index: str = '*', agg: str = 'requestmessage.kktRegId.raw') -> int:
        cardinality: dict = deepcopy(data)
        cardinality['aggs']: dict = {
            "name": {
                "cardinality": {
                    "field": agg
                }
            }
        }
        return self.query(cardinality, index)['aggregations']['name']['value']

    def scroll(self, data: dict, index: str, sid: str = None, window_time: str = "1m") -> dict:
        scroll_data: dict = deepcopy(data)
        if not sid:
            url: str = f'{self.__url}{index}/_search?scroll={window_time}'
        else:
            url: str = f"{self.__url}/_search/scroll"
            scroll_data: dict = {
                "scroll": window_time,
                "scroll_id": sid
            }
        return requests.post(url=url, **self.__params, json=scroll_data).json()


class ElasticSingleton(Elastic):
    __instance: Optional["ElasticSingleton"] = None

    @classmethod
    def create_singleton(cls, url: str, login: Optional[str] = None, password: Optional[str] = None):
        if cls.__instance is not None:
            raise SingletonExistException("Singleton already exists")
        cls.__instance = ElasticSingleton(url, login, password)

    @classmethod
    def get_singleton(cls) -> "ElasticSingleton":
        if cls.__instance is None:
            raise SingletonExistException("Singleton not exists")
        return cls.__instance
